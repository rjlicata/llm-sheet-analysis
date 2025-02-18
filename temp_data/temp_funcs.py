
import pandas as pd
import matplotlib.pyplot as plt

def func(data):
    # Group the data by city and create a scatter plot of price vs square footage
    fig, ax = plt.subplots(figsize=(10, 8))
    for city in data['City'].unique():
        city_data = data[data['City'] == city]
        ax.scatter(city_data['Square Footage'], city_data['Price'], label=city)
    
    # Set the title and labels
    ax.set_title('Home Price vs Square Footage by City')
    ax.set_xlabel('Square Footage')
    ax.set_ylabel('Price')
    
    # Add a legend
    ax.legend()
    
    # Save the figure to a file
    plt.savefig('figures/output.png')
    
    # Close the figure before returning
    plt.close()
    
    return None
