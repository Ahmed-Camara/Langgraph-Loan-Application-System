from src.graph.state import LoanState
from langchain_openai import ChatOpenAI
from src.models.loan_data import LoanData,LoanValidationResult,LoanRiskAssessment
import json

model = ChatOpenAI(model="qwen3.6-35b-fp8",api_key="DUMMY",
                 temperature = 0,base_url = "http://10.30.60.20:8000/v1")

def extract_loan_data(state: LoanState) -> dict:
    loan_application = state["loan_application"]
    structured_llm = model.with_structured_output(LoanData)
    result = structured_llm.invoke([
        ("system", "Extract the loan application details from the user's message. "
                "Use only information the user provided."),
        ("human", json.dumps(loan_application, ensure_ascii=False)),  
    ])
    state["extracted_data"] = result.model_dump()
    return state




def validate_loan_data(state: LoanState) -> dict:
    
    extracted_data = state["extracted_data"]
    prompt = (f"You are a data loan validator expert for a bank."
                f"Your task is to validate a json data received according to these rules"
                f"Monthly salary is greater than zero."
                f"Loan amount is greater than zero."
                f"Loan duration is greater than zero."
                f"Credit score is between 300 and 850."
                f"the output should be a json in this format for example: {{'is_valid': True,'validation_errors': []}}"
                f"CONTEXT : {extracted_data} "
                f"Answer must always be in french"
                )
    validator = model.with_structured_output(LoanValidationResult)
    result = validator.invoke(prompt)
    result = result.model_dump()
    
    state["is_valid"] = result["is_valid"]
    state["validation_errors"] = result["validation_errors"]
    return state

def financial_analysis(state: LoanState) -> dict:

    data = state["extracted_data"]

    monthly_salary = data["monthly_salary"]
    existing_monthly_debt = data["existing_monthly_debt"]
    loan_amount = data["requested_loan_amount"]
    loan_duration = data["loan_duration_months"]

    monthly_payment = loan_amount / loan_duration

    total_monthly_debt = (
        existing_monthly_debt + monthly_payment
    )

    
    dti = (
        total_monthly_debt / monthly_salary
    ) * 100

    disposable_income = (
        monthly_salary - total_monthly_debt
    )

    total_repayment = (
        monthly_payment * loan_duration
    )

    total_interest = (
        total_repayment - loan_amount
    )
    
    result = {}
    result["estimated_monthly_payment"] = round(monthly_payment, 2)
    result["total_monthly_debt"] = round(total_monthly_debt, 2)
    result["debt_to_income_ratio"] = round(dti, 2)
    result["disposable_monthly_income"] = round(disposable_income, 2)
    result["total_repayment"] = round(total_repayment, 2)
    result["total_interest"] = round(total_interest, 2)
    
    state["financial_analysis"] = result

    return state

def risk_assessment(state: LoanState) -> dict:
    prompt = (
        f"You are risk assessment expert for a bank "
        f"your goal is to assess the risk of granting a loan to a customer based on rules below : \n"
        f"- if DTI <= 35 then acceptable\n"
        f"- if Credit score >= 700 then acceptable\n"
        f"- if Employment = 'permanent' then acceptable\n"
        f"- if Credit history = 'No defaults' then acceptable\n"
        f"you will receive a json data of global and financial analysis on this customer "
        f"CONTEXT: \n {state} "
        f"Answer must always be in french"
    )
    
    validator = model.with_structured_output(LoanRiskAssessment)
    result = validator.invoke(prompt)
    result = result.model_dump()
    
    state["risk_assessment"] = result
    return state

def generate_report(state: LoanState) -> dict:
    prompt = (
        f"You are a Senior Banking Credit Analyst specialized in financial analysis, credit risk assessment, and loan application evaluation "
        f"Your task is to generate a professional credit assessment report based exclusively on the information provided in the input data. "
        f"You must synthesize the customer's financial information, financial analysis results, and credit risk assessment into a structured report. "
        f"**STRICT RULES**\n"
        f"1. Use only the information explicitly provided in the input data.\n"
        f"2. Never invent, assume, estimate, or modify financial figures.\n"
        f"3. Never perform additional financial calculations. All financial calculations have already been performed by the Financial Analysis node.\n"
        f"4. Do not modify the risk level or recommendation provided by the Risk Assessment node.\n"
        f"5. Do not independently approve or reject a loan.\n"
        f"6. Do not introduce financial indicators that are not present in the input.\n"
        f"7. Provide a clear and factual justification for the recommendation using the available financial indicators and risk factors.\n"
        f"8. The report must be professional, concise, objective, and suitable for a banking credit officer.\n"
        f"CONTEXT : \n{state} "
        f"Answer must always be in french"
    )
    
    result = model.invoke(prompt).content
    
    state["final_report"] = result
    
    return state