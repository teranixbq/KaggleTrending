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
        
        # List datasets with tag 'trendingDataset' sorted by 'hottest'
        # 'hottest' is the API equivalent for Trending/Popularity-over-time
        datasets = api.dataset_list(tag_ids='trendingDataset', sort_by='hottest')
    except Exception as e:
        print(f"Error authenticating or fetching datasets: {e}")
        return

    if not datasets:
        print("No trending datasets found.")
        return

    # Extract relevant data
    data_list = []
    for ds in datasets:
        # Helper to convert bytes to human readable format
        total_bytes = getattr(ds, 'totalBytes', 0)
        if total_bytes:
            if total_bytes < 1024:
                size_str = f"{total_bytes} B"
            elif total_bytes < 1024**2:
                size_str = f"{total_bytes/1024:.1f} KB"
            elif total_bytes < 1024**3:
                size_str = f"{total_bytes/1024**2:.1f} MB"
            else:
                size_str = f"{total_bytes/1024**3:.1f} GB"
        else:
            size_str = "N/A"

        data_list.append({
            'ref': getattr(ds, 'ref', ''),
            'title': getattr(ds, 'title', '').strip(),
            'size': size_str,
            'lastUpdated': getattr(ds, 'lastUpdated', 'N/A'),
            'downloadCount': int(getattr(ds, 'downloadCount', 0)),
            'voteCount': int(getattr(ds, 'voteCount', 0)),
            'viewCount': int(getattr(ds, 'viewCount', 0)),
            'ownerName': getattr(ds, 'ownerName', 'N/A'),
            'kernelCount': int(getattr(ds, 'kernelCount', 0)),
            'url': getattr(ds, 'url', f"https://www.kaggle.com/datasets/{getattr(ds, 'ref', '')}"),
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
