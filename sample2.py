import streamlit as st
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
        star_rating_range = st.sidebar.slider("Rating", min_value=0.0, max_value=5.0, value=(0.0, 5.0))
        df = df[df['star_rating'].between(star_rating_range[0], star_rating_range[1])]

        # Filter by price
        df['price'] = df['price'].replace('[\₹,]', '', regex=True).astype(float)  
        # Clean price data
        price_range = st.sidebar.slider("Price Range", min_value=float(df['price'].min()), max_value=float(df['price'].max()), value=(float(df['price'].min()), float(df['price'].max())))
        df = df[df['price'].between(price_range[0], price_range[1])]

        st.write(f"Filtered Details", df)
    else:
        st.write("No data found or an error occurred.")

if __name__ == "__main__":
    main()
