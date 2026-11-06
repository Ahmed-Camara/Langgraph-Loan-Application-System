from langgraph.graph import StateGraph, START,END
from src.graph.state import LoanState
from src.graph.nodes import extract_loan_data,validate_loan_data,financial_analysis,risk_assessment,generate_report
def build_graph():
    graph = StateGraph(LoanState)
    
    graph.add_node("extract_loan_data",extract_loan_data)
    graph.add_node("validate_loan_data",validate_loan_data)
    graph.add_node("financial_analysis",financial_analysis)
    graph.add_node("risk_assessment",risk_assessment)
    graph.add_node("generate_report",generate_report)
    
    graph.add_edge(START,"extract_loan_data")
    graph.add_edge("extract_loan_data","validate_loan_data")
    graph.add_edge("validate_loan_data","financial_analysis")
    graph.add_edge("financial_analysis","risk_assessment")
    graph.add_edge("risk_assessment","generate_report")
    graph.add_edge("generate_report",END)
    
    workflow = graph.compile()
    
    return workflow