from pytrends.request import TrendReq
import sqlite3
from datetime import datetime, timedelta
import pandas as pd

class DataCollectionAgent:
    def __init__(self, keywords):
        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.keywords = keywords
        self.db_connection = sqlite3.connect('trends_data.db')

    def fetch_data(self):
        try:
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            timeframe = f'{start_date} {end_date}'

            all_data = pd.DataFrame()

            for keyword in self.keywords:
                self.pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo='', gprop='')
                data = self.pytrends.interest_over_time()
                if not data.empty:
                    data = data.drop('isPartial', axis=1)
                    data.columns = [keyword]
                    all_data = pd.concat([all_data, data], axis=1)

            if not all_data.empty:
                self.store_data(all_data)
                print(f"Data collected from {start_date} to {end_date} for keywords: {', '.join(self.keywords)}")
            else:
                print("No data collected.")

        except Exception as e:
            print(f"Error fetching data: {e}")

    def store_data(self, data):
        if not data.empty:
            # Clear existing data
            cursor = self.db_connection.cursor()
            cursor.execute("DELETE FROM trends")
            self.db_connection.commit()

            # Store new data
            data.reset_index(inplace=True)
            data.to_sql('trends', self.db_connection, if_exists='replace', index=False)
            print("Data stored successfully.")
        else:
            print("No data to store.")

    def close_connection(self):
        self.db_connection.close()