import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from tools import duckduckgo_stock_search

# Load environment variables from local .env if available
load_dotenv()

st.set_page_config(
    page_title="Multibagger & Equity Research Agent",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Stock Equity Research & Multibagger Analysis Agent")
st.markdown("Powered by **CrewAI**, **Groq (`openai/gpt-oss-120b`)**, and **DuckDuckGo Search**.")

# Sidebar API Key Configuration
with st.sidebar:
    st.header("Configuration")
    groq_api_key = st.text_input("Groq API Key", type="password", help="Enter your Groq API key")
    if groq_api_key:
        os.environ["GROQ_API_KEY"] = groq_api_key

# Stock Input Form
share_name = st.text_input("Enter Share / Ticker Symbol (e.g., AAPL, NVDA, RELIANCE, SYS.PSX):")

if st.button("Analyze Stock", type="primary"):
    if not os.environ.get("GROQ_API_KEY"):
        st.error("Please provide a valid Groq API key in the sidebar or environment variables.")
    elif not share_name.strip():
        st.warning("Please enter a stock or ticker name.")
    else:
        with st.spinner(f"Analyzing {share_name}... Please wait as the AI agent conducts research."):
            try:
                # 1. Initialize Groq LLM with openai/gpt-oss-120b
                llm = LLM(
                    model="groq/openai/gpt-oss-120b",
                    temperature=0.2
                )

                # 2. Define the Single Agent
                stock_analyst = Agent(
                    role="Senior Equity & Technical Research Analyst",
                    goal=f"Conduct thorough fundamental and technical analysis for {share_name}, calculate multibagger potential, and provide a definitive recommendation.",
                    backstory=(
                        "You are a top-tier hedge fund analyst specializing in stock fundamental metrics, technical trend patterns, "
                        "and identifying early multibagger growth stocks using real-time search data."
                    ),
                    tools=[duckduckgo_stock_search],
                    llm=llm,
                    verbose=True,
                    allow_delegation=False
                )

                # 3. Define the Analysis Task
                analysis_task = Task(
                    description=(
                        f"Perform a comprehensive evaluation of the stock: '{share_name}'.\n"
                        f"1. Search DuckDuckGo for the latest stock fundamental metrics (P/E ratio, Revenue growth, Profit margins, Debt-to-Equity, Institutional holding).\n"
                        f"2. Search DuckDuckGo for current technical indicators and trend health (RSI, Moving Averages, Support & Resistance levels).\n"
                        f"3. Evaluate the stock's Multibagger Potential based on TAM (Total Addressable Market), competitive moat, earnings trajectory, and key growth catalysts.\n"
                        f"4. Provide a definitive Action Recommendation chosen strictly from: BUY, HOLD, SELL, or INCREASE HOLDING."
                    ),
                    expected_output=(
                        "A structured Markdown report including:\n"
                        "- **Executive Summary & Verdict**: Recommended Action (BUY / HOLD / SELL / INCREASE HOLDING).\n"
                        "- **Multibagger Potential Rating**: (High / Medium / Low) with detailed rationale.\n"
                        "- **Fundamental Analysis**: Key financial metrics, valuation, earnings growth, and debt structure.\n"
                        "- **Technical Analysis**: Trend direction, momentum indicators, key support and resistance zones.\n"
                        "- **Risk Assessment**: Major downside risks or key metrics to monitor."
                    ),
                    agent=stock_analyst
                )

                # 4. Form and Run the Crew
                crew = Crew(
                    agents=[stock_analyst],
                    tasks=[analysis_task],
                    process=Process.sequential
                )

                result = crew.kickoff()

                # Display Results
                st.success("Analysis Complete!")
                st.markdown("---")
                st.markdown(result.raw)

            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")