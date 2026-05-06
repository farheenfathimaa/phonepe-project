import urllib.parse
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import sqlalchemy
import plotly.express as px
import config

# Set page configuration
st.set_page_config(page_title="PhonePe Pulse Insights", layout="wide", initial_sidebar_state="expanded")

# Initialize database connection engine
@st.cache_resource
def init_connection():
    try:
        engine = sqlalchemy.create_engine(f'mysql+mysqlconnector://{config.DB_USER}:{urllib.parse.quote_plus(config.DB_PASSWORD)}@{config.DB_HOST}/{config.DB_NAME}')
        return engine
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None

engine = init_connection()

# Execute SQL query and return DataFrame
@st.cache_data
def run_query(query):
    if engine is None:
        return pd.DataFrame()
    try:
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
            return df
    except Exception as e:
        st.error(f"Database query error: {e}")
        return pd.DataFrame()

# Sidebar Navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Transaction Analysis", "User Analysis", "Insurance Analysis", "Top Performers"],
        icons=["house", "currency-exchange", "people", "shield-check", "trophy"],
        menu_icon="cast",
        default_index=0,
    )
    
    st.markdown("---")
    st.header("Global Filters")
    # Fetch available years
    years_df = run_query("SELECT DISTINCT Year FROM Aggregated_transaction ORDER BY Year DESC")
    if not years_df.empty:
        available_years = years_df['Year'].tolist()
        available_years.insert(0, "All")
        selected_year = st.selectbox("Select Year", available_years)
    else:
        selected_year = "All"
        
    # Fetch available quarters
    quarters = ["All", 1, 2, 3, 4]
    selected_quarter = st.selectbox("Select Quarter", quarters)

# Helper function to build WHERE clause
def build_where_clause(year, quarter):
    conditions = []
    if year != "All":
        conditions.append(f"Year = {year}")
    if quarter != "All":
        conditions.append(f"Quarter = {quarter}")
        
    if conditions:
        return "WHERE " + " AND ".join(conditions)
    return ""

where_clause = build_where_clause(selected_year, selected_quarter)

# Indian states GeoJSON URL
india_geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

# Home Page
if selected == "Home":
    st.title("PhonePe Pulse Data Visualization & Exploration")
    st.markdown("""
    This interactive dashboard provides insights from the **PhonePe Pulse dataset**. 
    Navigate through the sidebar to explore different aspects:
    
    - **Transaction Analysis:** View aggregated transaction amounts and types across different states.
    - **User Analysis:** Analyze registered users and device brand distributions.
    - **Insurance Analysis:** Explore insurance purchase trends on PhonePe.
    - **Top Performers:** Discover the top states, districts, and pin codes based on volume and value.
    """)
    st.image("https://www.phonepe.com/pulse/static/images/hero-illustration.svg", use_column_width=True)

# Transaction Analysis Page
elif selected == "Transaction Analysis":
    st.title("Transaction Analysis")
    
    # KPI metrics
    kpi_query = f"SELECT SUM(Transaction_amount) as total_amt, SUM(Transaction_count) as total_count FROM Aggregated_transaction {where_clause}"
    kpi_df = run_query(kpi_query)
    
    col1, col2 = st.columns(2)
    if not kpi_df.empty and pd.notna(kpi_df['total_amt'][0]):
        col1.metric("Total Transaction Amount (₹)", f"{kpi_df['total_amt'][0]:,.2f}")
        col2.metric("Total Transaction Count", f"{int(kpi_df['total_count'][0]):,}")
        
    st.markdown("---")
    
    # 1. Bar Chart: Total amount by state
    st.subheader("Total Transaction Amount by State")
    state_trans_query = f"SELECT State, SUM(Transaction_amount) as Total_Amount FROM Aggregated_transaction {where_clause} GROUP BY State ORDER BY Total_Amount DESC"
    state_trans_df = run_query(state_trans_query)
    
    if not state_trans_df.empty:
        fig_bar = px.bar(state_trans_df, x='State', y='Total_Amount', color='State', title='Transaction Amount per State')
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Choropleth Map
        st.subheader("India Map: Transaction Amount by State")
        fig_map = px.choropleth(
            state_trans_df,
            geojson=india_geojson_url,
            featureidkey='properties.ST_NM',
            locations='State',
            color='Total_Amount',
            color_continuous_scale='Viridis',
            title='Transaction Amount Heatmap'
        )
        fig_map.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig_map, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # 2. Pie Chart: Transaction Types
        st.subheader("Transaction Types Distribution")
        type_query = f"SELECT Transaction_type, SUM(Transaction_amount) as Total_Amount FROM Aggregated_transaction {where_clause} GROUP BY Transaction_type"
        type_df = run_query(type_query)
        if not type_df.empty:
            fig_pie = px.pie(type_df, values='Total_Amount', names='Transaction_type', title='Transaction Amount by Category', hole=0.3)
            st.plotly_chart(fig_pie, use_container_width=True)
            
    with col4:
        # 3. Line Chart: Quarterly Trend
        st.subheader("Quarterly Transaction Trend")
        if selected_year == "All":
            trend_query = "SELECT Year, Quarter, SUM(Transaction_amount) as Total_Amount FROM Aggregated_transaction GROUP BY Year, Quarter ORDER BY Year, Quarter"
            trend_df = run_query(trend_query)
            if not trend_df.empty:
                trend_df['Period'] = trend_df['Year'].astype(str) + " Q" + trend_df['Quarter'].astype(str)
                fig_line = px.line(trend_df, x='Period', y='Total_Amount', markers=True, title='Trend over Time')
                st.plotly_chart(fig_line, use_container_width=True)
        else:
            trend_query = f"SELECT Quarter, SUM(Transaction_amount) as Total_Amount FROM Aggregated_transaction WHERE Year = {selected_year} GROUP BY Quarter ORDER BY Quarter"
            trend_df = run_query(trend_query)
            if not trend_df.empty:
                fig_line = px.line(trend_df, x='Quarter', y='Total_Amount', markers=True, title=f'Trend for Year {selected_year}')
                st.plotly_chart(fig_line, use_container_width=True)

