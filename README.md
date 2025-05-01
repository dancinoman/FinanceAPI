[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Dockerized](https://img.shields.io/badge/Docker-Ready-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Powered-green.svg)
![Build Status](https://github.com/dancinoman/FinanceAPI/actions/workflows/.github/workflows/ci.yaml/badge.svg)

Current Version: `{{VERSION}}`

## Overview

This API provides tailored access to stock market data, specifically focusing on time series information. It's built using Python with the FastAPI framework for high performance and ease of use, and it's containerized with Docker for consistent deployment across different environments. The API fetches real-time or historical stock data from an external source (e.g., Alpha Vantage - *replace with your actual data source if different*) and presents it in a structured and easily consumable JSON format.

## Key Features

* **Time Series Data:** Specifically designed to retrieve and serve time series stock data (intraday, daily, weekly, monthly).
* **Customizable Queries:** Allows users to specify stock symbols and time intervals through query parameters.
* **Structured Response:** Returns data in a well-defined JSON format based on Pydantic models for easy integration.
* **Rate Limiting:** Implements basic rate limiting to ensure fair usage and prevent overloading the external data source.
* **Caching:** Integrates a caching strategy (e.g., Redis - *upcoming implementing*) to improve response times and reduce load on the upstream API.
* **Error Handling:** Provides informative error responses for invalid requests or issues with the external data source.
* **Dockerized:** Fully containerized using Docker, making it easy to deploy and run in various environments.
* **Built with FastAPI:** Leverages the speed, robustness, and automatic documentation features of the FastAPI framework.

## Technology Stack

* **Python:** The primary programming language.
* **FastAPI:** A modern, high-performance web framework for building APIs with Python.
* **Pydantic:** Used for data validation and serialization/deserialization.
* **Requests:** For making HTTP requests to the external stock data source.
* **Docker:** For containerization and deployment.

## API Endpoints

* **`GET /stocks/intraday`**: Retrieves intraday time series data for specified stock symbols and interval.
    * **Query Parameters:**
        * `symbols` (list of strings, required): A comma-separated list of stock symbols (e.g., `AAPL,MSFT`).
        * `interval` (string, optional, default: `5min`): The time interval for intraday data (e.g., `1min`, `15min`, `30min`, `60min`).
        * `function` (string, optional, default: `TIME_SERIES_INTRADAY`): The specific Alpha Vantage time series function to use.
    * **Response:** A JSON object containing metadata and the time series data. See the response model definition in the code for details.
    * **Error Responses:** Returns JSON objects with a `detail` field for errors (e.g., invalid symbol, rate limit exceeded, data not found).

## Getting Started

### Prerequisites

* Python 3.7+
* Docker (if you want to run the containerized version)
* An API key for the external stock data source (e.g., Alpha Vantage - set as an environment variable).

### Running Locally (without Docker)

1.  Clone the repository:
    ```bash
    git clone <your_repository_url>
    cd <your_repository_directory>
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Set your API key as an environment variable (e.g., in a `.env` file):
    ```
    API_KEY=YOUR_ALPHAVANTAGE_API_KEY
    ```
4.  Run the FastAPI application using Uvicorn:
    ```bash
    uvicorn main:app --reload
    ```
    The API will be accessible at `http://127.0.0.1:8000/stocks/intraday`.

### Running with Docker

1.  Clone the repository:
    ```bash
    git clone <your_repository_url>
    cd <your_repository_directory>
    ```
2.  Create a `.env` file at the root of the project with your API key:
    ```
    API_KEY=YOUR_ALPHAVANTAGE_API_KEY
    ```
3.  Build the Docker image:
    ```bash
    docker build -t stock-market-api .
    ```
4.  Run the Docker container, mapping port 8000 of the container to port 8000 on your host:
    ```bash
    docker run -p 8000:8000 --env-file .env stock-market-api
    ```
    The API will be accessible at `http://localhost:8000/stocks/intraday`.

## API Documentation

FastAPI automatically generates interactive API documentation using Swagger UI and ReDoc. You can access them at:

* Swagger UI: `http://localhost:8000/docs`
* ReDoc: `http://localhost:8000/redoc`

## Diagram (Recommended)

For better clarity, consider including a simple architecture diagram that illustrates the flow of data:

```mermaid
graph LR
    A[Client Application] --> B(FastAPI API);
    B --> C{Rate Limiter};
    C -- Passes --> D{Cache};
    D -- Cache Hit --> E[FastAPI Response];
    D -- Cache Miss --> F(External Stock Data Source);
    F --> G(FastAPI Processing);
    G --> H{Cache Storage};
    H --> D;
    G --> E;
    B -- Error --> I[Client Error Response];
