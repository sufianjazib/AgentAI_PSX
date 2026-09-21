import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from tools import duckduckgo_stock_search

# Load environment variables for local testing
load_dotenv()

st.set_page_config(
    page_title="Multibagger & Equity Research Agent",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Stock Equity Research & Multibagger Analysis Agent")
st.markdown("Powered by **CrewAI**, **Groq (`openai/gpt-oss-120b`)**, and **DuckDuckGo Search**.")

# 1. Obtain API Key strictly from Secrets / Environment Variables
groq_api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

# Stock Input Form
share_name = st.text_input("Enter Share / Ticker Symbol (e.g., AAPL, NVDA, RELIANCE, SYS.PSX):")

if st.button("Analyze Stock", type="primary"):
    if not groq_api_key:
        st.error("Missing Groq API Key! Please configure `GROQ_API_KEY` under Streamlit Cloud -> Settings -> Secrets.")
    elif not share_name.strip():
        st.warning("Please enter a valid share or ticker symbol.")
    else:
        with st.spinner(f"Analyzing {share_name}... Please wait as the AI agent gathers data."):
            try:
                # 2. Initialize Groq LLM with openai/gpt-oss-120b
                llm = LLM(
                    model="groq/openai/gpt-oss-120b",
                    api_key=groq_api_key,
                    temperature=0.2
                )

                # 3. Define the Single Agent
                stock_analyst = Agent(
                    role="Senior Equity & Technical Research Analyst",
                    goal=f"Conduct thorough fundamental and technical analysis for {share_name}, calculate multibagger potential, and give a clear action recommendation.",
                    backstory=(
                        "You are a top-tier hedge fund analyst specializing in stock fundamental metrics, technical patterns, "
                        "and identifying early multibagger growth stocks using real-time search data."
                    ),
                    tools=[duckduckgo_stock_search],
                    llm=llm,
                    verbose=True,
                    allow_delegation=False
                )

                # 4. Define Analysis Task
                analysis_task = Task(
                    description=(
                        f"Perform a comprehensive evaluation of the stock: '{share_name}'.\n"
                        f"1. Search DuckDuckGo for the latest fundamental metrics (P/E ratio, Revenue growth, Profit margins, Debt-to-Equity, Institutional holding).\n"
                        f"2. Search DuckDuckGo for technical indicators and trend health (RSI, Moving Averages, Support & Resistance levels).\n"
                        f"3. Evaluate the stock's Multibagger Potential based on TAM (Total Addressable Market), competitive moats, earnings trajectory, and key growth catalysts.\n"
                        f"4. Provide a definitive Action Recommendation strictly chosen from: BUY, HOLD, SELL, or INCREASE HOLDING."
                    ),
                    expected_output=(
                        "A structured Markdown report including:\n"
                        "- **Executive Summary & Verdict**: Recommended Action (BUY / HOLD / SELL / INCREASE HOLDING).\n"
                        "- **Multibagger Potential Rating**: (High / Medium / Low) with detailed rationale.\n"
                        "- **Fundamental Analysis**: Financial metrics, valuation, earnings growth, and debt structure.\n"
                        "- **Technical Analysis**: Trend direction, momentum indicators, key support and resistance zones.\n"
                        "- **Risk Assessment**: Major downside risks or key metrics to monitor."
                    ),
                    agent=stock_analyst
                )

                # 5. Form and Run Crew
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

# Patch CrewAI's cache breakpoint function so it doesn't send unsupported keys to Groq
import crewai.llms.cache as _crewai_cache
_crewai_cache.mark_cache_breakpoint = lambda msg: msg
# Initialize Groq LLM with max_retries and timeout configuration
llm = LLM(
    model="groq/openai/gpt-oss-120b",
    temperature=0.2,
    max_retries=5,          # Automatically retry when Groq throws 429 RateLimitError
    request_timeout=120     # Allow enough time for backoff delays
)
