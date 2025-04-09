# Bitcoin Price Prediction API

This project is a FastAPI-based web application that predicts future Bitcoin (or other cryptocurrency) prices using historical data and machine learning. The model is built using the XGBoost library and fetches historical data from the Binance API.

## Features

- Fetches historical cryptocurrency price data from Binance.
- Validates cryptocurrency symbols using Binance's exchange information.
- Prepares data for machine learning by creating lagged features.
- Trains an XGBoost regression model to predict future price changes.
- Predicts cryptocurrency prices for the next 365 days.
- Provides a RESTful API endpoint to fetch predictions in JSON format.

## Requirements

- Python 3.8 or higher
- FastAPI
- Uvicorn
- NumPy
- Pandas
- XGBoost
- Binance API

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/bitcoin_prediction.git
   cd bitcoin_prediction


