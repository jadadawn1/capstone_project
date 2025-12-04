"""
Streamlit Dashboard for Climate Signals Insight Platform
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import numpy as np
from prophet import Prophet
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Climate Signals Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8000"

st.markdown("""
<h1 style='text-align: center; color: #2E7D32;'>
    🌍 Climate Signals Insight Platform
</h1>
<p style='text-align: center; color: #666; font-size: 1.1em;'>
    Interactive dashboard for global climate analytics and insights
</p>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("📊 Navigation")
page = st.sidebar.radio(
    "Select a view:",
    ["Overview", "Country Analysis", "Time Series", "Comparisons", "Statistics", "Climate Risk Dashboard", "Top Performers", "Key Insights", "Correlation Analysis", "Forecasting"]
)

api_status = st.sidebar.checkbox("Show API Status", value=False)

if api_status:
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            st.sidebar.success("✓ API Connected")
        else:
            st.sidebar.error("✗ API Error")
    except requests.exceptions.RequestException:
        st.sidebar.error("✗ API Unavailable")


# Overview Page
if page == "Overview":
    st.header("📋 Overview")
    
    # Database stats
    try:
        response = requests.get(f"{API_BASE_URL}/api/records?limit=1", timeout=5)
        if response.status_code == 200:
            total_records = 1000  # We know we loaded 1000
            available_countries = 15
            years_span = "2000-2023"
        else:
            total_records = "N/A"
            available_countries = "N/A"
            years_span = "N/A"
    except:
        total_records = "N/A"
        available_countries = "N/A"
        years_span = "N/A"
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🌐 Platform Status", "Active", "✓ Online")
    
    with col2:
        st.metric("📊 Total Records", f"{total_records:,}" if isinstance(total_records, int) else total_records, "Climate Data")
    
    with col3:
        st.metric("🌍 Countries", available_countries, "Global Coverage")
    
    with col4:
        st.metric("📅 Years", years_span, "24 Years")
    
    st.markdown("---")
    
    st.subheader("📚 About This Dashboard")
    st.info("""
    The **Climate Signals Insight Platform** provides interactive visualizations
    and analyses of global climate data. Explore trends, compare countries,
    and discover insights about climate change indicators.
    
    ### Key Features:
    - 📊 Interactive charts and visualizations
    - 🌍 Country-by-country climate analysis
    - 📈 Time series trend analysis
    - 🔍 Multi-variable comparisons
    - 📋 Statistical summaries
    """)


# Country Analysis Page
elif page == "Country Analysis":
    st.header("🌍 Country Analysis")
    
    available_countries = [
        "Argentina", "Australia", "Brazil", "Canada", "China",
        "France", "Germany", "India", "Indonesia", "Japan",
        "Mexico", "Russia", "South Africa", "UK", "USA"
    ]
    
    country_input = st.selectbox("Select country:", available_countries, index=14)
    
    if st.button("Analyze Country"):
        try:
            response = requests.get(
                f"{API_BASE_URL}/api/records/country/{country_input}", timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data)
                
                st.success(f"✓ Found {len(df)} records for {country_input}")
                
                st.subheader("📊 Climate Data")
                st.dataframe(df, use_container_width=True)
                
                if 'year' in df.columns and 'avg_temperature' in df.columns:
                    st.subheader("🌡️ Temperature Trend")
                    
                    # Calculate trend
                    temp_mean = df['avg_temperature'].mean()
                    temp_change = df['avg_temperature'].iloc[-1] - df['avg_temperature'].iloc[0] if len(df) > 1 else 0
                    
                    col_t1, col_t2, col_t3 = st.columns(3)
                    with col_t1:
                        st.metric("Average Temperature", f"{temp_mean:.1f}°C")
                    with col_t2:
                        st.metric("Total Change", f"{temp_change:.1f}°C", delta=f"{temp_change:.1f}°C")
                    with col_t3:
                        trend = "Warming" if temp_change > 0 else "Cooling" if temp_change < 0 else "Stable"
                        st.metric("Trend", trend)
                    
                    fig_temp = px.line(
                        df, x='year', y='avg_temperature', markers=True,
                        title=f"Average Temperature Over Time - {country_input}",
                        labels={'avg_temperature': 'Temperature (°C)', 'year': 'Year'}
                    )
                    fig_temp.update_traces(line_color='#FF6B6B', marker=dict(size=8))
                    st.plotly_chart(fig_temp, use_container_width=True)
                
                if 'year' in df.columns and 'co2_per_capita' in df.columns:
                    st.subheader("💨 CO₂ Emissions")
                    
                    co2_mean = df['co2_per_capita'].mean()
                    co2_max = df['co2_per_capita'].max()
                    
                    col_c1, col_c2 = st.columns(2)
                    with col_c1:
                        st.metric("Average CO₂", f"{co2_mean:.2f} tons/capita")
                    with col_c2:
                        st.metric("Peak CO₂", f"{co2_max:.2f} tons/capita")
                    
                    fig_co2 = px.bar(
                        df, x='year', y='co2_per_capita',
                        title=f"CO₂ Emissions Per Capita - {country_input}",
                        labels={'co2_per_capita': 'CO₂ (metric tons)', 'year': 'Year'},
                        color='co2_per_capita',
                        color_continuous_scale='Reds'
                    )
                    st.plotly_chart(fig_co2, use_container_width=True)
            else:
                st.error(f"❌ No data found for {country_input}")
        
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {str(e)}")


