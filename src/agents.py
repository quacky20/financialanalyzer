from dotenv import load_dotenv
import os
from crewai import Agent, LLM
import litellm
from pathlib import Path
from langchain_community.chat_models import ChatLiteLLM

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

groq = os.getenv("GROQ_API_KEY")
# print(groq)

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.1
)

# response = litellm.completion(
#     model="groq/llama3-70b-8192",
#     messages=[{"role": "user", "content": "Hello, how are you?"}],
#     api_key=os.getenv("GROQ_API_KEY")
# )

# print(response)

# def call_groq_llm(prompt: str):
#     response = litellm.completion(
#         model="groq/llama3-70b-8192",
#         messages=[{"role": "user", "content": prompt}],
#         api_key=groq
#     )
#     return response["choices"][0]["message"]["content"]

financial_extractor = Agent(
    role="Financial Data Extractor",
    goal="Extract structured financial data from raw text",
    backstory="An expert in reading financial statements, financial reports and balance sheets with decades of experience and expertise.",
    allow_delegation=False,
    llm=llm
)

risk_analyzer = Agent(
    role="Risk Analysis Specialist",
    goal="Analyze financial risk based on extracted metrics.",
    backstory="An expert in financial risk management, portfolio analysis and credit risk with decades of experience and expertise.",
    allow_delegation=True,
    llm=llm
)

report_summarizer = Agent(
    role="Financial Report Summarizer",
    goal="Summarize extracted financial insights into a concise report.",
    backstory="An AI-driven financial analyst providing executive summaries for investors.",
    allow_delegation=False,
    llm=llm
)

agents = {
    "financial_extractor": financial_extractor,
    "risk_analyzer": risk_analyzer,
    "report_summarizer": report_summarizer
}
