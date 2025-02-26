import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Global Slash-and-Burn Agriculture Map",
    layout="wide"
)

# App title and description
st.title("Global Slash-and-Burn Agriculture Prevalence")
st.markdown("""
This application visualizes the prevalence of slash-and-burn agriculture techniques across different countries.
The color scale ranges from white (not common) to dark blue (extremely common).
""")

# Sample data - Replace this with your actual data
@st.cache_data
def load_data():
    # This is example data - you'll need to replace with real data
    # Format: country code, country name, prevalence score (0-100)
    data = {
        "country_code": [
            "USA", "CAN", "MEX", "BRA", "ARG", "COL", "PER", "BOL", 
            "VEN", "CHL", "ECU", "GBR", "FRA", "DEU", "ITA", "ESP", 
            "PRT", "RUS", "CHN", "IND", "IDN", "MYS", "THA", "VNM", 
            "PHL", "AUS", "NZL", "ZAF", "NGA", "EGY", "COD", "ETH",
            "KEN", "TZA", "UGA", "GHA", "CMR", "CIV", "MDG", "MOZ"
        ],
        "country_name": [
            "United States", "Canada", "Mexico", "Brazil", "Argentina", "Colombia", "Peru", "Bolivia",
            "Venezuela", "Chile", "Ecuador", "United Kingdom", "France", "Germany", "Italy", "Spain",
            "Portugal", "Russia", "China", "India", "Indonesia", "Malaysia", "Thailand", "Vietnam",
            "Philippines", "Australia", "New Zealand", "South Africa", "Nigeria", "Egypt", "DR Congo", "Ethiopia",
            "Kenya", "Tanzania", "Uganda", "Ghana", "Cameroon", "Côte d'Ivoire", "Madagascar", "Mozambique"
        ],
        "slash_burn_prevalence": [
            5, 8, 20, 85, 15, 60, 55, 40,
            50, 10, 30, 2, 3, 2, 4, 5,
            7, 15, 25, 30, 90, 80, 65, 70,
            60, 10, 5, 40, 75, 10, 95, 80,
            70, 65, 60, 70, 75, 65, 85, 70
        ]
    }
    return pd.DataFrame(data)

# Load data
df = load_data()

# Sidebar for filters
st.sidebar.header("Filters")

# Region filter (optional)
regions = {
    "All": df["country_name"].tolist(),
    "North America": ["United States", "Canada", "Mexico"],
    "South America": ["Brazil", "Argentina", "Colombia", "Peru", "Bolivia", "Venezuela", "Chile", "Ecuador"],
    "Europe": ["United Kingdom", "France", "Germany", "Italy", "Spain", "Portugal", "Russia"],
    "Asia": ["China", "India", "Indonesia", "Malaysia", "Thailand", "Vietnam", "Philippines"],
    "Oceania": ["Australia", "New Zealand"],
    "Africa": ["South Africa", "Nigeria", "Egypt", "DR Congo", "Ethiopia", "Kenya", "Tanzania", "Uganda", "Ghana", "Cameroon", "Côte d'Ivoire", "Madagascar", "Mozambique"]
}

selected_region = st.sidebar.selectbox("Select Region", list(regions.keys()))

if selected_region != "All":
    filtered_countries = regions[selected_region]
    df_filtered = df[df["country_name"].isin(filtered_countries)]
else:
    df_filtered = df

# Prevalence threshold filter
min_prevalence = st.sidebar.slider("Minimum Prevalence", 0, 100, 0)
max_prevalence = st.sidebar.slider("Maximum Prevalence", 0, 100, 100)

df_filtered = df_filtered[
    (df_filtered["slash_burn_prevalence"] >= min_prevalence) & 
    (df_filtered["slash_burn_prevalence"] <= max_prevalence)
]

# Create the map
fig = px.choropleth(
    df_filtered, 
    locations="country_code",
    color="slash_burn_prevalence",
    hover_name="country_name",
    color_continuous_scale=[[0, "white"], [1, "darkblue"]],
    range_color=[0, 100],
    labels={"slash_burn_prevalence": "Prevalence (%)"},
    title="Slash-and-Burn Agriculture Prevalence by Country"
)

# Update layout
fig.update_layout(
    margin={"r": 0, "t": 30, "l": 0, "b": 0},
    coloraxis_colorbar=dict(
        title="Prevalence",
        tickvals=[0, 25, 50, 75, 100],
        ticktext=["Not Common", "Low", "Moderate", "High", "Very Common"]
    )
)

# Display the map
st.plotly_chart(fig, use_container_width=True)

# Add some information about the data
st.subheader("About the Data")
st.info("""
This is a demonstration using sample data. For a production application, you should:
1. Replace the sample data with real prevalence data on slash-and-burn agriculture
2. Consider using ISO country codes instead of custom codes
3. Add proper data attribution and sources
""")

# Add download capability
if st.checkbox("Show raw data"):
    st.write(df_filtered)
    csv = df_filtered.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name="slash_burn_data.csv",
        mime="text/csv"
    )

# Add methodology information
st.sidebar.markdown("---")
st.sidebar.subheader("Methodology")
st.sidebar.write("""
The prevalence score (0-100) represents the estimated percentage of 
agricultural land in each country that uses slash-and-burn techniques.
""")
