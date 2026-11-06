from pydantic import BaseModel,Field

class LoanData(BaseModel):
    customer_name: str = Field(max_length=50,title='Name of the customer', description='Give the name of the customer')
    monthly_salary: float
    existing_monthly_debt: float
    requested_loan_amount: float
    loan_duration_months: int
    employment_status: str
    credit_score: int
    credit_history: str
    
class LoanValidationResult(BaseModel):
    is_valid: bool
    validation_errors: list[str]
    
class LoanRiskAssessment(BaseModel):
    risk_level: str
    recommendation: str
    risk_factors: list[str]