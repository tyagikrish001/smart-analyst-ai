import pandas as pd
import os
import matplotlib.pyplot as plt


print(os.getcwd())

def load_data():
    df = pd.read_csv("C:/Users/krish tyagi/smart-analyst-ai/data/sales.csv", quotechar='"')
    return df

def basic_stats(df):
    total_sales = df["Sales"].sum()
    avg_sales = df["Sales"].mean()
    max_sales = df["Sales"].max()
    min_sales = df["Sales"].min()

    print("Total Sales:", total_sales)
    print("Average Sales:", avg_sales)
    print("Max Sales:", max_sales)
    print("Min Sales:", min_sales)

def region_analysis(df):
    region_sales = df.groupby("Region")["Sales"].sum()

    print("\nsales by Region:")
    print(region_sales)

def sales_trend(df):

    df["Date"] = pd.to_datetime(df["Date"])
    trend = df.groupby("Date")["Sales"].sum()

    # 👇 clean date format
    trend.index = trend.index.strftime('%d-%b')

    plt.figure(figsize=(8,5))
    plt.plot(trend.index, trend.values, marker='o')

    plt.title("Sales Trend")
    plt.xlabel("Date")
    plt.ylabel("Sales")

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()

def generate_insights(df):
    df["Date"] = pd.to_datetime(df["Date"])
    trend = df.groupby("Date")["Sales"].sum()

    print("\nInsights:")

    if trend.iloc[-1] < trend.iloc[0]:
        print("- Sales overall decrease ho rahi hai")

    lowest_day = trend.idxmin()
    print(f"- Lowest sales on: {lowest_day.date()}")

    highest_day = trend.idxmax()
    print(f"- Highest sales on: {highest_day.date()}")

def generate_recommendations(df):
    df["Date"] = pd.to_datetime(df["Date"])
    trend = df.groupby("Date")["Sales"].sum()

    print("\nRecommendations:")

    # Overall trend check
    if trend.iloc[-1] < trend.iloc[0]:
        print("- Sales gir rahi hai → marketing increase karo")

    # Lowest day
    lowest_day = trend.idxmin()
    print(f"- {lowest_day.date()} pe sales lowest thi → issue investigate karo")

    # Highest day
    highest_day = trend.idxmax()
    print(f"- {highest_day.date()} pe peak sales thi → us strategy ko repeat karo")

    # Region recommendation
    region_sales = df.groupby("Region")["Sales"].sum()
    top_region = region_sales.idxmax()
    print(f"- {top_region} best perform kar raha hai → yahan invest karo")

# 👇 sab call yahan neeche
df = load_data()
print(df.head())
basic_stats(df)
region_analysis(df)
sales_trend(df)
generate_insights(df)
generate_recommendations(df)