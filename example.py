import streamlit as st
import subprocess
import sys

# Function to print installed packages
def print_installed_packages():
    result = subprocess.run([sys.executable, "-m", "pip", "freeze"], stdout=subprocess.PIPE)
    st.text(result.stdout.decode('utf-8'))

print_installed_packages()

import pandas as pd
from sqlalchemy import create_engine
import psycopg2
from psycopg2 import sql

# Database connection details
db_user = 'postgres'
db_password = 'password'
db_host = 'localhost'
db_port = '5432'
db_name = 'bus_details'

# Create a connection string for SQLAlchemy
connection_string = f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

# Function to get data from PostgreSQL
def get_data_from_postgres():
    engine = create_engine(connection_string)
    query = "SELECT * FROM bus_data"
    df = pd.read_sql(query, engine)
    return df

# Streamlit application
def main():
    st.title("Bus Details")

    # Load data from PostgreSQL
    df = get_data_from_postgres()

    if df is not None and not df.empty:
        st.write("Current List", df)

        # Filter options
        st.sidebar.header("Filter Options")

        # Filter by route name
        unique_route_names = df['route_name'].unique()
        selected_route_name = st.sidebar.selectbox("Route Name", ["All"] + list(unique_route_names))
        
        if selected_route_name != "All":
            df = df[df['route_name'] == selected_route_name]

        # Filter by bus type
        unique_bus_types = df['bus_type'].unique()
        selected_bus_type = st.sidebar.selectbox("Bus Type", ["All"] + list(unique_bus_types))
        
        if selected_bus_type != "All":
            df = df[df['bus_type'] == selected_bus_type]

        # Filter by star rating
        if 'star_rating' in df.columns:
            star_ratings = df['star_rating'].dropna().unique()
            star_ratings = sorted(set(star_ratings))  # Ensure unique and sorted values
            star_ratings = [round(rating, 1) for rating in star_ratings]  # Round to one decimal place
            selected_star_rating = st.sidebar.selectbox("Star Rating", ["All"] + star_ratings)
            
            if selected_star_rating != "All":
                df = df[df['star_rating'] == selected_star_rating]
        else:
            st.warning("Star rating data is not available.")

        # Filter by price
        if 'price' in df.columns:
            # Clean and convert price data
            df['price'] = df['price'].replace('[\₹,]', '', regex=True)
            df['price'] = pd.to_numeric(df['price'], errors='coerce')  # Convert to numeric, set errors to 'coerce'
            df = df.dropna(subset=['price'])  # Drop rows where price is NaN
            
            # Create dropdown options for price ranges
            price_options = sorted(df['price'].unique())
            selected_price = st.sidebar.selectbox("Price", ["All"] + price_options)
            
            if selected_price != "All":
                df = df[df['price'] == selected_price]
        else:
            st.warning("Price data is not available.")

        st.write("Filtered Details", df)
    else:
        st.write("No data found or an error occurred.")

if __name__ == "__main__":
    main()
