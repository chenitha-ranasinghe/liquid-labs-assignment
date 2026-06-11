# Liquid Labs Market Data API

## Overview

this is a simple REST API that i built for the liquid labs assignment.
if user give a stock symbol and year, this API will return the highest price, 
lowest price and total trading volume for that year.

i used Alpha Vantage free API for get the stock data. when user make a request, 
first i check the local SQLite database. if data is not there, system will call 
the Alpha Vantage API and save that data to the database. so next time if same 
request came, system will directly give data from database without calling 
the API again. this is basically how the caching works.

## Tech Stack

- Python 3.x
- FastAPI
- SQLite
- Alpha Vantage API

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

## Setup

### 1. Clone the repository

git clone https://github.com/chenitha-ranasinghe/liquid-labs-assignment.git
cd liquid-labs-assignment

### 2. Create virtual environment

python -m venv .venv

Windows:
.venv\Scripts\activate

Mac/Linux:
source .venv/bin/activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Set up environment variables

create a .env file in the root folder and add your API key:
ALPHAVANTAGE_API_KEY=your_api_key_here

you can get a free API key from here:
https://www.alphavantage.co/support/#api-key


### 5. Run the API

uvicorn main:app --reload

## API Usage

### Endpoint

GET /symbols/{symbol}/annual/{year}

### Example Request

GET /symbols/IBM/annual/2005

### Example Response

{
    "high": "99.1",
    "low": "71.85",
    "volume": "1539128900"
}

### Error Responses

- 400 - year format is wrong, must be YYYY format like 2005
- 404 - symbol not found or no data available for that year
- 503 - something went wrong when calling Alpha Vantage API

## Libraries Used

- **fastapi** - i used fastapi to build the REST API. i choose this because 
it automatically validates the input data and also it generate interactive 
API documentation at /docs endpoint which is really useful for testing

- **uvicorn** - i used uvicorn because its the server that runs the fastapi 
application. fastapi needs uvicorn to actually run

- **requests** - i used requests library for make HTTP GET calls to the 
Alpha Vantage external API. this is a popular python library for HTTP requests

- **python-dotenv** - i used this because i stored my API key in .env file. 
this library loads the API key from .env file so i dont have to hardcode 
the API key directly in the code

## Interactive API Docs

after running the app you can visit this url in browser:
http://127.0.0.1:8000/docs