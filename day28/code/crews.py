from models import InvestmentRecommendation

from config import VERBOSE
from crewai import Crew, Process

from agents import risk_officer_agent, chief_invenstment_officer_agent, equity_analyst_agent
from tasks import create_executive_memo_task, create_fundamental_research_task, create_risk_stress_test_task

import logging

logger = logging.getLogger(__name__)

class InvestmentCrews:
    def kickoff_research(self, ticker: str = "NVDA") -> InvestmentRecommendation:

        # format the ticker
        ticker = ticker.upper().strip()

        # collect the tasks
        fundamental_task = create_fundamental_research_task()
        risk_stress_task = create_risk_stress_test_task()
        executive_memo_task = create_executive_memo_task(fundamental_task, risk_stress_task)
        
        # create the crew
        crew = Crew(
            # CIO will use these agents
            agents=[equity_analyst_agent, risk_officer_agent],

            # the crew will be driven by CIO agent
            manager_agent=chief_invenstment_officer_agent,

            # tasks
            tasks=[fundamental_task, risk_stress_task, executive_memo_task],

            # since the hierarchical implementation is required to use the sub-agents 
            # by the main agent, set the process to the Process.hierarchical
            process=Process.hierarchical,
            verbose=VERBOSE
        )

        # kick off the crew
        result = crew.kickoff(inputs={"ticker": ticker})

        # get the final result
        final_result = result.tasks_output[-1]

        # read the pydantic structured output
        structured_output = getattr(final_result, "pydantic", None)

        # check if the structured_output is of InvestmentRecommendation type
        if isinstance(structured_output, InvestmentRecommendation):
            structured_output.ticker = ticker
            return structured_output

        logger.error("The final output is not of type InvestmentRecommendation")

        #TODO: fix this to return a default result
        return None




