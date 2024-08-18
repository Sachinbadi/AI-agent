from DataColl import DataCollectionAgent
from AnalysisReport import AnalysisReportingAgent

def get_keywords_from_user():
    keywords = []
    print("Enter keywords (one per line). Press Enter twice to finish:")
    while True:
        keyword = input().strip()
        if keyword:
            keywords.append(keyword)
        else:
            break
    return keywords

def run_data_collection_and_report():
    keywords = get_keywords_from_user()

    if not keywords:
        print("No keywords entered. Exiting.")
        return

    print(f"Collecting data for keywords: {', '.join(keywords)}")

    # Collect data
    data_agent = DataCollectionAgent(keywords)
    data_agent.fetch_data()
    data_agent.close_connection()

    # Generate report
    openai_api_key = "YOUR OPENAI API KEY "
    agent = AnalysisReportingAgent(openai_api_key)
    data = agent.analyze_data( )
    agent.generate_report(data)
    agent.close_connection()

    print("Data collection and report generation complete.")

def main():
    while True:
        print("\nGoogle Trends Reporter")
        print("1. Collect Data and Generate Report")
        print("2. Exit")

        choice = input("Enter your choice (1-2): ")

        if choice == '1':
            run_data_collection_and_report()
        elif choice == '2':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()