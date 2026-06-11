from fastapi import FastAPI
import database
from routes import symbols

# create app

app = FastAPI(title = "Liquid-Labs Market Data API")

# creat DB tables when app start

database.init_db()

# register our routes
app.include_router(symbols.router)