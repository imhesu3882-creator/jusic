import yfinance as yf
import json
import time
from datetime import datetime

DATA_FILE = "data.json"

stocks = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "NAVER": "035420.KS",
    "현대차": "005380.KS"
}

# 초기 자본
cash = 10_000_000
holdings = {}

def load():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"trades": [], "assets": []}

def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load()

print("🚀 엔진 시작 (자동매매 실행 중)")

while True:
    total = cash

    for name, code in stocks.items():
        try:
            price = yf.Ticker(code).history(period="1d", interval="1m")["Close"].iloc[-1]

            # 매우 단순 전략 (테스트용)
            if name not in holdings:
                holdings[name] = price
                cash_used = price

                data["trades"].append({
                    "type": "BUY",
                    "name": name,
                    "time": str(datetime.now()),
                    "price": price
                })

            else:
                change = (price - holdings[name]) / holdings[name]

                # +0.7% 익절
                if change > 0.007:
                    cash += price
                    data["trades"].append({
                        "type": "SELL",
                        "name": name,
                        "time": str(datetime.now()),
                        "profit_pct": round(change*100,2)
                    })
                    del holdings[name]

        except:
            pass

    # 총 자산 계산
    total = cash + sum(holdings.values())

    data["assets"].append({
        "time": str(datetime.now()),
        "total": total
    })

    save(data)

    print("💰 자산:", int(total))

    time.sleep(30)