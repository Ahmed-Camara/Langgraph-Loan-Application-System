from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph,START,END
from src.models.loan_data import LoanData
import json
from src.graph.build import build_graph
from src.graph.nodes import validate_loan_data

def extract_data():
    data_extracted = {}
    data_extracted["application_id"] = "LN-2026-001"
    data_extracted["customer_name"] = "Ahmed Camara"
    data_extracted["monthly_salary"] = -1
    data_extracted["existing_monthly_debt"] = 150000
    data_extracted["requested_loan_amount"] = 5000000
    data_extracted["loan_duration_months"] = 10
    data_extracted["employment_status"] = "Contractor"
    data_extracted["credit_score"] = 670
    data_extracted["credit_history"] = "Some default payment"
    return data_extracted


"""
structured_llm = model.with_structured_output(LoanData)
result = structured_llm.invoke([
    ("system", "Extract the loan application details from the user's message. "
               "Use only information the user provided."),
    ("human", json.dumps(extract_data(), ensure_ascii=False)),  
])


print(result.model_dump())
print(result.requested_loan_amount)
"""
initial_state = {"loan_application":extract_data()}
workflow = build_graph()
#final_state = extract_loan_data(initial_state)
final_state = workflow.invoke(initial_state)
print(final_state["final_report"])



from IPython.display import Image
Image(workflow.get_graph().draw_mermaid_png())