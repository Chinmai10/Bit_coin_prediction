# Bitcoin Price Prediction

This project predicts future Bitcoin prices using historical data and machine learning. The model is built using the XGBoost library and fetches historical data from the Binance API.

## Requirements

- Python 3.x
- NumPy
- Pandas
- XGBoost
- Binance API

You can install the required packages using pip:

```sh
pip install numpy pandas xgboost python-binance
```

## Usage

1. Clone the repository:

```sh
git clone https://github.com/yourusername/bitcoin_prediction.git
cd bitcoin_prediction
```

2. Run the script:

```sh
python BITCOIN_PREDICTION.py
```

3. Enter the cryptocurrency pair when prompted (e.g., `BTCUSDT`).

The script will fetch historical data, train the model, and predict future prices for the next 365 days. The predicted prices will be printed in the console.

## Functions

### `fetch_data(symbol, start_date="1 Jan, 2020")`

Fetches historical data for the given cryptocurrency pair from Binance.

### `prepare_data(df, n_in=20, n_out=1)`

Prepares the data for model training by creating lagged features and target variables.

### `predict_future_prices(model, last_known_prices, n_in=20, days=365)`

Predicts future prices using the trained model and the last known prices.

## Main Function

### `main()`

- Prompts the user to enter the cryptocurrency pair.
- Fetches historical data.
- Prepares the data for training.
- Trains the XGBoost model.
- Predicts future prices for the next 365 days.
- Prints the predicted prices.

## License

This project is licensed under the MIT License.