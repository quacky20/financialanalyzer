from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from crewai import Task, Crew
from agents import agents

# ✅ Define tasks for each agent
extract_task = Task(
    description="Extract structured financial data from the provided raw text.",
    agent=agents["financial_extractor"]
)

risk_task = Task(
    description="Analyze financial risks based on extracted data.",
    agent=agents["risk_analyzer"]
)

summary_task = Task(
    description="Summarize financial insights into a concise executive report.",
    agent=agents["report_summarizer"]
)

# ✅ Define function to execute tasks properly
def extract_financial_data(state):
    crew = Crew(agents=[agents["financial_extractor"]], tasks=[extract_task])
    extracted_data = crew.kickoff(inputs={"raw_text": state["raw_text"]})
    return {**state, "extracted_data": extracted_data}

def perform_risk_analysis(state):
    crew = Crew(agents=[agents["risk_analyzer"]], tasks=[risk_task])
    risk_analysis = crew.kickoff(inputs={"extracted_data": state["extracted_data"]})
    return {**state, "risk_analysis": risk_analysis}

def summarize_financial_report(state):
    crew = Crew(agents=[agents["report_summarizer"]], tasks=[summary_task])
    summary = crew.kickoff(inputs={"risk_analysis": state["risk_analysis"]})
    return {**state, "summary": summary}

# ✅ Setup the LangGraph workflow
checkpoint = MemorySaver()
graph = StateGraph(dict)

graph.add_node("extract_data", extract_financial_data)
graph.add_node("risk_analysis", perform_risk_analysis)
graph.add_node("summarize", summarize_financial_report)

graph.set_entry_point("extract_data")
graph.add_edge("extract_data", "risk_analysis")
graph.add_edge("risk_analysis", "summarize")

workflow = graph.compile(checkpointer=checkpoint)

# ✅ Function to run the pipeline
def run_financial_pipeline(raw_text, thread_id="1"):
    state = {"raw_text": raw_text}
    result = workflow.invoke(state, config={"configurable": {"thread_id": thread_id}})
    return result  # Returning full state

# ✅ Execution
if __name__ == "__main__":
    with open('data/raw_reports/matched_pages.txt', 'r', encoding='utf-8') as file:
        sample_text = file.read()
    
    final_state = run_financial_pipeline(sample_text, thread_id="12345")

    print("\n🔍 Extracted Financial Data:\n", final_state["extracted_data"])
    print("\n⚠️ Risk Analysis:\n", final_state["risk_analysis"])
    print("\n📄 Final Financial Summary:\n", final_state["summary"])
