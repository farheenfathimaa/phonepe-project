import os
import json
import pandas as pd
from pathlib import Path
from git.repo.base import Repo
import sqlalchemy
from sqlalchemy import create_engine
import mysql.connector

# Import database credentials from config
try:
    import config
except ImportError:
    print("Error: config.py not found. Please create config.py with DB_HOST, DB_USER, DB_PASSWORD, DB_NAME.")
    exit(1)

# Configuration
GITHUB_REPO_URL = "https://github.com/PhonePe/pulse"
CLONE_DIR = "pulse"

def clone_repo():
    """Clones the PhonePe Pulse repository if it doesn't already exist."""
    if not os.path.exists(CLONE_DIR):
        print(f"Cloning {GITHUB_REPO_URL} into {CLONE_DIR}...")
        try:
            Repo.clone_from(GITHUB_REPO_URL, CLONE_DIR)
            print("Repository cloned successfully.")
        except Exception as e:
            print(f"Error cloning repository: {e}")
    else:
        print(f"Directory '{CLONE_DIR}' already exists. Skipping clone.")

def extract_aggregated_transaction():
    """Extracts data from aggregated/transaction directory into a pandas DataFrame."""
    path = Path(CLONE_DIR, "data", "aggregated", "transaction", "country", "india", "state")
    data = []
    
    if not path.exists():
        print(f"Path not found: {path}")
        return pd.DataFrame()
        
    for state in os.listdir(path):
        state_path = path / state
        if not state_path.is_dir(): continue
        for year in os.listdir(state_path):
            year_path = state_path / year
            if not year_path.is_dir(): continue
            for file in os.listdir(year_path):
                if file.endswith('.json'):
                    file_path = year_path / file
                    with open(file_path, 'r') as f:
                        content = json.load(f)
                        quarter = int(file.replace('.json', ''))
                        
                        if content['data'] and content['data']['transactionData']:
                            for item in content['data']['transactionData']:
                                data.append({
                                    'State': state,
                                    'Year': int(year),
                                    'Quarter': quarter,
                                    'Transaction_type': item['name'],
                                    'Transaction_count': item['paymentInstruments'][0]['count'],
                                    'Transaction_amount': item['paymentInstruments'][0]['amount']
                                })
    return pd.DataFrame(data)

def extract_aggregated_user():
    """Extracts data from aggregated/user directory into a pandas DataFrame."""
    path = Path(CLONE_DIR, "data", "aggregated", "user", "country", "india", "state")
    data = []
    
    if not path.exists(): return pd.DataFrame()
    
    for state in os.listdir(path):
        state_path = path / state
        if not state_path.is_dir(): continue
        for year in os.listdir(state_path):
            year_path = state_path / year
            if not year_path.is_dir(): continue
            for file in os.listdir(year_path):
                if file.endswith('.json'):
                    file_path = year_path / file
                    with open(file_path, 'r') as f:
                        content = json.load(f)
                        quarter = int(file.replace('.json', ''))
                        
                        if content['data'] and content['data']['usersByDevice']:
                            for item in content['data']['usersByDevice']:
                                data.append({
                                    'State': state,
                                    'Year': int(year),
                                    'Quarter': quarter,
                                    'Brand': item['brand'],
                                    'User_count': item['count'],
                                    'User_percentage': item['percentage']
                                })
    return pd.DataFrame(data)

def extract_aggregated_insurance():
    """Extracts data from aggregated/insurance directory into a pandas DataFrame."""
    path = Path(CLONE_DIR, "data", "aggregated", "insurance", "country", "india", "state")
    data = []
    
    if not path.exists(): return pd.DataFrame()
    
    for state in os.listdir(path):
        state_path = path / state
        if not state_path.is_dir(): continue
        for year in os.listdir(state_path):
            year_path = state_path / year
            if not year_path.is_dir(): continue
            for file in os.listdir(year_path):
                if file.endswith('.json'):
                    file_path = year_path / file
                    with open(file_path, 'r') as f:
                        content = json.load(f)
                        quarter = int(file.replace('.json', ''))
                        
                        if content['data'] and content['data']['transactionData']:
                            for item in content['data']['transactionData']:
                                data.append({
                                    'State': state,
                                    'Year': int(year),
                                    'Quarter': quarter,
                                    'Insurance_type': item['name'],
                                    'Insurance_count': item['paymentInstruments'][0]['count'],
                                    'Insurance_amount': item['paymentInstruments'][0]['amount']
                                })
    return pd.DataFrame(data)

