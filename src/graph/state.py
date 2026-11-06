from typing import TypedDict
from pydantic import Field
class LoanState(TypedDict):
    loan_application: dict = Field(default={})
    extracted_data: dict = Field(default={})
    is_valid: bool = Field(default=False)
    validation_errors: list = Field(default=None)
    financial_analysis: dict = Field(default={})
    risk_assessment: dict = Field(default={})
    final_report: dict = Field(default={})