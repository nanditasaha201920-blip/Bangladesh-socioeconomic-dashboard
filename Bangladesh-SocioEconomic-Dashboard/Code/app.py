import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ১. পেজ কনফিগারেশন (স্ক্রিনশটের মতো চওড়া লেআউট)
st.set_page_config(page_title="Bangladesh Socio-Economic Dashboard", layout="wide")

# ২. ড্যাশবোর্ড টাইটেল ও হেডার (Custom CSS সহ)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Bangladesh Socio-Economic Dashboard")
st.markdown("Analysis of poverty, employment, income, and education across districts")

# ৩. ডেটা লোড করার ফাংশন (Error Handling সহ)
@st.cache_data
def load_data():
    file_path = "data/socioeconomic_bd.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        # ফাইল না থাকলে স্যাম্পল ডেটা তৈরি (আপনার দেওয়া আগের ডেটা অনুযায়ী)
        data = {
            'district': ['Dhaka', 'Chattogram', 'Rajshahi', 'Khulna', 'Barisal', 'Sylhet', 'Rangpur', 'Mymensingh'],
            'poverty_rate': [20, 25, 35, 30, 40, 28, 45, 38],
            'employment_rate': [65, 60, 55, 58, 50, 57, 48, 52],
            'avg_income': [30000, 25000, 18000, 20000, 15000, 22000, 14000, 16000],
            'literacy_rate': [85, 80, 75, 78, 70, 77, 68, 72]
        }
        return pd.DataFrame(data)

df = load_data()

# ৪. সাইডবার ফিল্টার
st.sidebar.header("🔎 Filter Control")
all_districts = ["All Districts"] + list(df["district"].unique())
selected_district = st.sidebar.selectbox("Select District Scope", all_districts)

# ডাটা ফিল্টারিং লজিক
if selected_district == "All Districts":
    display_df = df
else:
    display_df = df[df["district"] == selected_district]

# ৫. কি ইন্ডিকেটর (KPIs) - স্ক্রিনশটের স্টাইলে
st.subheader("📌 Key Indicators Overview")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric("Avg Poverty Rate", f"{display_df['poverty_rate'].mean():.1f}%")
with kpi2:
    st.metric("Avg Employment", f"{display_df['employment_rate'].mean():.1f}%")
with kpi3:
    st.metric("Avg Monthly Income", f"৳{display_df['avg_income'].mean():,.0f}")
with kpi4:
    st.metric("Avg Literacy", f"{display_df['literacy_rate'].mean():.1f}%")

st.divider()

# ৬. ভিজ্যুয়ালাইজেশন (Charts) - ২ কলাম লেআউট
col1, col2 = st.columns(2)

with col1:
    # Poverty Rate Bar Chart
    fig_pov = px.bar(display_df, x="district", y="poverty_rate", 
                     color="poverty_rate", color_continuous_scale='Reds',
                     title="Poverty Rate Comparison (%)",
                     labels={'poverty_rate':'Poverty (%)', 'district':'District'})
    st.plotly_chart(fig_pov, use_container_width=True)

    # Income vs Literacy Scatter
    fig_scatter = px.scatter(display_df, x="avg_income", y="literacy_rate", 
                             size="poverty_rate", color="district", hover_name="district",
                             title="Income vs Literacy (Bubble size = Poverty Rate)",
                             labels={'avg_income':'Avg Income (BDT)', 'literacy_rate':'Literacy (%)'})
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    # Employment Rate Bar Chart
    fig_emp = px.bar(display_df, x="district", y="employment_rate", 
                     color="employment_rate", color_continuous_scale='Greens',
                     title="Employment Opportunities (%)",
                     labels={'employment_rate':'Employment (%)', 'district':'District'})
    st.plotly_chart(fig_emp, use_container_width=True)

    # Average Income Chart
    fig_inc = px.bar(display_df, x="district", y="avg_income", 
                     color="avg_income", color_continuous_scale='Blues',
                     title="Average Monthly Income Distribution",
                     labels={'avg_income':'Income (BDT)', 'district':'District'})
    st.plotly_chart(fig_inc, use_container_width=True)

# ৭. ডেটা টেবিল ভিউ
with st.expander("📂 View Detailed Data Table"):
    st.dataframe(display_df.sort_values('poverty_rate', ascending=False), use_container_width=True)

# ৮. ফুটার
st.markdown("---")
st.caption("Dashboard developed for Socio-Economic Analysis of Bangladesh. Data updated as of 2026.")