def extract_map_transaction():
    """Extracts data from map/transaction directory into a pandas DataFrame."""
    path = Path(CLONE_DIR, "data", "map", "transaction", "hover", "country", "india", "state")
    data = []
    
    if not path.exists(): return pd.DataFrame()
    
    for state in os.listdir(path):
        state_path = path / state
        if not state_path.is_dir(): continue
        for year in os.listdir(state_path):
            year_path = state_path / year
            if not year_path.is_dir(): continue
            for file in os.listdir(year_path):
                if file.endswith('.json'):
                    file_path = year_path / file
                    with open(file_path, 'r') as f:
                        content = json.load(f)
                        quarter = int(file.replace('.json', ''))
                        
                        if content['data'] and content['data']['hoverDataList']:
                            for item in content['data']['hoverDataList']:
                                data.append({
                                    'State': state,
                                    'Year': int(year),
                                    'Quarter': quarter,
                                    'District': item['name'],
                                    'Transaction_count': item['metric'][0]['count'],
                                    'Transaction_amount': item['metric'][0]['amount']
                                })
    return pd.DataFrame(data)

def extract_map_user():
    """Extracts data from map/user directory into a pandas DataFrame."""
    path = Path(CLONE_DIR, "data", "map", "user", "hover", "country", "india", "state")
    data = []
    
    if not path.exists(): return pd.DataFrame()
    
    for state in os.listdir(path):
        state_path = path / state
        if not state_path.is_dir(): continue
        for year in os.listdir(state_path):
            year_path = state_path / year
            if not year_path.is_dir(): continue
            for file in os.listdir(year_path):
                if file.endswith('.json'):
                    file_path = year_path / file
                    with open(file_path, 'r') as f:
                        content = json.load(f)
                        quarter = int(file.replace('.json', ''))
                        
                        if content['data'] and content['data']['hoverData']:
                            for district, info in content['data']['hoverData'].items():
                                data.append({
                                    'State': state,
                                    'Year': int(year),
                                    'Quarter': quarter,
                                    'District': district,
                                    'Registered_users': info['registeredUsers'],
                                    'App_opens': info['appOpens']
                                })
    return pd.DataFrame(data)

def extract_map_insurance():
    """Extracts data from map/insurance directory into a pandas DataFrame."""
    path = Path(CLONE_DIR, "data", "map", "insurance", "hover", "country", "india", "state")
    data = []
    
    if not path.exists(): return pd.DataFrame()
    
    for state in os.listdir(path):
        state_path = path / state
        if not state_path.is_dir(): continue
        for year in os.listdir(state_path):
            year_path = state_path / year
            if not year_path.is_dir(): continue
            for file in os.listdir(year_path):
                if file.endswith('.json'):
                    file_path = year_path / file
                    with open(file_path, 'r') as f:
                        content = json.load(f)
                        quarter = int(file.replace('.json', ''))
                        
                        if content['data'] and content['data']['hoverDataList']:
                            for item in content['data']['hoverDataList']:
                                data.append({
                                    'State': state,
                                    'Year': int(year),
                                    'Quarter': quarter,
                                    'District': item['name'],
                                    'Insurance_count': item['metric'][0]['count'],
                                    'Insurance_amount': item['metric'][0]['amount']
                                })
    return pd.DataFrame(data)

def extract_top_transaction():
    """Extracts data from top/transaction directory into a pandas DataFrame."""
    path = Path(CLONE_DIR, "data", "top", "transaction", "country", "india", "state")
    data = []
    
    if not path.exists(): return pd.DataFrame()
    
    for state in os.listdir(path):
        state_path = path / state
        if not state_path.is_dir(): continue
        for year in os.listdir(state_path):
            year_path = state_path / year
            if not year_path.is_dir(): continue
            for file in os.listdir(year_path):
                if file.endswith('.json'):
                    file_path = year_path / file
                    with open(file_path, 'r') as f:
                        content = json.load(f)
                        quarter = int(file.replace('.json', ''))
                        
                        if content['data'] and content['data']['pincodes']:
                            for item in content['data']['pincodes']:
                                data.append({
                                    'State': state,
                                    'Year': int(year),
                                    'Quarter': quarter,
                                    'Pincode': item['entityName'],
                                    'Transaction_count': item['metric']['count'],
                                    'Transaction_amount': item['metric']['amount']
                                })
    return pd.DataFrame(data)

