from fastapi import APIRouter, HTTPException
import database
import services.alpha_vantage as av

router = APIRouter()  # create route container

# check if date in DB
def data_exists_for_year(symbol: str, year: str) -> bool:
    # connect to the data base
    connection = database.get_connection()

    # count rows for this symbol and year
    symbol_and_year = connection.execute(
        "SELECT COUNT(*) as count FROM monthly_data WHERE symbol = ? AND strftime('%Y', date) = ?",
        (symbol, year)
    )
    row = symbol_and_year.fetchone()
    connection.close()

    # if count > 0 means data exists
    return row["count"] > 0

# insert data for DB from Alpha Vantage
def insert_monthly_data(symbol: str, monthly_series: dict):
    # connect to the database
    connection = database.get_connection()

    # looping all months
    for date, values in monthly_series.items():

        # only insert high, low and volume data to the database
        try:
            connection.execute(
                "INSERT OR IGNORE INTO monthly_data (symbol, date, high, low, volume) VALUES(?, ?, ?, ?, ?)",
                (
                    symbol,
                    date,
                    float(values["2. high"]),
                    float(values["3. low"]),
                    int(values["5. volume"])
                )
            )

        except Exception as e:
            print(f"Skipping row {date}: {e}")

    connection.commit()
    connection.close()

def get_annual_stats(symbol: str, year: str):
    connection = database.get_connection()

    # get high, low, volume statistis for the year
    get_high_low_volume = connection.execute(

        """
            SELECT
                MAX(high) AS high,
                MIN(low) AS low,
                SUM(volume) AS volume
                
            FROM monthly_data
            Where symbol = ?
            AND strftime('%Y', date) = ?
        """,
        (symbol, year)

    )
    row = get_high_low_volume.fetchone()
    connection.close()

    # if data is Not Found
    if row["high"] is None:
        raise HTTPException(status_code = 404, detail = f"No data for {symbol} in {year}")

    # return as strings like assignment expects

    return{
        "high" : str(row["high"]),
        "low" : str(row["low"]),
        "volume" : str(int(row["volume"]))
    }

@router.get("/symbols/{symbol}/annual/{year}")
def get_annual(symbol: str, year: str):
    symbol = symbol.upper()

    # check the year format
    if not year.isdigit() or len(year) != 4:
        raise HTTPException(status_code = 400, detail = f"year must be in YYYY format")

    # check the database before save data to database
    if not data_exists_for_year(symbol, year):

        # fech data from API
        try:
            monthly_series = av.fetch_monthly_data(symbol)

        except ValueError as e:
            raise HTTPException(status_code = 404, detail = str(e))

        except ConnectionError as e:
            raise HTTPException(status_code = 503, detail = str(e))

        # save data
        insert_monthly_data(symbol, monthly_series)

    return get_annual_stats(symbol, year)
