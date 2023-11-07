import requests
import json
import pandas as pd

def get_uk_gov_bank_holidays():
    api_endpoint = "https://www.gov.uk/bank-holidays.json"
    api_holidays = None

    response = requests.get(api_endpoint)
    if response.status_code == 200:
        data = response.json()
        api_holidays = parse_bank_holidays(data)

    return api_holidays

def parse_bank_holidays(data):
    england_and_wales_data = data.get("england-and-wales", {})
    england_and_wales = parse_bank_holiday_division(england_and_wales_data)

    scotland_data = data.get("scotland", {})
    scotland = parse_bank_holiday_division(scotland_data)

    northern_ireland_data = data.get("northern-ireland", {})
    northern_ireland = parse_bank_holiday_division(northern_ireland_data)

    return {"EnglandAndWales": england_and_wales, "Scotland": scotland, "NorthernIreland": northern_ireland}

def parse_bank_holiday_division(division_data):
    division = division_data.get("division", "")
    events = division_data.get("events", [])
    return {"Division": division, "Events": events}

def extract_event_info(events, division):
    return [{"Division": division, "Event": event["title"], "Date": event["date"], "Notes": event["notes"], "Bunting": event["bunting"]} for event in events]

api_holidays = get_uk_gov_bank_holidays()
if api_holidays:
    # Create a list of dictionaries with "Division," "Event," "Date," "Notes," and "Bunting" for each event
    data = []
    for division, events in api_holidays.items():
        data.extend(extract_event_info(events["Events"], division))

    # Create a Pandas DataFrame
    df = pd.DataFrame(data)
    
    # Write to csv
    df.to_csv('./api/bankholidays.csv', index=False)

print("(●'◡'●")
