from models import InvestmentRecommendation
from tools import fetch_sec_filing_financials, calculate_dcf_valuation
from llm import call_real_llm
from config import MODEL

class InvestmentCrews:
    def kickoff_research(self, ticker: str = "NVDA") -> InvestmentRecommendation:
        fin = fetch_sec_filing_financials(ticker)
        dcf = calculate_dcf_valuation(fin["fy_revenue_billions"], fin["datacenter_growth_cagr_pct"], fin["gross_margin_pct"])
        
        curr_price = fin["current_price"]
        target_price = dcf["implied_share_price_usd"]
        upside = ((target_price - curr_price) / curr_price) * 100.0

        system_prompt = (
            f"You are the Chief Investment Officer & Committee Chair powered by '{MODEL}'. "
            "Draft a high-impact 3-point Investment Committee Memorandum for institutional investors."
        )
        user_content = f"Target: {fin['company']} ({ticker})\nCurrent: ${curr_price:.2f}, Target: ${target_price:.2f} (+{upside:.1f}%)\nRevenue: ${fin['fy_revenue_billions']}B, Growth: {fin['datacenter_growth_cagr_pct']}%, Gross Margin: {fin['gross_margin_pct']}%\nRisks: {', '.join(fin['risks'])}"

        # make a call to llm
        memo_text = call_real_llm(
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_content}]
        )

        return InvestmentRecommendation(
            company_name=fin["company"],
            ticker=ticker,
            target_price_usd=target_price,
            current_price_usd=curr_price,
            upside_potential_pct=round(upside, 1),
            rating="BUY" if upside > 15.0 else "HOLD",
            thesis_pillars=[
                f"Datacenter revenue CAGR of {fin['datacenter_growth_cagr_pct']}%",
                f"Industry leading gross margins at {fin['gross_margin_pct']}%",
                "Robust enterprise software & ecosystem moat"
            ],
            critical_risks=fin["risks"],
            executive_memo=memo_text
        )


