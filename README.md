# Liquid Labs Market Data API

## Overview

This is a simple REST API that I built for the Liquid Labs assignment.

If the user gives a stock symbol and year, this API will return the highest price, lowest price, and total trading volume for that year.

I used the Alpha Vantage free API to get stock data. When a user makes a request, the system first checks the local SQLite database. If the data is not there, the system will call the Alpha Vantage API and save the data to the database. Next time, if the same request comes again, the system will return data directly from the database without calling the API again. This is basically how caching works.

---

## Tech Stack

- Python 3.x  
- FastAPI  
- SQLite  
- Alpha Vantage API  

---

## Project Structure

liquid-labs-assignment/
├── main.py
├── database.py
├── routes/
│   └── symbols.py
├── services/
│   └── alpha_vantage.py
├── .env
├── requirements.txt
└── README.md

---

## Setup

### 1. Clone the repository

git clone https://github.com/chenitha-ranasinghe/liquid-labs-assignment.git
cd liquid-labs-assignment

---

### 2. Create virtual environment

python -m venv .venv

Windows:
.venv\Scripts\activate

Mac/Linux:
source .venv/bin/activate

---

### 3. Install dependencies

pip install -r requirements.txt

---

### 4. Set up environment variables

Create a .env file in the root folder and add your API key:

ALPHAVANTAGE_API_KEY=your_api_key_here

You can get a free API key from:
https://www.alphavantage.co/support/#api-key

---

### 5. Run the API

uvicorn main:app --reload

---

## API Usage

### Endpoint

GET /symbols/{symbol}/annual/{year}

### Example Request

GET /symbols/IBM/annual/2005

### Example Response

{
  "high": "99.1000",
  "low": "71.8500",
  "volume": "1539128900"
}

---

## Error Responses

- 400 → Year format is wrong (must be YYYY like 2005)  
- 404 → Symbol not found or no data available for that year  
- 503 → Error when calling Alpha Vantage API  

---

## How it works

1. User sends request with stock symbol and year  
2. System checks SQLite database  
3. If data exists → return cached data  
4. If not → call Alpha Vantage API  
5. Save result to database  
6. Return response to user  

---

## Database Structure

stock_data table:

symbol   TEXT  
year     INTEGER  
high     REAL  
low      REAL  
volume   INTEGER  

---

## Why caching?

Alpha Vantage has request limits, so I store results in SQLite.  
If the same request comes again, I return cached data instead of calling the API.

---

## Why FastAPI?

FastAPI makes it easy to build REST APIs and automatically handles input validation. It also provides interactive API documentation at /docs.

---

## Why SQLite?

I used SQLite because it is simple and enough for local caching in this project.

---

## Why requests?

Used for making HTTP calls to the Alpha Vantage API.

---

## Interactive API Docs

http://127.0.0.1:8000/docs