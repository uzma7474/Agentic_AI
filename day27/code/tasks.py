class InvestmentTasks:
    TASK_FUNDAMENTAL_RESEARCH = """
        Analyze SEC 10-K filings and financial telemetry for {ticker}.
        Extract gross margins, revenue CAGR, datacenter growth rates, and forward valuation multiples.
    """

    TASK_RISK_STRESS_TEST = """
        Conduct comprehensive downside scenario stress testing for {ticker}.
        Quantify risks related to customer concentration, supply chain bottlenecks, and competitive alternatives.
    """

    TASK_EXECUTIVE_MEMO = """
        Synthesize findings from the Fundamental Analyst and Risk Officer into a final
        Investment Committee Recommendation Memo including Target Price, Upside %, Rating, Thesis Pillars, and Risk Mitigation.
    """
