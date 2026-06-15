import yfinance as yf
import json
import time
from datetime import datetime

DATA_FILE = "data.json"

stocks = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "NAVER": "035420.KS"
}

INITIAL_CASH = 10_000_000

def load():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {
            "cash": INITIAL_CASH,
            "positions": {},
            "trades": [],
            "assets": []
        }

def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load()

print("🚀 백테스트 엔진 시작")

while True:
    cash = data["cash"]
    positions = data["positions"]

    total_asset = cash
    unrealized = 0

    for name, code in stocks.items():
        try:
            price = yf.Ticker(code).history(period="1d", interval="1m")["Close"].iloc[-1]

            # =========================
            # 📌 매수 (없으면 1회만)
            # =========================
            if name not in positions and cash > price:
                positions[name] = {
                    "buy_price": price,
                    "qty": 1
                }

                data["cash"] -= price

                data["trades"].append({
                    "type": "BUY",
                    "name": name,
                    "price": price,
                    "time": str(datetime.now())
                })

            # =========================
            # 📌 평가 손익
            # =========================
            if name in positions:
                buy_price = positions[name]["buy_price"]
                qty = positions[name]["qty"]

                profit_rate = (price - buy_price) / buy_price
                unrealized += (price - buy_price) * qty

                # =========================
                # 📌 매도 조건 (+0.7%)
                # =========================
                if profit_rate > 0.007:
                    data["cash"] += price * qty

                    data["trades"].append({
                        "type": "SELL",
                        "name": name,
                        "price": price,
                        "profit_pct": round(profit_rate*100, 2),
                        "time": str(datetime.now())
                    })

                    del positions[name]

        except:
            pass

    total_asset = data["cash"] + unrealized

    data["assets"].append({
        "time": str(datetime.now()),
        "total": total_asset,
        "cash": data["cash"],
        "unrealized": unrealized
    })

    save(data)

    print(f"💰 총자산: {int(total_asset)} | 현금: {int(data['cash'])}")

    time.sleep(30)