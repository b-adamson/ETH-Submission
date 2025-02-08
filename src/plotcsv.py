import pandas as pd
import matplotlib.pyplot as plt

def plot_queries_and_price(csv_file):

    # plots a graph of current csv

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file, names=["date", "queries", "bool", "price"], parse_dates=["date"])
    
    # Plotting
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Plot the number of queries
    ax1.plot(df["date"], df["queries"], color='tab:blue', label='Number of Queries')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Number of Queries', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    
    # Plot the price on the same graph with a secondary y-axis
    ax2 = ax1.twinx()
    ax2.plot(df["date"], df["price"], color='tab:red', label='Price')
    ax2.set_ylabel('Price', color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')
    
    # Add legend and grid
    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))
    plt.title("Number of Queries and Price Over Time")
    plt.grid(True)
    
    # Show the plot
    plt.show()

plot_queries_and_price("training_data/@DOGE.csv")
