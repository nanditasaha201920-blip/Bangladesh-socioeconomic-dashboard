import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Bangladesh Socio-Economic Dashboard", layout="wide")

# Title
st.title(" Bangladesh Socio-Economic Dashboard")
st.markdown("Analysis of poverty, employment, income, and education across districts")

# Load data
df = pd.read_csv("data/socioeconomic_bd.csv")

# Sidebar filter
st.sidebar.header(" Filter")
district = st.sidebar.selectbox("Select District", ["All"] + list(df["district"].unique()))

if district != "All":
    df = df[df["district"] == district]

# KPIs
st.subheader(" Key Indicators")

col1, col2, col3 = st.columns(3)

col1.metric("Avg Poverty Rate", f"{df['poverty_rate'].mean():.1f}%")
col2.metric("Avg Employment Rate", f"{df['employment_rate'].mean():.1f}%")
col3.metric("Avg Income", f"{df['avg_income'].mean():.0f}")

# Charts
st.subheader(" Data Visualizations")

col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(df, x="district", y="poverty_rate",
                  color="poverty_rate",
                  title="Poverty Rate by District")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.bar(df, x="district", y="employment_rate",
                  color="employment_rate",
                  title="Employment Rate by District")
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    fig3 = px.scatter(df,
                      x="avg_income",
                      y="literacy_rate",
                      size="poverty_rate",
                      color="district",
                      title="Income vs Literacy")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.bar(df, x="district", y="avg_income",
                  color="avg_income",
                  title="Average Income by District")
    st.plotly_chart(fig4, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(" Data Source: Sample socio-economic dataset (Bangladesh)")
