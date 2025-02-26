import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Biodiversity and Slash-and-Burn Agriculture",
    layout="wide"
)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Map", "About", "Environmental Effects", "Sustainable Solutions", "Implementation", "SDG Alignment"])

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

# MAP PAGE
if page == "Map":
    st.title("Global Slash-and-Burn Agriculture Prevalence")
    st.markdown("""
    This application visualizes the prevalence of slash-and-burn agriculture techniques across different countries.
    The color scale ranges from white (not common) to dark blue (extremely common).
    """)
    
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
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.subheader("Filters")
        selected_region = st.selectbox("Select Region", list(regions.keys()))
        
        if selected_region != "All":
            filtered_countries = regions[selected_region]
            df_filtered = df[df["country_name"].isin(filtered_countries)]
        else:
            df_filtered = df
        
        # Prevalence threshold filter
        min_prevalence = st.slider("Minimum Prevalence", 0, 100, 0)
        max_prevalence = st.slider("Maximum Prevalence", 0, 100, 100)
        
        df_filtered = df_filtered[
            (df_filtered["slash_burn_prevalence"] >= min_prevalence) & 
            (df_filtered["slash_burn_prevalence"] <= max_prevalence)
        ]
    
    with col1:
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

# ABOUT PAGE
elif page == "About":
    st.title("Biodiversity and Agriculture")
    
    st.header("Introduction and Overview")
    st.markdown("""
    Biodiversity refers to the variety of life on Earth, encompassing all species of plants, animals, fungi, and microorganisms, as well as the ecosystems they form. It plays a crucial role in maintaining ecological balance by supporting essential processes such as pollination, nutrient cycling, and climate regulation. A rich biodiversity ensures ecosystem resilience, allowing nature to adapt to changes and disturbances.

    Agriculture, the practice of cultivating soil, growing crops, and raising livestock, provides food, fiber, and other essential resources for human survival. It has been a fundamental part of civilization for thousands of years, evolving from traditional farming methods to modern, technology-driven agricultural systems. Advances in irrigation, fertilizers, and genetically modified crops have significantly increased food production, helping to sustain a growing global population. However, agricultural expansion and certain farming practices, such as slash-and-burn, can negatively impact biodiversity and the environment.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("What is Slash-and-Burn Agriculture?")
        st.markdown("""
        Slash-and-burn agriculture is a traditional farming method where:
        - Forests or grasslands are cleared by cutting down vegetation
        - The cleared biomass is then burned
        - Crops are planted in the ash-fertilized soil
        - Land is abandoned after a few years when soil fertility declines
        - New land is cleared, continuing the cycle
        """)
    
    with col2:
        st.subheader("Global Impact")
        st.markdown("""
        This practice is most common in:
        - Tropical regions of South America (especially Brazil)
        - Southeast Asia (Indonesia, Malaysia, Thailand)
        - Central Africa (DR Congo, Madagascar)
        
        It accounts for an estimated 5% of global deforestation annually.
        """)

# ENVIRONMENTAL EFFECTS PAGE
elif page == "Environmental Effects":
    st.title("Environmental Effects of Slash-and-Burn Agriculture")
    
    st.markdown("""
    Slash-and-burn agriculture is a traditional farming practice where forests or grasslands are cleared by cutting down vegetation and then burning the biomass. While it quickly clears land for farming, this method also has several negative environmental impacts:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Deforestation and Habitat Loss")
        st.markdown("""
        - Destruction of forests reduces biodiversity
        - Disrupts ecosystems and food chains
        - Threatens countless species of plants and animals
        - Creates forest fragmentation
        - Reduces wildlife corridors
        """)
        
        st.subheader("Soil Degradation")
        st.markdown("""
        - Initial burning provides nutrients to the soil
        - Repeated use depletes essential minerals and organic matter
        - Nutrients often washed away by rain
        - Leads to poor soil quality over time
        - Increases erosion and runoff
        """)
    
    with col2:
        st.subheader("Increased Carbon Emissions")
        st.markdown("""
        - Burning releases carbon stored in trees and plants
        - Contributes to greenhouse gas emissions
        - Exacerbates global warming
        - Reduces forest carbon sequestration capacity
        - Creates air pollution and respiratory hazards
        """)
        
        st.subheader("Challenges to Sustainability")
        st.markdown("""
        - Loss of soil fertility forces farmers to move to new land
        - Continues the cycle of deforestation
        - Disrupts ecosystems for pollinators
        - Affects animals and plant species that depend on stable habitats
        - Creates a cycle of unsustainable land use
        """)

# SUSTAINABLE SOLUTIONS PAGE
elif page == "Sustainable Solutions":
    st.title("Agroforestry with Inga Trees: A Sustainable Solution")
    
    st.markdown("""
    A viable alternative to slash-and-burn farming is the integration of agroforestry using Inga trees. 
    This approach helps restore soil fertility and reduces environmental degradation.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Soil Restoration")
        st.markdown("""
        - Inga trees naturally enrich the soil by fixing nitrogen
        - Add organic matter through leaf mulch
        - Reduce the need for synthetic fertilizers
        - Create self-sustaining soil improvement system
        - Support beneficial soil microorganisms
        """)
        
        st.subheader("Moisture Retention")
        st.markdown("""
        - Leaves create a protective mulch layer
        - Retains soil moisture effectively
        - Prevents erosion during heavy rainfall
        - Stabilizes ground temperature
        - Reduces water requirements for crops
        """)
    
    with col2:
        st.subheader("Sustainable Land Use")
        st.markdown("""
        - Maintains soil health over time
        - Eliminates need for frequent land clearing
        - Preserves existing forests
        - Creates permanent agricultural plots
        - Integrates with natural ecosystem functions
        """)
        
        st.subheader("Low Maintenance")
        st.markdown("""
        - Trees require minimal care
        - Ideal for farmers managing extensive land areas
        - Reduce labor requirements long-term
        - Self-propagating once established
        - Resilient to local conditions
        """)
    
    st.header("Target Farmers for Agroforestry with Inga Trees")
    st.markdown("""
    The solution is particularly beneficial for:
    - Palm oil farmers
    - Wet rice farmers
    - Farmers in Brazil
    - Farmers practicing extensive agriculture (large-scale land management with minimal input requirements)
    """)
    
    st.header("Agricultural Context of the Solution")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Types of Agriculture")
        st.markdown("""
        - Conservational Agriculture: Focuses on restoring soil health and preventing land degradation
        - Agroforestry: Integrates trees with crops to enhance sustainability
        """)
    
    with col2:
        st.subheader("Technological Requirements")
        st.markdown("""
        - Low to moderate technology levels
        - Aligns with Second Agricultural Revolution (crop rotation, selective breeding)
        - Compatible with Green Revolution techniques (modern irrigation)
        - Requires only basic tools for planting and maintaining Inga trees
        """)
    
    with col3:
        st.subheader("Agricultural Revolution Relevance")
        st.markdown("""
        - Falls under the Third Agricultural Revolution (Green Revolution)
        - Emphasis on soil fertility and food security
        - Focuses on sustainable intensification
        - Reduces dependency on external inputs
        """)

# IMPLEMENTATION PAGE
elif page == "Implementation":
    st.title("Practical Implementation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Implementation Steps")
        st.markdown("""
        **Tree Planting:**
        - Integrate Inga trees into existing farming systems
        - Plant in rows between crop areas
        - Establish nurseries for Inga seedlings
        - Maintain appropriate spacing for optimal growth
        - Prune strategically to manage light exposure
        
        **Farmer Education:**
        - Provide training on agroforestry benefits
        - Teach sustainable farming techniques
        - Develop demonstration plots
        - Create farmer-to-farmer learning networks
        - Distribute educational materials in local languages
        """)
    
    with col2:
        st.markdown("""
        **Incentives & Policy Support:**
        - Governments can provide subsidies for adoption
        - NGOs can offer training programs
        - Improve resource accessibility
        - Develop certification programs for sustainable products
        - Create market linkages for agroforestry products
        """)
    
    st.header("Contribution to Global Food Security")
    st.markdown("""
    By improving soil fertility and providing shade, Inga trees can enhance crop yields in areas suffering from land degradation. This sustainable system ensures consistent food production without the need for additional land, contributing to food security for growing populations. Additionally, crops grown under agroforestry conditions are more resilient to extreme weather events, ensuring long-term agricultural productivity.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Productivity Benefits")
        st.markdown("""
        - Improved soil fertility
        - Higher crop yields
        - Reduced pest pressure
        - Diversified farm income
        - Sustainable long-term production
        """)
    
    with col2:
        st.subheader("Resilience Factors")
        st.markdown("""
        - Better drought resistance
        - Reduced flood impact
        - Temperature moderation
        - Wind protection
        - Habitat for beneficial insects
        """)
    
    with col3:
        st.subheader("Socioeconomic Impact")
        st.markdown("""
        - Reduced need to clear new land
        - Lower input costs
        - Stable agricultural livelihoods
        - Improved food sovereignty
        - Enhanced community resilience
        """)

# SDG ALIGNMENT PAGE
elif page == "SDG Alignment":
    st.title("Alignment with UN Sustainable Development Goals")
    
    st.markdown("""
    Agroforestry with Inga trees addresses key global challenges outlined in the United Nations Sustainable Development Goals (SDGs).
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Climate Action (SDG 13)")
        st.markdown("""
        - Reduces deforestation
        - Increases carbon sequestration
        - Minimizes slash-and-burn methods
        - Reduces agricultural carbon emissions
        - Promotes climate-resilient farming
        """)
    
    with col2:
        st.subheader("Zero Hunger (SDG 2)")
        st.markdown("""
        - Improves soil health
        - Increases crop yields
        - Combats food insecurity
        - Supports sustainable agriculture
        - Enhances agricultural resilience
        """)
    
    with col3:
        st.subheader("Life on Land (SDG 15)")
        st.markdown("""
        - Protects forests and biodiversity
        - Ensures ecosystem stability
        - Promotes sustainable land use
        - Prevents habitat fragmentation
        - Supports habitat connectivity
        """)
    
    st.header("Conclusion")
    st.markdown("""
    Agroforestry with Inga trees presents a practical, low-maintenance, and highly effective alternative to slash-and-burn agriculture. By restoring soil fertility, reducing deforestation, and improving crop resilience, this solution aligns with global sustainability goals while providing farmers with a viable long-term agricultural strategy. Governments, organizations, and farming communities must work together to implement and scale this approach for a more sustainable future.
    """)

# Add data source info in the sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("About This Application")
st.sidebar.info("""
This application visualizes slash-and-burn agriculture prevalence and presents sustainable alternatives using agroforestry with Inga trees.

**Note:** The map data is for demonstration purposes. For a production application, you should replace this with verified data from credible sources.
""")
