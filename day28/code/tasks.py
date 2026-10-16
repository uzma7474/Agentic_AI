from crewai import Task
from models import InvestmentRecommendation

class InvestmentTasks:
    TASK_FUNDAMENTAL_RESEARCH = """
        Analyze SEC 10-K filings and financial telemetry for {ticker}.
        Extract gross margins, revenue CAGR, datacenter growth rates, and forward valuation multiples.
    """

    EXPECTED_FUNDAMENTAL_RESEARCH = (
        "A structured fundamental research report for the requested ticker with: verified "
        "fundamentals (company, current price, FY revenue, gross margin, growth CAGR, forward "
        "multiple), the DCF output (implied share price, WACC, terminal growth), the implied "
        "upside versus the current price, and the key risks listed."
    )

    TASK_RISK_STRESS_TEST = """
        Conduct comprehensive downside scenario stress testing for {ticker}.
        Quantify risks related to customer concentration, supply chain bottlenecks, and competitive alternatives.
    """

    EXPECTED_RISK_STRESS_TEST = (
        "A structured stress test report with: scenario descriptions, quantified revenue and "
        "margin impacts per scenario, probability-weighted expected impact, recommended "
        "mitigations, the identified company risks, and an overall risk rating."
    )

    TASK_EXECUTIVE_MEMO = """
        Synthesize findings from the Fundamental Analyst and Risk Officer into a final
        Investment Committee Recommendation Memo including Target Price, Upside %, Rating, Thesis Pillars, and Risk Mitigation.
    """

    EXPECTED_EXECUTIVE_MEMO = (
        "A complete InvestmentCommittee recommendation for the ticker: company and ticker, "
        "current and target price, upside percentage, a single rating "
        "(STRONG_BUY/BUY/HOLD/SELL), three concise thesis pillars, the critical risks carried "
        "over from the stress test, and a 3-point executive memo ready for institutional "
        "distribution."
    )

# create a task for fundamental research
def create_fundamental_research_task():
    return Task(
        name="Fundamental Research",
        description=InvestmentTasks.TASK_FUNDAMENTAL_RESEARCH,
        expected_output=InvestmentTasks.EXPECTED_FUNDAMENTAL_RESEARCH
    )

# create a task for performing the risk analysis 
def create_risk_stress_test_task():
    return Task(
        name="Risk Stress Test",
        description=InvestmentTasks.TASK_RISK_STRESS_TEST,
        expected_output=InvestmentTasks.EXPECTED_RISK_STRESS_TEST
    )

# create a task for execute memo
def create_executive_memo_task(fundamental_task: Task, risk_task: Task):
    return Task(
        name="Executive Recommendation Memo",
        description=InvestmentTasks.TASK_EXECUTIVE_MEMO,
        expected_output=InvestmentTasks.EXPECTED_EXECUTIVE_MEMO,

        # structured output
        output_pydantic=InvestmentRecommendation,

        # read the contents from both the tasks
        context=[fundamental_task, risk_task]
    )