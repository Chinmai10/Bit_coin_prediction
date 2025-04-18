from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import pandas as pd
import sklearn as sklearn
from xgboost import XGBRegressor
from binance.client import Client
import datetime


# Initialize Binance client
client = Client()

# Initialize FastAPI app
app = FastAPI()

# Function to fetch historical data for any cryptocurrency in BTC
def fetch_data(symbol, start_date="1 Jan, 2020"):
    try:
        # Fetch historical data for the given symbol (e.g., ETHBTC, DOGEBTC)
        klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, start_date)
        df = pd.DataFrame(klines, columns=["open_time", "open", "high", "low", "close", "volume", "close_time", "quote", "no_trades", "base_buy", "quote_buy", "ignore"])
        df["date"] = pd.to_datetime(df["open_time"], unit='ms')
        df["close"] = df["close"].astype(float)
        return df[["date", "close"]]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching data for {symbol}: {e}")


# Function to validate cryptocurrency symbol
def validate_symbol(symbol):
    try:
        # Query Binance API to check if the symbol exists
        exchange_info = client.get_exchange_info()
        symbols = [s['symbol'] for s in exchange_info['symbols']]
        if symbol not in symbols:
            raise HTTPException(status_code=400, detail=f"Invalid cryptocurrency symbol: {symbol}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error validating symbol {symbol}: {e}")

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




@app.get("/")
def read_root():
    return {"Welcome to the Cryptocurrency Price Prediction" ,   
            
            "Use the /predict endpoint to get predictions for any cryptocurrency in BTC." , 
            "Example: /predict?symbol=DOGEBTC etc." ,}  


# FastAPI endpoint to predict cryptocurrency prices
@app.get("/predict")
def predict_prices(symbol: str):
    symbol = symbol.upper()
    
    # Validate the symbol
    validate_symbol(symbol)
    
    # Fetch historical data
    df = fetch_data(symbol)
    
    # Prepare data for training
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
    predictions = [{"date": str(date.date()), "predicted_price": price} for date, price in zip(future_dates, future_prices)]
    
    # Return predictions as JSON
    return {
        "symbol": symbol,
        "The predicted value is": {
            "date": str(future_dates[364].date()),
            "price": round(future_prices[364], 6)  
        }
    }
    
    