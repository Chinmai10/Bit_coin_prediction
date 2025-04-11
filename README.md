# Cryptocurrency Price Prediction API

This project is a FastAPI-based web application that predicts future cryptocurrency prices using historical data and machine learning. The model is built using the XGBoost library and fetches historical data from the Binance API.

## Features

- Fetches historical cryptocurrency price data from Binance.
- Validates cryptocurrency symbols using Binance's exchange information.
- Prepares data for machine learning by creating lagged features.
- Trains an XGBoost regression model to predict future price changes.
- Predicts cryptocurrency prices for the next 365 days.
- Provides RESTful API endpoints to fetch predictions in JSON format.

## Requirements

- Python 3.8 or higher
- FastAPI
- Uvicorn
- NumPy
- Pandas
- XGBoost
- Binance API
- Scikit-learn

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/Chinmai10/Bit_coin_prediction.git
   cd Bit_coin_prediction
   ```

2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Start the FastAPI server:
   ```sh
   uvicorn BITCOIN_PREDICTION:app --host 127.0.0.1 --port 8000
   ```

2. Access the API in your browser or API client at:
   ```
   http://127.0.0.1:8000
   ```

3. Use the `/predict` endpoint to get cryptocurrency price predictions. Example:
   ```
   http://127.0.0.1:8000/predict?symbol=DOGEBTC
   ```

## API Endpoints

### `/`
- **Method**: GET
- **Description**: Returns a welcome message and instructions for using the API.

### `/predict`
- **Method**: GET
- **Parameters**:
  - `symbol` (string): The cryptocurrency symbol (e.g., `ETCBTC`, `DOGEBTC`).
- **Description**: Predicts the future prices of the specified cryptocurrency for the next 365 days.

## Project Structure

```
BITCOIN_PREDICTION.py   # Main application file
Procfile                # Deployment configuration for platforms like Heroku
README.md               # Project documentation
requirements.txt        # Python dependencies
```

## Deployment

To deploy this application on a platform like Heroku, use the provided `Procfile`:
```sh
web: uvicorn BITCOIN_PREDICTION:app --host 127.0.0.1 --port $PORT
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [Binance API](https://binance-docs.github.io/apidocs/)
- [XGBoost](https://xgboost.readthedocs.io/)