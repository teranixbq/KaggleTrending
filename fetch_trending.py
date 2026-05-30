import os
import pandas as pd
from datetime import datetime
import kagglehub

def fetch_trending():
    print("Fetching trending datasets using kagglehub...")
    try:
        # kagglehub will automatically use KAGGLE_API_TOKEN environment variable
        # or KAGGLE_USERNAME and KAGGLE_KEY if provided.
        datasets = kagglehub.dataset_list(sort_by="hottest")
    except Exception as e:
        print(f"Error fetching datasets: {e}")
        return

    if not datasets:
        print("No trending datasets found.")
        return

    # Extract relevant data
    # Note: kagglehub returns a list of dataset objects/dictionaries
    data_list = []
    for ds in datasets:
        # Check if ds is an object with attributes or a dictionary
        if hasattr(ds, 'ref'):
            ref = ds.ref
            title = ds.title
            size = getattr(ds, 'size', 'N/A')
            lastUpdated = getattr(ds, 'lastUpdated', 'N/A')
            downloadCount = getattr(ds, 'downloadCount', 0)
            voteCount = getattr(ds, 'voteCount', 0)
        else:
            ref = ds.get('ref', '')
            title = ds.get('title', '')
            size = ds.get('size', 'N/A')
            lastUpdated = ds.get('lastUpdated', 'N/A')
            downloadCount = ds.get('downloadCount', 0)
            voteCount = ds.get('voteCount', 0)

        data_list.append({
            'ref': ref,
            'title': title,
            'size': size,
            'lastUpdated': lastUpdated,
            'downloadCount': downloadCount,
            'voteCount': voteCount,
            'url': f"https://www.kaggle.com/datasets/{ref}",
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
