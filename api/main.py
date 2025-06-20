from fastapi import FastAPI,HTTPException
import requests
# start the fastapi app

app=FastAPI()

# define the url to fetch data from it 

THE_URL="https://data.messari.io/api/v1/assets/btc/metrics"

# Create an endpoint to fetch from it 

@app.get("/btc-metrics")
def get_btc_metrics():
    """ Fetches the Bitcoin Metrics and returns the json response """
    try:
        response=requests.get(THE_URL)
        response.raise_for_status() # Raise an error if requesting goes wrong
        data=response.json()["data"]
        # the data is not cleaned we should just extract the relevant fields
        cleaned = {
        "symbol": data["symbol"],
        "name": data["name"],
        "price_usd": round(data["market_data"]["price_usd"], 2),
        "volume_24h": round(data["market_data"]["volume_last_24_hours"], 2),
        "market_cap_usd": round(data["marketcap"]["current_marketcap_usd"], 2),
        "change_24h_percent": round(data["market_data"]["percent_change_usd_last_24_hours"], 3),
        "ath_price": round(data["all_time_high"]["price"], 2),
        "ath_date": data["all_time_high"]["at"],
        "cycle_low_price": round(data["cycle_low"]["price"], 2),
        "cycle_low_date": data["cycle_low"]["at"],
        "timestamp": response.json()["status"]["timestamp"]
        }
        # return the cleaned json response
        return cleaned
    except Exception as e:
        # Return a 500 error if something goes wrong while requesting
        raise HTTPException(status_code=500,detail=str(e))