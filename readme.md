# 📈 AI Stock Equity Research & Multibagger Agent

A streamlined AI-powered stock research and evaluation tool built using **CrewAI**, **Groq (`openai/gpt-oss-120b`)**, **DuckDuckGo Search**, and **Streamlit**. 

This application uses a specialized AI agent to fetch real-time financial data, analyze fundamental and technical characteristics, estimate multibagger potential, and deliver actionable trading/investing recommendations (**BUY**, **HOLD**, **SELL**, or **INCREASE HOLDING**).

---

## 🌟 Features

- **Single-Agent Architecture**: Built on CrewAI for lightweight, high-performance agentic reasoning.
- **Powered by Groq**: Leverages the `openai/gpt-oss-120b` model via Groq's high-speed inference engine.
- **Real-Time Market Search**: Uses DuckDuckGo search integration to gather up-to-date fundamental metrics, technical trends, and earnings insights without requiring paid stock data API keys.
- **Multibagger Evaluation**: Evaluates Total Addressable Market (TAM), growth catalysts, competitive moats, and financial strength to gauge long-term upside.
- **Actionable Verdict**: Provides clear recommendation outputs (**BUY / HOLD / SELL / INCREASE HOLDING**).
- **Streamlit Web UI**: Simple, intuitive user interface ready for one-click deployment on Streamlit Community Cloud.

---

## 📂 Project Structure

```text
.
├── app.py              # Main Streamlit application entry point
├── tools.py            # Custom DuckDuckGo search tool definition for CrewAI
├── requirements.txt    # Project dependencies
├── .env                # Local environment key configuration (git-ignored)
└── README.md           # Project documentation
```

---

## 📋 Prerequisites

Before running the project locally or deploying to the cloud, ensure you have:

- **Python 3.10+** installed on your system.
- A **Groq API Key** (Get one for free at [console.groq.com](https://console.groq.com/)).

---

## 🚀 Local Setup & Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Create and Activate a Virtual Environment**
   - **Linux / macOS**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - **Windows**:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Run the Application**
   ```bash
   streamlit run app.py
   ```

---

## ☁️ Deployment to Streamlit Community Cloud

1. **Push Code to GitHub**:
   Ensure all files (`app.py`, `tools.py`, `requirements.txt`, `README.md`) are committed and pushed to a public or private GitHub repository. **Do not commit `.env`**.

2. **Deploy on Streamlit**:
   - Go to [share.streamlit.io](https://share.streamlit.io/).
   - Click **New app** and select your GitHub repository, branch, and `app.py` as the main file path.

3. **Configure Secrets**:
   - In your app's settings on Streamlit Cloud, go to **Advanced settings** -> **Secrets**.
   - Add your Groq API key in TOML format:
     ```toml
     GROQ_API_KEY = "your_groq_api_key_here"
     ```
   - Click **Save** and deploy.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).