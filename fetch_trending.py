import os
import pandas as pd
from datetime import datetime
from kaggle.api.kaggle_api_extended import KaggleApi

def fetch_trending():
    print("Fetching trending datasets using Kaggle API...")
    try:
        # The library will look for KAGGLE_USERNAME and KAGGLE_KEY
        # OR KAGGLE_API_TOKEN environment variables.
        api = KaggleApi()
        api.authenticate()
        
        # List trending (hottest) datasets
        datasets = api.dataset_list(sort_by='hottest')
    except Exception as e:
        print(f"Error fetching datasets: {e}")
        return

    if not datasets:
        print("No trending datasets found.")
        return

    # Extract relevant data
    data_list = []
    for ds in datasets:
        data_list.append({
            'ref': ds.ref,
            'title': ds.title,
            'size': ds.size,
            'lastUpdated': ds.lastUpdated,
            'downloadCount': ds.downloadCount,
            'voteCount': ds.voteCount,
            'usabilityRating': ds.usabilityRating,
            'url': f"https://www.kaggle.com/datasets/{ds.ref}",
            'fetch_date': datetime.now().isoformat()
        })

    # Create DataFrame
    df = pd.DataFrame(data_list)

    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)

    # Generate filename with date
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"data/trending_{date_str}.csv"

    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"Successfully saved {len(df)} datasets to {filename}")

if __name__ == "__main__":
    fetch_trending()
