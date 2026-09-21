import os
import io
import pandas as pd
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents import create_pandas_dataframe_agent

# ---------------------------------------------------------
# 1. Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="PSX Stock Screener & AI Agent",
    page_icon="📈",
    layout="wide"
)

st.title("📈 PSX Stock Screener & AI Analysis Agent")
st.markdown("Upload your PSX stock data CSV to filter, analyze, and query stock metrics using AI.")

# ---------------------------------------------------------
# 2. File Download Feature (For Updated app.py)
# ---------------------------------------------------------
with open(__file__, "r", encoding="utf-8") as f:
    app_code = f.read()

st.sidebar.download_button(
    label="💾 Download Updated app.py",
    data=app_code,
    file_name="app.py",
    mime="text/x-python"
)

# ---------------------------------------------------------
# 3. Sidebar Configuration & API Key Initialization
# ---------------------------------------------------------
st.sidebar.header("⚙️ Configuration")

# Retrieve Gemini API Key securely from st.secrets or user input
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

# Safeguard variable definition to prevent NameError
llm = None
if api_key:
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.2
        )
        st.sidebar.success("Gemini LLM Connected!")
    except Exception as e:
        st.sidebar.error(f"Failed to initialize LLM: {str(e)}")

# ---------------------------------------------------------
# 4. Data Loading & Stock Screening
# ---------------------------------------------------------
uploaded_file = st.sidebar.file_uploader("Upload PSX CSV File", type=["csv"])

df = None
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success("Dataset loaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Error loading file: {e}")
elif os.path.exists("psx_stocks_data.csv"):
    df = pd.read_csv("psx_stocks_data.csv")
    st.sidebar.info("Loaded default dataset: psx_stocks_data.csv")

if df is not None:
    st.subheader("📊 Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    # Sidebar Stock Screener Controls
    st.sidebar.header("🎯 Stock Screener Filters")
    
    # Check for expected PSX metric columns
    if "MarketCap" in df.columns:
        min_mc, max_mc = float(df["MarketCap"].min()), float(df["MarketCap"].max())
        mc_range = st.sidebar.slider("Market Cap Range (in Billions)", min_mc, max_mc, (5.0, 40.0))
        df = df[(df["MarketCap"] >= mc_range[0]) & (df["MarketCap"] <= mc_range[1])]

    if "PromoterHolding" in df.columns:
        min_promoter = st.sidebar.slider("Minimum Promoter Holding (%)", 0.0, 100.0, 60.0)
        df = df[df["PromoterHolding"] >= min_promoter]

    if "SalesGrowth" in df.columns:
        min_sales = st.sidebar.slider("Minimum Sales Growth (%)", -50.0, 200.0, 20.0)
        df = df[df["SalesGrowth"] >= min_sales]

    if "ProfitGrowth" in df.columns:
        min_profit = st.sidebar.slider("Minimum Profit Growth (%)", -50.0, 200.0, 20.0)
        df = df[df["ProfitGrowth"] >= min_profit]

    st.subheader("🔍 Filtered PSX Stocks")
    st.write(f"Showing **{len(df)}** matching stocks:")
    st.dataframe(df, use_container_width=True)

    # ---------------------------------------------------------
    # 5. AI Agent Section (LangChain + Pandas)
    # ---------------------------------------------------------
    st.markdown("---")
    st.subheader("🤖 Ask the AI Agent About PSX Data")

    query = st.text_input("Ask a question about the stocks (e.g., 'Which company has the highest profit growth?'):")

    if query:
        if llm is None:
            st.error("Please provide a valid Gemini API key in the sidebar to run AI queries.")
        else:
            with st.spinner("AI Agent is analyzing the dataset..."):
                try:
                    # Create Pandas DataFrame Agent safely
                    agent = create_pandas_dataframe_agent(
                        llm=llm,
                        df=df,
                        verbose=True,
                        allow_dangerous_code=True
                    )
                    
                    response = agent.run(query)
                    st.success("Analysis Complete!")
                    st.write(response)
                except Exception as e:
                    st.error(f"Error executing AI query: {str(e)}")

else:
    st.warning("Please upload a CSV file or ensure `psx_stocks_data.csv` exists in the app root directory.")
