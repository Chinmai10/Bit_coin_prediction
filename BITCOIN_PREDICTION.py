import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from binance.client import Client
import datetime

# Initialize Binance client
client = Client()

# Function to fetch historical data for any cryptocurrency pair
def fetch_data(symbol, start_date="1 Jan, 2020"):
    symbol = symbol.upper()  # Ensure the symbol is in uppercase
    klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, start_date)
    df = pd.DataFrame(klines, columns=["open_time", "open", "high", "low", "close", "volume", "close_time", "quote", "no_trades", "base_buy", "quote_buy", "ignore"])
    df["date"] = pd.to_datetime(df["open_time"], unit='ms')
    df["close"] = df["close"].astype(float)
    return df[["date", "close"]]

# Function to prepare data for model training
def prepare_data(df, n_in=20, n_out=1):
    df = pd.DataFrame(df["close"].values)
    cols = list()
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
    cols.append(df.shift(-n_out))
    full_df = pd.concat(cols, axis=1).dropna().reset_index(drop=True)
    full_df.columns = [f't{i}' for i in range(n_in, 0, -1)] + ['target']
    full_df['target'] = full_df['target'] - full_df['t1']
    for col in full_df.columns[:-1]:
        full_df[col] = full_df[col] - full_df['t1']
    return full_df

# Function to predict future prices
def predict_future_prices(model, last_known_prices, n_in=20, days=365):
    future_prices = []
    for _ in range(days):
        input_features = np.array(last_known_prices[-n_in:]).reshape(1, -1)
        next_price_change = model.predict(input_features)[0]
        next_price = last_known_prices[-1] + next_price_change
        future_prices.append(next_price)
        last_known_prices.append(next_price)
    return future_prices

# Main function
def main():
    symbol = input("Enter the cryptocurrency pair (e.g., BTCUSDT): ").upper()
    df = fetch_data(symbol)
    
    full_df = prepare_data(df)
    
    input_col_names = [f't{i}' for i in range(20, 0, -1)]
    target_col_name = 'target'
    
    train_X = full_df[input_col_names]
    train_y = full_df[target_col_name]
    
    model = XGBRegressor(objective='reg:squarederror', n_estimators=200)
    model.fit(train_X, train_y)
    
    last_known_prices = df["close"].values[-20:].tolist()
    future_prices = predict_future_prices(model, last_known_prices)
    
    start_date = df["date"].iloc[-1] + pd.Timedelta(days=1)
    future_dates = pd.date_range(start=start_date, periods=365, freq='D')
    predicted_df = pd.DataFrame({"date": future_dates, "predicted_price": future_prices ,"currency": "USD"})
    
    print(predicted_df)

if __name__ == "__main__":
    main()
    