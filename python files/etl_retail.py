# etl_retail.py
import pandas as pd
import sqlite3
from io import BytesIO
import requests
from datetime import datetime, timedelta

# UCI dataset URL
UCI_XLSX_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
DB_FILE = "retail_dw.db"

def download_online_retail(url=UCI_XLSX_URL):
    """Download the Online Retail dataset from UCI and load into a pandas DataFrame."""
    print("Downloading dataset from UCI...")
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    df = pd.read_excel(BytesIO(r.content))
    print(f"Downloaded {len(df)} rows")
    return df

def basic_cleaning(df):
    """Clean dataset: fix column names, drop missing CustomerID/InvoiceDate."""
    df.columns = [c.strip() for c in df.columns]
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
    df = df.dropna(subset=['InvoiceDate', 'StockCode', 'CustomerID'])
    df['CustomerID'] = df['CustomerID'].astype(int)
    return df

def transform_data(df):
    """Transform data: add TotalSales, remove invalids."""
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0).astype(int)
    df['UnitPrice'] = pd.to_numeric(df['UnitPrice'], errors='coerce').fillna(0.0)
    df['TotalSales'] = df['Quantity'] * df['UnitPrice']
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
    return df

def create_time_dim(df):
    """Create TimeDim from InvoiceDate."""
    df['InvoiceDateOnly'] = df['InvoiceDate'].dt.date
    time_df = pd.DataFrame({'InvoiceDate': df['InvoiceDateOnly'].unique()})
    time_df['Day'] = pd.to_datetime(time_df['InvoiceDate']).dt.day
    time_df['Month'] = pd.to_datetime(time_df['InvoiceDate']).dt.month
    time_df['Quarter'] = pd.to_datetime(time_df['InvoiceDate']).dt.quarter
    time_df['Year'] = pd.to_datetime(time_df['InvoiceDate']).dt.year
    time_df['WeekOfYear'] = pd.to_datetime(time_df['InvoiceDate']).dt.isocalendar().week
    time_df = time_df.sort_values('InvoiceDate').reset_index(drop=True)
    time_df['TimeID'] = time_df.index + 1
    return time_df

def load_to_sqlite(df, db_path=DB_FILE):
    """Load all four tables into SQLite."""
    conn = sqlite3.connect(db_path)

    # CustomerDim
    customer_dim = df[['CustomerID', 'Country']].drop_duplicates()
    customer_dim['CustomerName'] = None
    customer_dim.to_sql('CustomerDim', conn, if_exists='replace', index=False)

    # ProductDim
    product_dim = df[['StockCode', 'Description']].drop_duplicates()
    product_dim['Category'] = None
    product_dim.to_sql('ProductDim', conn, if_exists='replace', index=False)

    # TimeDim
    time_dim = create_time_dim(df)
    time_dim[['TimeID', 'InvoiceDate', 'Day', 'Month', 'Quarter', 'Year', 'WeekOfYear']].to_sql(
        'TimeDim', conn, if_exists='replace', index=False
    )

    # Map TimeID into SalesFact
    df['InvoiceDateOnly'] = df['InvoiceDate'].dt.date
    time_map = dict(zip(time_dim['InvoiceDate'], time_dim['TimeID']))
    df['TimeID'] = df['InvoiceDateOnly'].map(time_map)

    # SalesFact
    sales_fact = df[['InvoiceNo', 'StockCode', 'CustomerID', 'TimeID', 'Quantity', 'UnitPrice', 'TotalSales', 'Country']]
    sales_fact.to_sql('SalesFact', conn, if_exists='replace', index=False)

    conn.close()
    print(f"Data loaded into {db_path} successfully.")

def run_etl():
    df_raw = download_online_retail()
    df_clean = basic_cleaning(df_raw)
    df_trans = transform_data(df_clean)
    load_to_sqlite(df_trans)

if __name__ == "__main__":
    run_etl()
