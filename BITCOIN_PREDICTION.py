import numpy as np
import pandas as pd
from binance.client import Client
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from fastapi import FastAPI, HTTPException, Query
from datetime import datetime, timedelta
from pydantic import BaseModel

app = FastAPI()
client = Client()

def fetch_5_years_data(symbol):
    end = datetime.now()
    start = end - timedelta(days=5*365)
    klines = client.get_historical_klines(
        symbol,
        Client.KLINE_INTERVAL_1DAY,
        start_str=start.strftime("%d %b, %Y"),
        end_str=end.strftime("%d %b, %Y")
    )
    if not klines:
        return pd.DataFrame()

    df = pd.DataFrame(klines, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote", "no_trades", "base_buy", "quote_buy", "ignore"
    ])
    df["date"] = pd.to_datetime(df["open_time"], unit='ms')
    df["close"] = df["close"].astype(float)
    return df[["date", "close"]]

def create_sequences(data, window=30):
    X, y = [], []
    for i in range(window, len(data)):
        X.append(data[i-window:i])
        y.append(data[i])
    return np.array(X), np.array(y)

@app.get("/predict")
def predict(symbol: str = Query(..., description="Cryptocurrency symbol like BTCUSDT")):
    symbol = symbol.upper()
    if not symbol.endswith("USDT"):
        raise HTTPException(status_code=400, detail="Only USDT pairs are supported.")

    df = fetch_5_years_data(symbol)
    if df.empty:
        raise HTTPException(status_code=404, detail="No historical data found for this symbol.")

    close_prices = df["close"].values.reshape(-1, 1)
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(close_prices)

    X, y = create_sequences(scaled_data, window=30)
    X = X.reshape((X.shape[0], X.shape[1], 1))

    model = Sequential()
    model.add(LSTM(64, return_sequences=False, input_shape=(30, 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X, y, epochs=20, batch_size=32, verbose=0)

    last_window = scaled_data[-30:].reshape(1, 30, 1)
    future_predictions = []

    for _ in range(365):
        next_price_scaled = model.predict(last_window, verbose=0)[0][0]
        future_predictions.append(float(next_price_scaled))  # Convert numpy.float32 to Python float
        last_window = np.append(last_window[:, 1:, :], [[[next_price_scaled]]], axis=1)

    predicted_prices = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1)).flatten()
    start_date = df["date"].iloc[-1] + timedelta(days=1)
    future_dates = pd.date_range(start=start_date, periods=365, freq='D')

    return {
        "symbol": symbol,
        "forecast": [
            {"date": date.strftime("%Y-%m-%d"), "predicted_price_usdt": round(float(price), 2)}  # Convert to float
            for date, price in zip(future_dates, predicted_prices)
        ]
    }