import os
import pandas as pd
from datetime import datetime
from kaggle.api.kaggle_api_extended import KaggleApi

def fetch_trending():
    print("Fetching trending datasets using Kaggle API...")
    try:
        # Authenticate using KAGGLE_USERNAME and KAGGLE_KEY environment variables
        api = KaggleApi()
        api.authenticate()
        
        # List datasets with tag 'trendingDataset' sorted by 'active'
        # to match https://www.kaggle.com/datasets?topic=trendingDataset&sort=active
        datasets = api.dataset_list(tag_ids='trendingDataset', sort_by='active')
    except Exception as e:
        print(f"Error authenticating or fetching datasets: {e}")
        return

    if not datasets:
        print("No trending datasets found.")
        return

    # Extract relevant data
    data_list = []
    for ds in datasets:
        # The ApiDataset object has specific attribute names
        # ref, title, size, lastUpdated, downloadCount, voteCount, usabilityRating
        # Using getattr to be safe
        data_list.append({
            'ref': getattr(ds, 'ref', ''),
            'title': getattr(ds, 'title', ''),
            'size': getattr(ds, 'size', 'N/A'),
            'lastUpdated': str(getattr(ds, 'lastUpdated', 'N/A')),
            'downloadCount': getattr(ds, 'downloadCount', 0),
            'voteCount': getattr(ds, 'voteCount', 0),
            'usabilityRating': getattr(ds, 'usabilityRating', 0),
            'url': f"https://www.kaggle.com/datasets/{getattr(ds, 'ref', '')}",
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
