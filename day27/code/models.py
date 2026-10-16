from typing import List
from pydantic import BaseModel, Field

class InvestmentRecommendation(BaseModel):
    company_name: str
    ticker: str
    target_price_usd: float
    current_price_usd: float
    upside_potential_pct: float
    rating: str = Field(description="STRONG_BUY, BUY, HOLD, SELL")
    thesis_pillars: List[str]
    critical_risks: List[str]
    executive_memo: str