# Time Series Page
elif page == "Time Series":
    st.header("📈 Time Series Analysis")
    
    available_countries = [
        "Argentina", "Australia", "Brazil", "Canada", "China",
        "France", "Germany", "India", "Indonesia", "Japan",
        "Mexico", "Russia", "South Africa", "UK", "USA"
    ]
    
    country_ts = st.selectbox("Select country:", available_countries, index=14, key="ts_country")
    
    indicator = st.selectbox(
        "Select indicator:",
        [
            ("Temperature (°C)", "avg_temperature"),
            ("CO₂ Emissions (tons/capita)", "co2_per_capita"),
            ("Rainfall (mm)", "rainfall"),
            ("Sea Level Rise (mm)", "sea_level_rise"),
            ("Renewable Energy (%)", "renewable_energy_percent")
        ],
        format_func=lambda x: x[0]
    )
    
    indicator_key = indicator[1]
    indicator_label = indicator[0]
    
    if st.button("Generate Time Series"):
        try:
            response = requests.get(f"{API_BASE_URL}/api/records/country/{country_ts}", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data)
                df_filtered = df[df[indicator_key].notna()].copy()
                
                if len(df_filtered) > 0:
                    st.success(f"Found {len(df_filtered)} records")
                    df_filtered = df_filtered.sort_values('year')
                    
                    # Show summary stats
                    val_mean = df_filtered[indicator_key].mean()
                    val_min = df_filtered[indicator_key].min()
                    val_max = df_filtered[indicator_key].max()
                    
                    col_s1, col_s2, col_s3 = st.columns(3)
                    with col_s1:
                        st.metric("Average", f"{val_mean:.2f}")
                    with col_s2:
                        st.metric("Minimum", f"{val_min:.2f}")
                    with col_s3:
                        st.metric("Maximum", f"{val_max:.2f}")
                    
                    fig = px.line(
                        df_filtered, x='year', y=indicator_key, markers=True,
                        title=f"{indicator_label} Time Series - {country_ts}",
                        labels={indicator_key: indicator_label, 'year': 'Year'}
                    )
                    fig.update_traces(line_color='#4CAF50', marker=dict(size=10))
                    fig.update_layout(hovermode='x unified')
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.subheader("Data Table")
                    st.dataframe(df_filtered[['year', indicator_key]], use_container_width=True)
                else:
                    st.warning(f"No data available for {indicator_label}")
            else:
                st.error(f"No data found for {country_ts}")
        
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {str(e)}")


