from crewai import Agent, LLM
from config import MODEL, MODEL_PROVIDER, VERBOSE
from tools import fetch_sec_filing_financials, calculate_dcf_valuation

 # create the llm
llm = LLM(
    model=f"{MODEL_PROVIDER}/{MODEL}"
)

class InvestmentAgentSpecifications:
    LEAD_DIRECTOR = {
        "role": "Chief Investment Officer & Committee Chair",
        "goal": "Synthesize deep fundamental research into an institutional-grade investment committee memo.",
        "backstory": "Veteran Wall Street CIO with 25 years overseeing multi-billion dollar tech growth portfolios."
    }

    EQUITY_ANALYST = {
        "role": "Principal Equity Research Analyst",
        "goal": "Extract financial filings, model DCF cash flows, and determine intrinsic target valuations.",
        "backstory": "Chartered Financial Analyst (CFA) specialized in semiconductor and AI infrastructure equities."
    }

    RISK_OFFICER = {
        "role": "Chief Risk & Geopolitical Officer",
        "goal": "Stress test valuation models against regulatory, geopolitical, and supply chain disruptions.",
        "backstory": "Quantitative risk manager with expertise in downside tail-risk scenario modeling."
    }


# build the agent using the metadata
def build_agent(spec: dict, tools=None, max_iteration: int=2):
    return Agent(
        role=spec['role'],
        goal=spec['goal'],
        backstory=spec['backstory'],
        tools=tools or [],
        llm=llm,
        max_iteration=max_iteration,
        verbose=VERBOSE
    )

# create the chief_investment_officer agent
chief_invenstment_officer_agent = build_agent(
    spec=InvestmentAgentSpecifications.LEAD_DIRECTOR,
    tools=[]
)

# create the equity_analyst agent
equity_analyst_agent = build_agent(
    spec=InvestmentAgentSpecifications.EQUITY_ANALYST,
    tools=[fetch_sec_filing_financials, calculate_dcf_valuation]
)

# create risk_officer_agent
risk_officer_agent = build_agent(
    spec=InvestmentAgentSpecifications.RISK_OFFICER,
    tools=[]
)