def extract_top_user():
    """Extracts data from top/user directory into a pandas DataFrame."""
    path = Path(CLONE_DIR, "data", "top", "user", "country", "india", "state")
    data = []
    
    if not path.exists(): return pd.DataFrame()
    
    for state in os.listdir(path):
        state_path = path / state
        if not state_path.is_dir(): continue
        for year in os.listdir(state_path):
            year_path = state_path / year
            if not year_path.is_dir(): continue
            for file in os.listdir(year_path):
                if file.endswith('.json'):
                    file_path = year_path / file
                    with open(file_path, 'r') as f:
                        content = json.load(f)
                        quarter = int(file.replace('.json', ''))
                        
                        if content['data'] and content['data']['pincodes']:
                            for item in content['data']['pincodes']:
                                data.append({
                                    'State': state,
                                    'Year': int(year),
                                    'Quarter': quarter,
                                    'Pincode': item['name'],
                                    'Registered_users': item['registeredUsers']
                                })
    return pd.DataFrame(data)

def extract_top_insurance():
    """Extracts data from top/insurance directory into a pandas DataFrame."""
    path = Path(CLONE_DIR, "data", "top", "insurance", "country", "india", "state")
    data = []
    
    if not path.exists(): return pd.DataFrame()
    
    for state in os.listdir(path):
        state_path = path / state
        if not state_path.is_dir(): continue
        for year in os.listdir(state_path):
            year_path = state_path / year
            if not year_path.is_dir(): continue
            for file in os.listdir(year_path):
                if file.endswith('.json'):
                    file_path = year_path / file
                    with open(file_path, 'r') as f:
                        content = json.load(f)
                        quarter = int(file.replace('.json', ''))
                        
                        if content['data'] and content['data']['pincodes']:
                            for item in content['data']['pincodes']:
                                data.append({
                                    'State': state,
                                    'Year': int(year),
                                    'Quarter': quarter,
                                    'Pincode': item['entityName'],
                                    'Insurance_count': item['metric']['count'],
                                    'Insurance_amount': item['metric']['amount']
                                })
    return pd.DataFrame(data)


def load_to_mysql(dataframes_dict):
    """Loads all dataframes into MySQL database."""
    print("Connecting to MySQL Database...")
    try:
        # Create engine
        engine = create_engine(f'mysql+mysqlconnector://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_NAME}')
        
        for table_name, df in dataframes_dict.items():
            if df is not None and not df.empty:
                print(f"Loading data into table {table_name}...")
                df.to_sql(table_name, con=engine, if_exists='append', index=False)
                print(f"Successfully loaded {len(df)} rows into {table_name}.")
            else:
                print(f"Warning: DataFrame for {table_name} is empty. Skipping.")
                
    except Exception as e:
        print(f"Error loading to MySQL: {e}")

def clean_state_names(df):
    """Helper function to clean up state names."""
    if 'State' in df.columns:
        df['State'] = df['State'].str.replace('-', ' ').str.title()
        # Handle specific edge cases to match standard names
        df['State'] = df['State'].replace({
            'Andaman & Nicobar Islands': 'Andaman & Nicobar',
            'Dadra & Nagar Haveli & Daman & Diu': 'Dadra and Nagar Haveli and Daman and Diu'
        })
    return df

def main():
    print("Starting Data Extraction Process...")
    clone_repo()
    
    print("Extracting data into Pandas DataFrames...")
    # Extracting all datasets
    df_agg_trans = clean_state_names(extract_aggregated_transaction())
    df_agg_user = clean_state_names(extract_aggregated_user())
    df_agg_ins = clean_state_names(extract_aggregated_insurance())
    
    df_map_trans = clean_state_names(extract_map_transaction())
    df_map_user = clean_state_names(extract_map_user())
    df_map_ins = clean_state_names(extract_map_insurance())
    
    df_top_trans = clean_state_names(extract_top_transaction())
    df_top_user = clean_state_names(extract_top_user())
    df_top_ins = clean_state_names(extract_top_insurance())
    
    # Dictionary mapping table names to their respective DataFrames
    dataframes = {
        'Aggregated_transaction': df_agg_trans,
        'Aggregated_user': df_agg_user,
        'Aggregated_insurance': df_agg_ins,
        'Map_transaction': df_map_trans,
        'Map_user': df_map_user,
        'Map_insurance': df_map_ins,
        'Top_transaction': df_top_trans,
        'Top_user': df_top_user,
        'Top_insurance': df_top_ins
    }
    
    # Load all to MySQL
    load_to_mysql(dataframes)
    print("Data Extraction and Loading Complete.")

if __name__ == "__main__":
    main()