# User Analysis Page
elif selected == "User Analysis":
    st.title("User Analysis")
    
    # Map Users
    st.subheader("Registered Users by State")
    user_query = f"SELECT State, SUM(Registered_users) as Total_Users FROM Map_user {where_clause} GROUP BY State ORDER BY Total_Users DESC"
    user_df = run_query(user_query)
    
    if not user_df.empty:
        fig_user_bar = px.bar(user_df, x='State', y='Total_Users', color='State', title='Total Registered Users by State')
        st.plotly_chart(fig_user_bar, use_container_width=True)
        
        # User Choropleth Map
        st.subheader("India Map: Registered Users by State")
        fig_user_map = px.choropleth(
            user_df,
            geojson=india_geojson_url,
            featureidkey='properties.ST_NM',
            locations='State',
            color='Total_Users',
            color_continuous_scale='YlGnBu',
            title='Registered Users Heatmap'
        )
        fig_user_map.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig_user_map, use_container_width=True)
        
    st.markdown("---")
    
    # Brands
    st.subheader("Device Brand Distribution")
    brand_query = f"SELECT Brand, SUM(User_count) as Total_Users FROM Aggregated_user {where_clause} GROUP BY Brand ORDER BY Total_Users DESC LIMIT 15"
    brand_df = run_query(brand_query)
    
    if not brand_df.empty:
        fig_brand = px.pie(brand_df, values='Total_Users', names='Brand', title='Top Device Brands Used', hole=0.4)
        st.plotly_chart(fig_brand, use_container_width=True)

# Insurance Analysis Page
elif selected == "Insurance Analysis":
    st.title("Insurance Analysis")
    
    st.subheader("Total Insurance Amount by State")
    ins_query = f"SELECT State, SUM(Insurance_amount) as Total_Amount FROM Aggregated_insurance {where_clause} GROUP BY State ORDER BY Total_Amount DESC"
    ins_df = run_query(ins_query)
    
    if not ins_df.empty:
        fig_ins_bar = px.bar(ins_df, x='State', y='Total_Amount', color='State', title='Insurance Amount by State')
        st.plotly_chart(fig_ins_bar, use_container_width=True)
        
        # Insurance Types
        st.subheader("Insurance Amount by Category")
        type_ins_query = f"SELECT Insurance_type, SUM(Insurance_amount) as Total_Amount FROM Aggregated_insurance {where_clause} GROUP BY Insurance_type"
        type_ins_df = run_query(type_ins_query)
        if not type_ins_df.empty:
            fig_ins_pie = px.pie(type_ins_df, values='Total_Amount', names='Insurance_type', title='Insurance Type Distribution')
            st.plotly_chart(fig_ins_pie, use_container_width=True)

# Top Performers Page
elif selected == "Top Performers":
    st.title("Top Performers")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Top 10 States")
        top_states_query = f"SELECT State, SUM(Transaction_amount) as Total_Amount FROM Top_transaction {where_clause} GROUP BY State ORDER BY Total_Amount DESC LIMIT 10"
        top_states_df = run_query(top_states_query)
        if not top_states_df.empty:
            st.dataframe(top_states_df, hide_index=True)
            fig_ts = px.bar(top_states_df, x='State', y='Total_Amount', title="Top States")
            st.plotly_chart(fig_ts, use_container_width=True)
            
    with col2:
        st.subheader("Top 10 Districts")
        top_dist_query = f"SELECT District, SUM(Transaction_amount) as Total_Amount FROM Map_transaction {where_clause} GROUP BY District ORDER BY Total_Amount DESC LIMIT 10"
        top_dist_df = run_query(top_dist_query)
        if not top_dist_df.empty:
            st.dataframe(top_dist_df, hide_index=True)
            fig_td = px.bar(top_dist_df, x='District', y='Total_Amount', title="Top Districts")
            st.plotly_chart(fig_td, use_container_width=True)
            
    with col3:
        st.subheader("Top 10 Pin Codes")
        top_pin_query = f"SELECT Pincode, SUM(Transaction_amount) as Total_Amount FROM Top_transaction {where_clause} GROUP BY Pincode ORDER BY Total_Amount DESC LIMIT 10"
        top_pin_df = run_query(top_pin_query)
        if not top_pin_df.empty:
            st.dataframe(top_pin_df, hide_index=True)
            # Ensure Pincode is treated as string/categorical for visualization
            top_pin_df['Pincode'] = top_pin_df['Pincode'].astype(str)
            fig_tp = px.bar(top_pin_df, x='Pincode', y='Total_Amount', title="Top Pin Codes")
            st.plotly_chart(fig_tp, use_container_width=True)
