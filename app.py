import os
import streamlit as st
from dotenv import load_dotenv

# Patch CrewAI's cache breakpoint function for Groq compatibility
import crewai.llms.cache as _crewai_cache
_crewai_cache.mark_cache_breakpoint = lambda msg: msg

from crewai import Agent, Task, Crew, Process, LLM
from tools import duckduckgo_stock_search

load_dotenv()

st.set_page_config(page_title="PSX Stock Analyzer", page_icon="🇵🇰", layout="wide")
st.title("🇵🇰 Pakistan Stock Exchange (PSX) Equity Research Agent")

groq_api_key = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY"))

if not groq_api_key:
    st.error("GROQ_API_KEY missing. Please set it in Streamlit Cloud Secrets.")
    st.stop()

os.environ["GROQ_API_KEY"] = groq_api_key

share_name = st.text_input("Enter PSX Share Ticker or Name (e.g., HUBC, SYS, ENGRO, LUCK):")

if st.button("Analyze Stock", type="primary"):
    if not share_name.strip():
        st.warning("Please enter a stock symbol.")
    else:
        with st.spinner(f"Searching PSX market data for {share_name}..."):
            try:
                llm = LLM(
                    model="groq/openai/gpt-oss-120b",
                    temperature=0.2,
                    max_retries=5,
                    request_timeout=180
                )

                # PSX-focused Agent Definition
                psx_analyst = Agent(
                    role="Senior PSX Equity Analyst",
                    goal=f"Analyze financial metrics, announcements, technicals, and multibagger potential for Pakistani company '{share_name}' listed on PSX.",
                    backstory="Expert research analyst specializing in Pakistan Stock Exchange (PSX) equities, PKR valuations, local dividend yields, and macro catalysts.",
                    tools=[duckduckgo_stock_search],
                    llm=llm,
                    verbose=True,
                    allow_delegation=False,
                    max_iter=3
                )

                # Explicit Task Prompt
                analysis_task = Task(
                    description=(
                        f"Perform research on '{share_name}' listed on Pakistan Stock Exchange (PSX):\n"
                        f"1. Search for fundamental metrics in PKR (P/E, EPS growth, Net Revenue, Dividend Yield, Debt).\n"
                        f"2. Search for recent market price, support/resistance, and technical indicators.\n"
                        f"3. Evaluate multibagger potential (growth drivers, local catalysts, market share).\n"
                        f"4. Provide a definitive recommendation: BUY, HOLD, SELL, or INCREASE HOLDING."
                    ),
                    expected_output=(
                        "Markdown report:\n"
                        "- **Verdict**: BUY / HOLD / SELL / INCREASE HOLDING\n"
                        "- **Multibagger Rating**: High / Medium / Low (with local market context)\n"
                        "- **Fundamental Profile**: EPS, Revenue, Dividends, P/E ratio\n"
                        "- **Technical Profile**: Price trend, Support/Resistance zones\n"
                        "- **Key Risks**: Currency fluctuation, interest rates, circular debt, or policy risks"
                    ),
                    agent=psx_analyst
                )

                crew = Crew(
                    agents=[psx_analyst],
                    tasks=[analysis_task],
                    process=Process.sequential
                )

                result = crew.kickoff()

                st.success("Analysis Complete!")
                st.markdown("---")
                st.markdown(result.raw)

            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
