import os
import io
import pandas as pd
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import CSVSearchTool

# ---------------------------------------------------------
# 1. Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="PSX Stock Screener & CrewAI Agents",
    page_icon="📈",
    layout="wide"
)

st.title("📈 PSX Stock Screener & CrewAI AI Agents")
st.markdown("Analyze PSX stock metrics and run multi-agent financial research powered by **CrewAI**.")

# ---------------------------------------------------------
# 2. Download Updated app.py
# ---------------------------------------------------------
try:
    with open(__file__, "r", encoding="utf-8") as f:
        app_code = f.read()

    st.sidebar.download_button(
        label="💾 Download Updated app.py",
        data=app_code,
        file_name="app.py",
        mime="text/x-python"
    )
except Exception:
    pass

# ---------------------------------------------------------
# 3. Sidebar Configuration & LLM Setup
# ---------------------------------------------------------
st.sidebar.header("⚙️ Configuration")

api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

llm = None
if api_key:
    try:
        # Initialize LLM directly through CrewAI's native LLM wrapper
        llm = LLM(
            model="gemini/gemini-2.5-flash",
            api_key=api_key,
            temperature=0.2
        )
        st.sidebar.success("CrewAI Gemini LLM Ready!")
    except Exception as e:
        st.sidebar.error(f"Error configuring LLM: {str(e)}")

# ---------------------------------------------------------
# 4. Data Loading & Interactive Screener
# ---------------------------------------------------------
uploaded_file = st.sidebar.file_uploader("Upload PSX CSV File", type=["csv"])

df = None
file_path = None

if uploaded_file is not None:
    # Save uploaded file temporarily for CrewAI CSVSearchTool access
    file_path = "temp_psx_data.csv"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    df = pd.read_csv(file_path)
    st.sidebar.success("Dataset uploaded successfully!")
elif os.path.exists("psx_stocks_data.csv"):
    file_path = "psx_stocks_data.csv"
    df = pd.read_csv(file_path)
    st.sidebar.info("Using default: `psx_stocks_data.csv`")

if df is not None:
    st.subheader("📊 Dataset Overview")
    st.dataframe(df.head(), use_container_width=True)

    # Filtering Sidebar
    st.sidebar.header("🎯 Screener Filters")

    if "MarketCap" in df.columns:
        min_mc, max_mc = float(df["MarketCap"].min()), float(df["MarketCap"].max())
        mc_range = st.sidebar.slider("Market Cap Range (Billions)", min_mc, max_mc, (5.0, 40.0))
        df = df[(df["MarketCap"] >= mc_range[0]) & (df["MarketCap"] <= mc_range[1])]

    if "PromoterHolding" in df.columns:
        min_promoter = st.sidebar.slider("Min Promoter Holding (%)", 0.0, 100.0, 60.0)
        df = df[df["PromoterHolding"] >= min_promoter]

    if "SalesGrowth" in df.columns:
        min_sales = st.sidebar.slider("Min Sales Growth (%)", -50.0, 200.0, 20.0)
        df = df[df["SalesGrowth"] >= min_sales]

    if "ProfitGrowth" in df.columns:
        min_profit = st.sidebar.slider("Min Profit Growth (%)", -50.0, 200.0, 20.0)
        df = df[df["ProfitGrowth"] >= min_profit]

    st.subheader("🔍 Screened Results")
    st.write(f"Matched **{len(df)}** companies:")
    st.dataframe(df, use_container_width=True)

    # ---------------------------------------------------------
    # 5. CrewAI Multi-Agent Execution Section
    # ---------------------------------------------------------
    st.markdown("---")
    st.subheader("🤖 Run CrewAI Financial Analysis")

    user_query = st.text_input(
        "Enter your research prompt for the CrewAI team:",
        value="Identify the top 3 PSX companies based on growth metrics and write a brief investment summary."
    )

    if st.button("🚀 Run Crew AI Agents"):
        if not llm:
            st.error("Please enter a valid Gemini API key in the sidebar.")
        elif not file_path:
            st.error("Data file path missing.")
        else:
            with st.spinner("CrewAI agents are collaborating..."):
                try:
                    # 1. Initialize Tool
                    csv_tool = CSVSearchTool(csv=file_path)

                    # 2. Define CrewAI Agents
                    data_analyst = Agent(
                        role="PSX Data Analyst",
                        goal="Analyze Pakistan Stock Exchange data and extract accurate metric insights.",
                        backstory="You are an expert financial analyst skilled at mining stock dataset files.",
                        tools=[csv_tool],
                        llm=llm,
                        verbose=True
                    )

                    investment_advisor = Agent(
                        role="Investment Strategist",
                        goal="Formulate actionable investment insights based on data analysis.",
                        backstory="You are a senior equity researcher specializing in emerging markets and PSX equities.",
                        llm=llm,
                        verbose=True
                    )

                    # 3. Define CrewAI Tasks
                    analysis_task = Task(
                        description=f"Search the CSV data and answer this query: {user_query}",
                        expected_output="A structured data summary with key metric figures and factual findings.",
                        agent=data_analyst
                    )

                    advisor_task = Task(
                        description="Review the data analysis output and generate a brief executive investment recommendation.",
                        expected_output="A professional bulleted summary highlighting stock strengths, risks, and outlook.",
                        agent=investment_advisor
                    )

                    # 4. Assemble and Run the Crew
                    psx_crew = Crew(
                        agents=[data_analyst, investment_advisor],
                        tasks=[analysis_task, advisor_task],
                        process=Process.sequential
                    )

                    result = psx_crew.kickoff()

                    st.success("Analysis Complete!")
                    st.markdown("### 📋 CrewAI Final Report")
                    st.write(str(result))

                except Exception as e:
                    st.error(f"CrewAI execution error: {str(e)}")

else:
    st.warning("Please upload a CSV file or place `psx_stocks_data.csv` in the root folder.")
