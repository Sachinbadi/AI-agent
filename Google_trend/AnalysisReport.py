import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime, timedelta
import numpy as np
from openai import OpenAI

class AnalysisReportingAgent:
    def __init__(self, openai_api_key):
        self.db_connection = sqlite3.connect('trends_data.db')
        self.client = OpenAI(api_key=openai_api_key)

    def analyze_data(self):
        query = "SELECT * FROM trends"
        df = pd.read_sql_query(query, self.db_connection, parse_dates=['date'])
        df.set_index('date', inplace=True)
        return df

    def generate_report(self, data):
        # Generate graph
        plt.figure(figsize=(10, 6))
        for column in data.columns:
            plt.plot(data.index, data[column], label=column)
        plt.title('Trend Analysis (Last 7 Days)')
        plt.xlabel('Date')
        plt.ylabel('Relative Interest')
        plt.legend()
        plt.savefig('trend_report.png')
        plt.close()

        # Prepare data summary for OpenAI
        summary = "Trend data summary:\n"
        for column in data.columns:
            summary += f"\nKeyword: {column}\n"
            summary += f"Average interest: {data[column].mean():.2f}\n"
            summary += f"Minimum interest: {data[column].min():.2f}\n"
            summary += f"Maximum interest: {data[column].max():.2f}\n"
            trend = np.polyfit(range(len(data)), data[column], 1)
            trend_direction = "Upward" if trend[0] > 0 else "Downward" if trend[0] < 0 else "Stable"
            summary += f"Overall trend: {trend_direction}\n"
            peak_day = data[column].idxmax().strftime('%Y-%m-%d')
            summary += f"Peak interest day: {peak_day}\n"

        # Generate report using OpenAI
        prompt = f"""Based on the following trend data summary, provide a detailed analysis report. 
        Include insights on trends, comparisons between keywords, potential reasons for changes, and recommendations.

        {summary}

        Please structure the report with the following sections:
        1. Executive Summary
        2. Detailed Analysis for Each Keyword
        3. Comparative Analysis
        4. Insights and Recommendations
        """

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a data analyst specializing in trend analysis."},
                {"role": "user", "content": prompt}
            ]
        )

        report = response.choices[0].message.content

        # Save report to file
        with open('trend_analysis_report.txt', 'w') as f:
            f.write(f"Trend Analysis Report\nGenerated at: {datetime.now()}\n\n")
            f.write(report)

        print(f"Report generated at {datetime.now()}")


    def close_connection(self):
        self.db_connection.close()