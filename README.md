# 🤖 AI Data Analyst Agent

A web app that lets you **chat with your CSV files** using AI. Upload any dataset → ask questions in plain English → get an instant dashboard and an AI-written executive report.

![banner](https://img.shields.io/badge/Python-3.13-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.63-red) ![Gemini](https://img.shields.io/badge/Google-Gemini-orange) ![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features
- 📁 CSV file upload (up to 200MB)
- 💬 Conversational Q&A powered by Google Gemini
- 📊 Multi-chart dashboard: KPIs, histograms, bar charts, trends, correlation heatmaps
- 🔮 Auto-generated AI insights report
- 🎁 Sample dataset included for instant testing
- 🌐 100% browser-based — no install needed

  Live at https://ai-data-analyst-agent-prachi.streamlit.app


## 🛠️ Tech Stack
Python · Streamlit · Google Gemini API · Plotly · Pandas

## 🚀 Quick Start
```bash
pip install -r requirements.txt
echo "GOOGLE_API_KEY=your_key" > .env
streamlit run app.py
