# Liquid Labs Market Data API

## Overview

This is a simple REST API that I built for the Liquid Labs assignment.
if user enter a stock symbol and year, the API will return the highest price,
lowest price and total trading volume for that year.

Data is fetched from Alpha Vantage free API.
If the data is not in the database, system will call the API and
locally save it to a SQLite database. if the same request comes again,
system will return data directly from database without calling the API again.

## How it works

1. User sends request with stock symbol and year
2. System checks SQLite database
3. If data exists → return it
4. If not → call Alpha Vantage API
5. Save result to database
6. Return response to user

## Architecture

```
Client Request
     |
     v
FastAPI Endpoint
     |
     v
Check SQLite Database
     |
  Yes -----> Return Cached Data
     |
     No
     |
     v
Call Alpha Vantage API
     |
     v
Save to SQLite
     |
     v
Return Response
```

## Why caching?

Alpha Vantage has request limits, so I store results in SQLite.
if the same request comes again, I return cached data instead of calling the API.

## Tech Stack

- Python 3.x
- FastAPI
- SQLite
- Alpha Vantage API

## Project Structure

```
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
```

## Database Structure

```
monthly_data table:

symbol   TEXT
date     TEXT
high     REAL
low      REAL
volume   INTEGER
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/chenitha-ranasinghe/liquid-labs-assignment.git
cd liquid-labs-assignment
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

Mac/Linux:
```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

create a .env file in the root folder and add your API key:

```
ALPHAVANTAGE_API_KEY=your_api_key_here
```

you can get a free API key from here:
https://www.alphavantage.co/support/#api-key
(use role: Student, you will get 25 free requests per day)

### 5. Run the API

```bash
uvicorn main:app --reload
```

## API Usage

### Endpoint

```
GET /symbols/{symbol}/annual/{year}
```

### Example

```
GET /symbols/IBM/annual/2005
```

### Response

```json
{
    "high": "99.1000",
    "low": "71.8500",
    "volume": "1539128900"
}
```

### Error Responses

- 400 - year format is wrong, must be YYYY format like 2005
- 400 - symbol must contain letters only
- 404 - symbol not found or no data available for that year
- 503 - something went wrong when calling Alpha Vantage API

## Why FastAPI?

FastAPI makes it easy to build REST APIs and automatically handles validation.
also it generates interactive API documentation at /docs which is useful for testing.

## Why SQLite?

I used SQLite because it is simple and enough for local caching.
no extra setup needed, everything is in one file.

## Why requests?

Used for calling the Alpha Vantage API from Python.

## Why python-dotenv?

I used this to load the API key from .env file so I don't have to
hardcode it directly in the code.

## Interactive API Docs

after running the app you can visit:

```
http://127.0.0.1:8000/docs
```