# Comparisons Page
elif page == "Comparisons":
    st.header("🔍 Country Comparisons")
    
    available_countries = [
        "Argentina", "Australia", "Brazil", "Canada", "China",
        "France", "Germany", "India", "Indonesia", "Japan",
        "Mexico", "Russia", "South Africa", "UK", "USA"
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        country1 = st.selectbox("First country:", available_countries, index=14, key="comp1")
    
    with col2:
        country2 = st.selectbox("Second country:", available_countries, index=3, key="comp2")
    
    if st.button("Compare Countries"):
        try:
            response1 = requests.get(f"{API_BASE_URL}/api/records/country/{country1}", timeout=5)
            response2 = requests.get(f"{API_BASE_URL}/api/records/country/{country2}", timeout=5)
            
            if response1.status_code == 200 and response2.status_code == 200:
                df1 = pd.DataFrame(response1.json())
                df2 = pd.DataFrame(response2.json())
                
                indicators = ["avg_temperature", "co2_per_capita", "rainfall", "renewable_energy_percent"]
                
                comparison_data = {
                    "Indicator": [],
                    country1: [],
                    country2: []
                }
                
                indicator_labels = {
                    "avg_temperature": "Avg Temperature (°C)",
                    "co2_per_capita": "CO₂ Emissions (tons/capita)",
                    "rainfall": "Rainfall (mm)",
                    "renewable_energy_percent": "Renewable Energy (%)"
                }
                
                for ind in indicators:
                    val1 = df1[ind].mean() if ind in df1.columns else None
                    val2 = df2[ind].mean() if ind in df2.columns else None
                    
                    if val1 is not None and val2 is not None and not pd.isna(val1) and not pd.isna(val2):
                        comparison_data["Indicator"].append(indicator_labels[ind])
                        comparison_data[country1].append(round(val1, 2))
                        comparison_data[country2].append(round(val2, 2))
                
                if len(comparison_data["Indicator"]) > 0:
                    df_comparison = pd.DataFrame(comparison_data)
                    st.success(f"Comparing {country1} vs {country2}")
                    
                    for i, indicator in enumerate(comparison_data["Indicator"]):
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric(f"{indicator} - {country1}", f"{comparison_data[country1][i]:.2f}")
                        with col_b:
                            st.metric(f"{indicator} - {country2}", f"{comparison_data[country2][i]:.2f}")
                    
                    st.subheader("Side-by-Side Comparison")
                    df_melted = df_comparison.melt(id_vars=["Indicator"], var_name="Country", value_name="Value")
                    
                    fig = px.bar(
                        df_melted, x="Indicator", y="Value", color="Country", barmode="group",
                        title=f"Climate Indicators: {country1} vs {country2}",
                        color_discrete_sequence=['#2196F3', '#FF9800']
                    )
                    fig.update_layout(
                        xaxis_title="Climate Indicator",
                        yaxis_title="Value",
                        legend_title="Country",
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning(f"Insufficient comparable data")
            else:
                st.error("Could not fetch data for one or both countries")
        
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {str(e)}")


# Statistics Page
elif page == "Statistics":
    st.header("📊 Statistical Analysis")
    
    year_select = st.number_input("Select year:", min_value=2000, max_value=2023, value=2019, step=1)
    st.info("Data available for years 2000-2023")
    
    if st.button("Generate Statistics"):
        try:
            response = requests.get(f"{API_BASE_URL}/api/statistics/year/{year_select}", timeout=5)
            
            if response.status_code == 200:
                stats_data = response.json()
                df_stats = pd.DataFrame(stats_data)
                
                st.success(f"✓ Generated statistics for {year_select}")
                st.dataframe(df_stats, use_container_width=True)
                
                if 'avg_temperature_mean' in df_stats.columns:
                    fig = px.bar(
                        df_stats, x='country', y='avg_temperature_mean',
                        title=f"Average Temperature by Country - {year_select}",
                        labels={'avg_temperature_mean': 'Temperature (°C)'},
                        color='avg_temperature_mean',
                        color_continuous_scale='RdYlBu_r'
                    )
                    fig.update_layout(xaxis={'categoryorder':'total descending'})
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Add CO2 comparison if available
                    if 'co2_per_capita_mean' in df_stats.columns:
                        st.subheader("CO₂ Emissions Comparison")
                        fig_co2 = px.bar(
                            df_stats, x='country', y='co2_per_capita_mean',
                            title=f"CO₂ Emissions by Country - {year_select}",
                            labels={'co2_per_capita_mean': 'CO₂ (tons/capita)'},
                            color='co2_per_capita_mean',
                            color_continuous_scale='Reds'
                        )
                        fig_co2.update_layout(xaxis={'categoryorder':'total descending'})
                        st.plotly_chart(fig_co2, use_container_width=True)
            else:
                st.error(f"No data available for {year_select}")
        
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {str(e)}")


# Climate Risk Dashboard Page
elif page == "Climate Risk Dashboard":
    st.header("🌊 Climate Risk Dashboard")
    st.markdown("Identify countries facing the highest climate risks based on multiple indicators")
    
    try:
        # Fetch all records
        response = requests.get(f"{API_BASE_URL}/api/records?limit=1000", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            
            # Get latest year data
            latest_year = df['year'].max()
            df_latest = df[df['year'] == latest_year].copy()
            
            st.info(f"Analyzing climate risk data for {latest_year}")
            
            # Risk Categories
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🌡️ Highest Temperature Rise")
                df_temp = df.groupby('country')['avg_temperature'].agg(['min', 'max']).reset_index()
                df_temp['temp_change'] = df_temp['max'] - df_temp['min']
                df_temp_top = df_temp.nlargest(10, 'temp_change')
                
                fig_temp = px.bar(
                    df_temp_top, x='country', y='temp_change',
                    title="Top 10 Countries by Temperature Increase",
                    labels={'temp_change': 'Temperature Change (°C)'},
                    color='temp_change',
                    color_continuous_scale='YlOrRd'
                )
                st.plotly_chart(fig_temp, use_container_width=True)
                
                st.subheader("🌊 Highest Sea Level Rise")
                df_sea = df_latest.nlargest(10, 'sea_level_rise')
                fig_sea = px.bar(
                    df_sea, x='country', y='sea_level_rise',
                    title=f"Sea Level Rise by Country ({latest_year})",
                    labels={'sea_level_rise': 'Sea Level Rise (mm)'},
                    color='sea_level_rise',
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig_sea, use_container_width=True)
            
            with col2:
                st.subheader("⚠️ Most Extreme Weather Events")
                df_weather = df_latest.nlargest(10, 'extreme_weather_events')
                fig_weather = px.bar(
                    df_weather, x='country', y='extreme_weather_events',
                    title=f"Extreme Weather Events ({latest_year})",
                    labels={'extreme_weather_events': 'Number of Events'},
                    color='extreme_weather_events',
                    color_continuous_scale='Reds'
                )
                st.plotly_chart(fig_weather, use_container_width=True)
                
                st.subheader("💨 Highest CO₂ Emissions")
                df_co2 = df_latest.nlargest(10, 'co2_per_capita')
                fig_co2 = px.bar(
                    df_co2, x='country', y='co2_per_capita',
                    title=f"CO₂ Per Capita ({latest_year})",
                    labels={'co2_per_capita': 'CO₂ (tons/capita)'},
                    color='co2_per_capita',
                    color_continuous_scale='OrRd'
                )
                st.plotly_chart(fig_co2, use_container_width=True)
            
            # Risk Score Calculation
            st.markdown("---")
            st.subheader("🎯 Composite Risk Score")
            st.markdown("*Risk score based on temperature change, sea level rise, extreme weather, and CO₂ emissions*")
            
            # Normalize and calculate risk scores
            from sklearn.preprocessing import MinMaxScaler
            scaler = MinMaxScaler()
            
            df_risk = df_latest.copy()
            df_risk['temp_norm'] = scaler.fit_transform(df_temp.set_index('country').loc[df_risk['country'], 'temp_change'].values.reshape(-1, 1))
            df_risk['sea_norm'] = scaler.fit_transform(df_risk[['sea_level_rise']])
            df_risk['weather_norm'] = scaler.fit_transform(df_risk[['extreme_weather_events']])
            df_risk['co2_norm'] = scaler.fit_transform(df_risk[['co2_per_capita']])
            
            df_risk['risk_score'] = (
                df_risk['temp_norm'] * 0.3 +
                df_risk['sea_norm'] * 0.25 +
                df_risk['weather_norm'] * 0.25 +
                df_risk['co2_norm'] * 0.2
            ) * 100
            
            df_risk_sorted = df_risk.sort_values('risk_score', ascending=False)
            
            col_r1, col_r2 = st.columns([2, 1])
            
            with col_r1:
                fig_risk = px.bar(
                    df_risk_sorted.head(15), x='country', y='risk_score',
                    title="Climate Risk Score by Country",
                    labels={'risk_score': 'Risk Score (0-100)'},
                    color='risk_score',
                    color_continuous_scale='RdYlGn_r'
                )
                st.plotly_chart(fig_risk, use_container_width=True)
            
            with col_r2:
                st.markdown("##### Highest Risk Countries")
                for idx, row in df_risk_sorted.head(5).iterrows():
                    st.metric(
                        row['country'],
                        f"{row['risk_score']:.1f}",
                        delta=f"{row['extreme_weather_events']:.0f} events"
                    )
        
        else:
            st.error(f"API returned status code: {response.status_code}")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")


# Top Performers Page
elif page == "Top Performers":
    st.header("🏆 Top Performers & Laggards")
    st.markdown("Countries leading and trailing in climate action")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/records?limit=1000", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            
            latest_year = df['year'].max()
            df_latest = df[df['year'] == latest_year].copy()
            
            st.info(f"Performance data for {latest_year}")
            
            tab1, tab2, tab3, tab4 = st.tabs([
                "🌱 Renewable Energy", 
                "🌳 Forest Conservation", 
                "💨 CO₂ Emissions",
                "📊 Overall Performance"
            ])
            
            with tab1:
                st.subheader("Renewable Energy Leaders")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🥇 Top 10 Countries")
                    top_renewable = df_latest.nlargest(10, 'renewable_energy_percent')
                    fig_top_ren = px.bar(
                        top_renewable, x='renewable_energy_percent', y='country',
                        orientation='h',
                        title="Highest Renewable Energy Adoption",
                        labels={'renewable_energy_percent': 'Renewable Energy (%)'},
                        color='renewable_energy_percent',
                        color_continuous_scale='Greens'
                    )
                    st.plotly_chart(fig_top_ren, use_container_width=True)
                
                with col2:
                    st.markdown("#### 📉 Bottom 10 Countries")
                    bottom_renewable = df_latest.nsmallest(10, 'renewable_energy_percent')
                    fig_bot_ren = px.bar(
                        bottom_renewable, x='renewable_energy_percent', y='country',
                        orientation='h',
                        title="Lowest Renewable Energy Adoption",
                        labels={'renewable_energy_percent': 'Renewable Energy (%)'},
                        color='renewable_energy_percent',
                        color_continuous_scale='Reds'
                    )
                    st.plotly_chart(fig_bot_ren, use_container_width=True)
            
            with tab2:
                st.subheader("Forest Conservation")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🥇 Highest Forest Coverage")
                    top_forest = df_latest.nlargest(10, 'forest_area_percent')
                    fig_top_for = px.bar(
                        top_forest, x='forest_area_percent', y='country',
                        orientation='h',
                        title="Countries with Most Forest Area",
                        labels={'forest_area_percent': 'Forest Area (%)'},
                        color='forest_area_percent',
                        color_continuous_scale='BuGn'
                    )
                    st.plotly_chart(fig_top_for, use_container_width=True)
                
                with col2:
                    # Calculate forest loss over time
                    df_forest_change = df.groupby('country').agg({
                        'forest_area_percent': ['first', 'last']
                    }).reset_index()
                    df_forest_change.columns = ['country', 'first', 'last']
                    df_forest_change['change'] = df_forest_change['last'] - df_forest_change['first']
                    
                    st.markdown("#### 📈 Forest Area Change (2000-2023)")
                    worst_forest = df_forest_change.nsmallest(10, 'change')
                    fig_forest_loss = px.bar(
                        worst_forest, x='change', y='country',
                        orientation='h',
                        title="Largest Forest Area Decrease",
                        labels={'change': 'Change in Forest Area (%)'},
                        color='change',
                        color_continuous_scale='YlOrRd'
                    )
                    st.plotly_chart(fig_forest_loss, use_container_width=True)
            
            with tab3:
                st.subheader("CO₂ Emissions")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🥇 Lowest Emissions")
                    low_co2 = df_latest.nsmallest(10, 'co2_per_capita')
                    fig_low_co2 = px.bar(
                        low_co2, x='co2_per_capita', y='country',
                        orientation='h',
                        title="Countries with Lowest CO₂ Per Capita",
                        labels={'co2_per_capita': 'CO₂ (tons/capita)'},
                        color='co2_per_capita',
                        color_continuous_scale='Greens_r'
                    )
                    st.plotly_chart(fig_low_co2, use_container_width=True)
                
                with col2:
                    st.markdown("#### 📉 Highest Emissions")
                    high_co2 = df_latest.nlargest(10, 'co2_per_capita')
                    fig_high_co2 = px.bar(
                        high_co2, x='co2_per_capita', y='country',
                        orientation='h',
                        title="Countries with Highest CO₂ Per Capita",
                        labels={'co2_per_capita': 'CO₂ (tons/capita)'},
                        color='co2_per_capita',
                        color_continuous_scale='Reds'
                    )
                    st.plotly_chart(fig_high_co2, use_container_width=True)
            
            with tab4:
                st.subheader("Overall Climate Performance Score")
                st.markdown("*Composite score: Renewable Energy + Forest Area - CO₂ Emissions - Extreme Weather*")
                
                # Calculate performance score
                from sklearn.preprocessing import MinMaxScaler
                scaler = MinMaxScaler()
                
                df_perf = df_latest.copy()
                df_perf['renewable_norm'] = scaler.fit_transform(df_perf[['renewable_energy_percent']])
                df_perf['forest_norm'] = scaler.fit_transform(df_perf[['forest_area_percent']])
                df_perf['co2_norm'] = scaler.fit_transform(df_perf[['co2_per_capita']])
                df_perf['weather_norm'] = scaler.fit_transform(df_perf[['extreme_weather_events']])
                
                df_perf['performance_score'] = (
                    df_perf['renewable_norm'] * 0.3 +
                    df_perf['forest_norm'] * 0.3 -
                    df_perf['co2_norm'] * 0.25 -
                    df_perf['weather_norm'] * 0.15
                ) * 100
                
                df_perf_sorted = df_perf.sort_values('performance_score', ascending=False)
                
                col_p1, col_p2 = st.columns(2)
                
                with col_p1:
                    st.markdown("#### 🥇 Top Performers")
                    fig_top_perf = px.bar(
                        df_perf_sorted.head(10), x='performance_score', y='country',
                        orientation='h',
                        title="Best Climate Performance",
                        labels={'performance_score': 'Performance Score'},
                        color='performance_score',
                        color_continuous_scale='RdYlGn'
                    )
                    st.plotly_chart(fig_top_perf, use_container_width=True)
                
                with col_p2:
                    st.markdown("#### 📉 Bottom Performers")
                    fig_bot_perf = px.bar(
                        df_perf_sorted.tail(10), x='performance_score', y='country',
                        orientation='h',
                        title="Needs Improvement",
                        labels={'performance_score': 'Performance Score'},
                        color='performance_score',
                        color_continuous_scale='RdYlGn'
                    )
                    st.plotly_chart(fig_bot_perf, use_container_width=True)
        
        else:
            st.error(f"API returned status code: {response.status_code}")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")


# Key Insights Page
elif page == "Key Insights":
    st.header("💡 Key Insights & Trends")
    st.markdown("Auto-generated insights from global climate data")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/records?limit=1000", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            
            # Global Statistics
            st.subheader("🌍 Global Climate Snapshot")
            
            earliest_year = df['year'].min()
            latest_year = df['year'].max()
            df_early = df[df['year'] == earliest_year]
            df_late = df[df['year'] == latest_year]
            
            col1, col2, col3, col4 = st.columns(4)
            
            # Temperature Change
            temp_early = df_early['avg_temperature'].mean()
            temp_late = df_late['avg_temperature'].mean()
            temp_change = temp_late - temp_early
            
            with col1:
                st.metric(
                    "🌡️ Global Avg Temperature",
                    f"{temp_late:.2f}°C",
                    f"+{temp_change:.2f}°C since {earliest_year}"
                )
            
            # CO2 Change
            co2_early = df_early['co2_per_capita'].mean()
            co2_late = df_late['co2_per_capita'].mean()
            co2_change = co2_late - co2_early
            
            with col2:
                st.metric(
                    "💨 Avg CO₂ Emissions",
                    f"{co2_late:.2f} tons",
                    f"{co2_change:+.2f} tons since {earliest_year}"
                )
            
            # Renewable Energy
            ren_early = df_early['renewable_energy_percent'].mean()
            ren_late = df_late['renewable_energy_percent'].mean()
            ren_change = ren_late - ren_early
            
            with col3:
                st.metric(
                    "🌱 Renewable Energy",
                    f"{ren_late:.1f}%",
                    f"+{ren_change:.1f}% since {earliest_year}"
                )
            
            # Extreme Weather
            weather_total = df_late['extreme_weather_events'].sum()
            
            with col4:
                st.metric(
                    "⚠️ Extreme Weather Events",
                    f"{int(weather_total)}",
                    f"in {latest_year}"
                )
            
            # Trend Analysis
            st.markdown("---")
            st.subheader("📈 Historical Trends")
            
            col_t1, col_t2 = st.columns(2)
            
            with col_t1:
                # Temperature Trend
                df_temp_trend = df.groupby('year')['avg_temperature'].mean().reset_index()
                fig_temp_trend = px.line(
                    df_temp_trend, x='year', y='avg_temperature',
                    title="Global Average Temperature Trend",
                    labels={'avg_temperature': 'Temperature (°C)'},
                    markers=True
                )
                fig_temp_trend.update_traces(line_color='#FF6B6B')
                st.plotly_chart(fig_temp_trend, use_container_width=True)
                
                # Renewable Energy Trend
                df_ren_trend = df.groupby('year')['renewable_energy_percent'].mean().reset_index()
                fig_ren_trend = px.line(
                    df_ren_trend, x='year', y='renewable_energy_percent',
                    title="Global Renewable Energy Adoption",
                    labels={'renewable_energy_percent': 'Renewable Energy (%)'},
                    markers=True
                )
                fig_ren_trend.update_traces(line_color='#4CAF50')
                st.plotly_chart(fig_ren_trend, use_container_width=True)
            
            with col_t2:
                # CO2 Trend
                df_co2_trend = df.groupby('year')['co2_per_capita'].mean().reset_index()
                fig_co2_trend = px.line(
                    df_co2_trend, x='year', y='co2_per_capita',
                    title="Global CO₂ Emissions Trend",
                    labels={'co2_per_capita': 'CO₂ (tons/capita)'},
                    markers=True
                )
                fig_co2_trend.update_traces(line_color='#FF9800')
                st.plotly_chart(fig_co2_trend, use_container_width=True)
                
                # Weather Events Trend
                df_weather_trend = df.groupby('year')['extreme_weather_events'].sum().reset_index()
                fig_weather_trend = px.line(
                    df_weather_trend, x='year', y='extreme_weather_events',
                    title="Total Extreme Weather Events",
                    labels={'extreme_weather_events': 'Number of Events'},
                    markers=True
                )
                fig_weather_trend.update_traces(line_color='#F44336')
                st.plotly_chart(fig_weather_trend, use_container_width=True)
            
            # Key Findings
            st.markdown("---")
            st.subheader("🔍 Key Findings")
            
            col_f1, col_f2 = st.columns(2)
            
            with col_f1:
                st.markdown("#### 🌡️ Temperature Insights")
                
                # Fastest warming country
                df_temp_change = df.groupby('country').agg({
                    'avg_temperature': ['first', 'last']
                }).reset_index()
                df_temp_change.columns = ['country', 'first', 'last']
                df_temp_change['change'] = df_temp_change['last'] - df_temp_change['first']
                fastest_warming = df_temp_change.loc[df_temp_change['change'].idxmax()]
                
                st.info(f"**Fastest Warming:** {fastest_warming['country']} (+{fastest_warming['change']:.2f}°C)")
                
                # Coolest country
                coolest_country = df_late.loc[df_late['avg_temperature'].idxmin()]
                st.info(f"**Coolest Country ({latest_year}):** {coolest_country['country']} ({coolest_country['avg_temperature']:.1f}°C)")
                
                # Hottest country
                hottest_country = df_late.loc[df_late['avg_temperature'].idxmax()]
                st.info(f"**Hottest Country ({latest_year}):** {hottest_country['country']} ({hottest_country['avg_temperature']:.1f}°C)")
            
            with col_f2:
                st.markdown("#### 🌱 Environmental Progress")
                
                # Most renewable
                most_renewable = df_late.loc[df_late['renewable_energy_percent'].idxmax()]
                st.success(f"**Renewable Leader:** {most_renewable['country']} ({most_renewable['renewable_energy_percent']:.1f}%)")
                
                # Lowest CO2
                lowest_co2 = df_late.loc[df_late['co2_per_capita'].idxmin()]
                st.success(f"**Lowest CO₂:** {lowest_co2['country']} ({lowest_co2['co2_per_capita']:.2f} tons/capita)")
                
                # Most forest
                most_forest = df_late.loc[df_late['forest_area_percent'].idxmax()]
                st.success(f"**Forest Leader:** {most_forest['country']} ({most_forest['forest_area_percent']:.1f}%)")
            
            # Warnings
            st.markdown("---")
            st.subheader("⚠️ Areas of Concern")
            
            col_w1, col_w2 = st.columns(2)
            
            with col_w1:
                # Highest CO2
                highest_co2 = df_late.loc[df_late['co2_per_capita'].idxmax()]
                st.warning(f"**Highest CO₂ Emitter:** {highest_co2['country']} ({highest_co2['co2_per_capita']:.2f} tons/capita)")
                
                # Most weather events
                most_weather = df_late.loc[df_late['extreme_weather_events'].idxmax()]
                st.warning(f"**Most Extreme Weather:** {most_weather['country']} ({int(most_weather['extreme_weather_events'])} events)")
            
            with col_w2:
                # Lowest renewable
                lowest_renewable = df_late.loc[df_late['renewable_energy_percent'].idxmin()]
                st.warning(f"**Lowest Renewable Energy:** {lowest_renewable['country']} ({lowest_renewable['renewable_energy_percent']:.1f}%)")
                
                # Highest sea level
                highest_sea = df_late.loc[df_late['sea_level_rise'].idxmax()]
                st.warning(f"**Highest Sea Level Rise:** {highest_sea['country']} ({highest_sea['sea_level_rise']:.1f} mm)")
        
        else:
            st.error(f"API returned status code: {response.status_code}")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")


# Correlation Analysis Page
elif page == "Correlation Analysis":
    st.header("📊 Correlation Analysis")
    st.markdown("Explore relationships between different climate indicators")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/records?limit=1000", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            
            # Select latest year for correlation
            latest_year = df['year'].max()
            df_latest = df[df['year'] == latest_year].copy()
            
            st.info(f"Correlation analysis for {latest_year}")
            
            # Select numeric columns for correlation
            numeric_cols = [
                'avg_temperature', 'co2_per_capita', 'rainfall', 
                'sea_level_rise', 'renewable_energy_percent', 
                'forest_area_percent', 'extreme_weather_events', 'population'
            ]
            
            # Calculate correlation matrix
            corr_matrix = df_latest[numeric_cols].corr()
            
            # Display correlation heatmap
            st.subheader("🔥 Correlation Heatmap")
            st.markdown("*Values range from -1 (negative correlation) to +1 (positive correlation)*")
            
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=[col.replace('_', ' ').title() for col in corr_matrix.columns],
                y=[col.replace('_', ' ').title() for col in corr_matrix.index],
                colorscale='RdBu_r',
                zmid=0,
                text=corr_matrix.values.round(2),
                texttemplate='%{text}',
                textfont={"size": 10},
                colorbar=dict(title="Correlation")
            ))
            
            fig_heatmap.update_layout(
                title="Climate Indicators Correlation Matrix",
                xaxis_title="Indicators",
                yaxis_title="Indicators",
                height=600
            )
            
            st.plotly_chart(fig_heatmap, use_container_width=True)
            
            # Key Correlations
            st.markdown("---")
            st.subheader("🔍 Key Correlations")
            
            col_cor1, col_cor2 = st.columns(2)
            
            with col_cor1:
                st.markdown("#### 💪 Strongest Positive Correlations")
                # Get top positive correlations (excluding diagonal)
                corr_flat = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
                corr_stack = corr_flat.stack().sort_values(ascending=False)
                
                for idx, (pair, value) in enumerate(corr_stack.head(5).items()):
                    var1 = pair[0].replace('_', ' ').title()
                    var2 = pair[1].replace('_', ' ').title()
                    st.success(f"**{var1}** ↔️ **{var2}**: {value:.3f}")
            
            with col_cor2:
                st.markdown("#### 🔻 Strongest Negative Correlations")
                for idx, (pair, value) in enumerate(corr_stack.tail(5).items()):
                    var1 = pair[0].replace('_', ' ').title()
                    var2 = pair[1].replace('_', ' ').title()
                    st.warning(f"**{var1}** ↔️ **{var2}**: {value:.3f}")
            
            # Interactive Scatter Plots
            st.markdown("---")
            st.subheader("🎯 Detailed Correlation Explorer")
            
            col_s1, col_s2 = st.columns(2)
            
            with col_s1:
                x_var = st.selectbox(
                    "Select X-axis variable:",
                    numeric_cols,
                    format_func=lambda x: x.replace('_', ' ').title(),
                    key="corr_x"
                )
            
            with col_s2:
                y_var = st.selectbox(
                    "Select Y-axis variable:",
                    numeric_cols,
                    index=1,
                    format_func=lambda x: x.replace('_', ' ').title(),
                    key="corr_y"
                )
            
            if x_var != y_var:
                correlation = df_latest[x_var].corr(df_latest[y_var])
                
                st.metric(
                    f"Correlation between {x_var.replace('_', ' ').title()} and {y_var.replace('_', ' ').title()}",
                    f"{correlation:.3f}",
                    delta="Strong" if abs(correlation) > 0.7 else "Moderate" if abs(correlation) > 0.4 else "Weak"
                )
                
                fig_scatter = px.scatter(
                    df_latest, x=x_var, y=y_var,
                    color='country',
                    title=f"{x_var.replace('_', ' ').title()} vs {y_var.replace('_', ' ').title()}",
                    labels={x_var: x_var.replace('_', ' ').title(), y_var: y_var.replace('_', ' ').title()},
                    trendline="ols",
                    hover_data=['country']
                )
                
                st.plotly_chart(fig_scatter, use_container_width=True)
            else:
                st.info("Please select different variables for X and Y axes")
            
            # Time-based correlation (how correlations change over time)
            st.markdown("---")
            st.subheader("📈 Correlation Trends Over Time")
            
            # Calculate correlation for each year
            years = sorted(df['year'].unique())
            corr_over_time = []
            
            var1 = st.selectbox(
                "Select first variable:",
                numeric_cols,
                format_func=lambda x: x.replace('_', ' ').title(),
                key="trend_var1"
            )
            var2 = st.selectbox(
                "Select second variable:",
                numeric_cols,
                index=1,
                format_func=lambda x: x.replace('_', ' ').title(),
                key="trend_var2"
            )
            
            if var1 != var2:
                for year in years:
                    df_year = df[df['year'] == year]
                    if len(df_year) > 1:
                        corr = df_year[var1].corr(df_year[var2])
                        corr_over_time.append({'year': year, 'correlation': corr})
                
                df_corr_trend = pd.DataFrame(corr_over_time)
                
                fig_trend = px.line(
                    df_corr_trend, x='year', y='correlation',
                    title=f"Correlation Trend: {var1.replace('_', ' ').title()} vs {var2.replace('_', ' ').title()}",
                    labels={'correlation': 'Correlation Coefficient', 'year': 'Year'},
                    markers=True
                )
                fig_trend.add_hline(y=0, line_dash="dash", line_color="gray")
                fig_trend.update_traces(line_color='#9C27B0')
                
                st.plotly_chart(fig_trend, use_container_width=True)
            else:
                st.info("Please select different variables")
        
        else:
            st.error(f"API returned status code: {response.status_code}")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")


# Forecasting Page
elif page == "Forecasting":
    st.header("🔮 Climate Forecasting")
    st.markdown("Predict future climate trends using Prophet time-series forecasting")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/records?limit=1000", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            
            st.info("Generate forecasts for temperature and CO₂ emissions (1-5 years ahead)")
            
            # User inputs
            col_f1, col_f2, col_f3 = st.columns(3)
            
            with col_f1:
                country_forecast = st.selectbox(
                    "Select country:",
                    ["Argentina", "Australia", "Brazil", "Canada", "China",
                     "France", "Germany", "India", "Indonesia", "Japan",
                     "Mexico", "Russia", "South Africa", "UK", "USA"],
                    index=14,
                    key="forecast_country"
                )
            
            with col_f2:
                indicator_forecast = st.selectbox(
                    "Select indicator:",
                    [("Temperature (°C)", "avg_temperature"),
                     ("CO₂ Emissions (tons/capita)", "co2_per_capita"),
                     ("Sea Level Rise (mm)", "sea_level_rise"),
                     ("Renewable Energy (%)", "renewable_energy_percent")],
                    format_func=lambda x: x[0],
                    key="forecast_indicator"
                )
            
            with col_f3:
                years_ahead = st.slider("Forecast years ahead:", 1, 5, 3)
            
            if st.button("Generate Forecast", type="primary"):
                with st.spinner("Training forecast model..."):
                    # Prepare data for Prophet
                    df_country = df[df['country'] == country_forecast].sort_values('year')
                    
                    indicator_key = indicator_forecast[1]
                    indicator_name = indicator_forecast[0]
                    
                    # Prophet requires 'ds' (date) and 'y' (value) columns
                    df_prophet = pd.DataFrame({
                        'ds': pd.to_datetime(df_country['year'], format='%Y'),
                        'y': df_country[indicator_key]
                    })
                    
                    if len(df_prophet) >= 3:  # Need at least 3 data points
                        # Train Prophet model
                        model = Prophet(
                            yearly_seasonality=False,
                            weekly_seasonality=False,
                            daily_seasonality=False,
                            changepoint_prior_scale=0.05
                        )
                        model.fit(df_prophet)
                        
                        # Create future dataframe
                        future = model.make_future_dataframe(periods=years_ahead, freq='YE')
                        forecast = model.predict(future)
                        
                        # Display results
                        st.success(f"Forecast generated for {country_forecast}")
                        
                        # Plot forecast
                        col_p1, col_p2 = st.columns([2, 1])
                        
                        with col_p1:
                            fig_forecast = go.Figure()
                            
                            # Historical data
                            fig_forecast.add_trace(go.Scatter(
                                x=df_prophet['ds'],
                                y=df_prophet['y'],
                                mode='markers+lines',
                                name='Historical Data',
                                line=dict(color='#2196F3', width=2),
                                marker=dict(size=8)
                            ))
                            
                            # Forecast
                            forecast_future = forecast[forecast['ds'] > df_prophet['ds'].max()]
                            fig_forecast.add_trace(go.Scatter(
                                x=forecast_future['ds'],
                                y=forecast_future['yhat'],
                                mode='markers+lines',
                                name='Forecast',
                                line=dict(color='#FF9800', width=2, dash='dash'),
                                marker=dict(size=8)
                            ))
                            
                            # Confidence interval
                            fig_forecast.add_trace(go.Scatter(
                                x=forecast_future['ds'].tolist() + forecast_future['ds'].tolist()[::-1],
                                y=forecast_future['yhat_upper'].tolist() + forecast_future['yhat_lower'].tolist()[::-1],
                                fill='toself',
                                fillcolor='rgba(255,152,0,0.2)',
                                line=dict(color='rgba(255,255,255,0)'),
                                name='Confidence Interval',
                                showlegend=True
                            ))
                            
                            fig_forecast.update_layout(
                                title=f"{indicator_name} Forecast - {country_forecast}",
                                xaxis_title="Year",
                                yaxis_title=indicator_name,
                                hovermode='x unified',
                                height=500
                            )
                            
                            st.plotly_chart(fig_forecast, use_container_width=True)
                        
                        with col_p2:
                            st.markdown("#### 📊 Forecast Values")
                            
                            latest_actual = df_prophet['y'].iloc[-1]
                            latest_year = df_prophet['ds'].iloc[-1].year
                            
                            st.metric("Latest Actual Value", f"{latest_actual:.2f}", f"Year {latest_year}")
                            
                            st.markdown("---")
                            st.markdown("##### Future Predictions")
                            
                            for idx, row in forecast_future.iterrows():
                                year = row['ds'].year
                                value = row['yhat']
                                change = value - latest_actual
                                
                                st.metric(
                                    f"Year {year}",
                                    f"{value:.2f}",
                                    delta=f"{change:+.2f}"
                                )
                        
                        # Forecast table
                        st.markdown("---")
                        st.subheader("📋 Detailed Forecast Table")
                        
                        forecast_table = forecast_future[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
                        forecast_table['ds'] = forecast_table['ds'].dt.year
                        forecast_table.columns = ['Year', 'Predicted Value', 'Lower Bound', 'Upper Bound']
                        forecast_table = forecast_table.round(2)
                        
                        st.dataframe(forecast_table, use_container_width=True)
                        
                        # Interpretation
                        st.markdown("---")
                        st.subheader("💡 Forecast Interpretation")
                        
                        trend = "increasing" if forecast_future['yhat'].iloc[-1] > latest_actual else "decreasing"
                        change_percent = ((forecast_future['yhat'].iloc[-1] - latest_actual) / latest_actual) * 100
                        
                        col_i1, col_i2 = st.columns(2)
                        
                        with col_i1:
                            st.info(f"**Trend Direction:** {trend.capitalize()}")
                            st.info(f"**Expected Change:** {change_percent:+.1f}% over {years_ahead} years")
                        
                        with col_i2:
                            st.info(f"**Average Annual Change:** {change_percent/years_ahead:+.1f}% per year")
                            uncertainty = ((forecast_future['yhat_upper'].iloc[-1] - forecast_future['yhat_lower'].iloc[-1]) / 2) / forecast_future['yhat'].iloc[-1] * 100
                            st.info(f"**Forecast Uncertainty:** ±{uncertainty:.1f}%")
                    
                    else:
                        st.error(f"Not enough data for {country_forecast}. Need at least 3 years of data.")
            
            # Global Forecast Comparison
            st.markdown("---")
            st.subheader("🌍 Global Forecast Comparison")
            st.markdown("Compare forecast trends across multiple countries")
            
            if st.button("Generate Multi-Country Forecast"):
                selected_countries = ["USA", "China", "India", "Germany", "Brazil"]
                
                with st.spinner("Generating forecasts for multiple countries..."):
                    all_forecasts = []
                    
                    for country in selected_countries:
                        df_country = df[df['country'] == country].sort_values('year')
                        
                        df_prophet = pd.DataFrame({
                            'ds': pd.to_datetime(df_country['year'], format='%Y'),
                            'y': df_country['avg_temperature']
                        })
                        
                        if len(df_prophet) >= 3:
                            model = Prophet(
                                yearly_seasonality=False,
                                weekly_seasonality=False,
                                daily_seasonality=False,
                                changepoint_prior_scale=0.05
                            )
                            model.fit(df_prophet)
                            
                            future = model.make_future_dataframe(periods=3, freq='YE')
                            forecast = model.predict(future)
                            
                            forecast['country'] = country
                            all_forecasts.append(forecast)
                    
                    if all_forecasts:
                        fig_multi = go.Figure()
                        
                        colors = ['#2196F3', '#FF9800', '#4CAF50', '#F44336', '#9C27B0']
                        
                        for i, (country, forecast) in enumerate(zip(selected_countries, all_forecasts)):
                            fig_multi.add_trace(go.Scatter(
                                x=forecast['ds'],
                                y=forecast['yhat'],
                                mode='lines+markers',
                                name=country,
                                line=dict(color=colors[i], width=2)
                            ))
                        
                        fig_multi.update_layout(
                            title="Temperature Forecast Comparison (Next 3 Years)",
                            xaxis_title="Year",
                            yaxis_title="Temperature (°C)",
                            hovermode='x unified',
                            height=500
                        )
                        
                        st.plotly_chart(fig_multi, use_container_width=True)
                        
                        st.success(f"Generated forecasts for {len(selected_countries)} countries")
        
        else:
            st.error(f"API returned status code: {response.status_code}")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.exception(e)


# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p><small>Climate Signals Insight Platform © 2025 | All Rights Reserved</small></p>
        <p><small>For API documentation, visit: http://localhost:8000/docs</small></p>
    </div>
    """,
    unsafe_allow_html=True
)
