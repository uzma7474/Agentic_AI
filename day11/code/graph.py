from langgraph.graph import START, END, StateGraph
from state import State
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage
from prompts import planner_system_prompt, planner_user_prompt, executor_system_prompt, executor_user_prompt, final_system_prompt, final_user_prompt
from langchain_tavily import TavilySearch

import os
import logging

# create logger
logger = logging.getLogger(__name__)

# load the model and provider
model = os.getenv('MODEL', 'qwen2.5:7b')
model_provider = os.getenv('MODEL_PROVIDER', 'ollama')

# create the llm
llm = init_chat_model(model=model, model_provider=model_provider)

# create tavily search tool
search_tool = TavilySearch(max_results=5,topic="general")

def planner(state: State):
    logger.info(f"planning the research steps. {state}")

    # send the user request and get the response
    response = llm.invoke([
        SystemMessage(content=planner_system_prompt),
        HumanMessage(content=planner_user_prompt.format(user_request=state['user_request']))
    ])
    logger.info(response.content)

    # process the response
    steps = []
    for line in response.content.strip().split('\n'):
        line = line.strip()
        if not line:
            continue

        # TODO: add the logic to remove the number (like 1.) from the line
        steps.append(line)

    logger.info(f"after cleansing we have #{len(steps)} number of steps")
    logger.info('')

    # return updated state
    return {
        "plan": steps,
        "current_step": 0,
        "execution_result": []
    }

def executor(state: State):

    # get the state members
    step_index = state['current_step']
    step = state['plan'][step_index]
    total_steps = len(state['plan'])

    logger.info(f"executor started execution job for step {step_index}/{total_steps}")
    logger.info(f"executing step: {step}")

    # send the request to the model
    response = llm.invoke([
        SystemMessage(content="""
        Convert the current step into a valid web search query.
        Return the search query ONLY. Nothing else.
        """),
        HumanMessage(content=step)
    ])
    search_query = response.content.strip()
    logger.info(f"search query = {search_query}")

    # search on internet for the real time result
    result = search_tool.invoke(search_query)

    # grab all the results
    parts = []
    for r in result['results']:
        title = r['title']
        content = r['content']
        parts.append(f"title: {title}, content: {content}")

    logger.info("summarizing the results")

    # get the results summarized
    summarized_result = llm.invoke([
        SystemMessage(content=executor_system_prompt),
        HumanMessage(content=executor_user_prompt.format(
            step=step, search_results=parts
        ))
    ])

    # create the final result of this step
    step_final_result = summarized_result.content.strip()

    # append the result to the state
    execution_results = list(state['execution_result'])
    execution_results.append(
        f"step: {step}\nresult: {step_final_result}"
    )
    
    return {
        "execution_result": execution_results,
        "current_step": step_index + 1
    }
    
def final_result(state: State):
    logger.info("generating the final result")

    # generate the final result using LLM
    result = llm.invoke([
        SystemMessage(content=final_system_prompt),
        HumanMessage(content=final_user_prompt.format(
            user_request=state['user_request'],
            plan="\n".join(state['plan']),
            results=state["execution_result"]
        ))        
    ])
    logger.info('')

    return {
        "final_result": result.content.strip()
    }

def route(state: State):
    # decide whether to generate the final result 
    # or continue calling executor to execute the next step
    if state['current_step'] < len(state['plan']):
        return "executor"
    return "final"

def create_graph():

    # create a graph
    graph = StateGraph(State)

    # add the nodes
    graph.add_node("planner", planner)
    graph.add_node("executor", executor)
    graph.add_node("final", final_result)

    # add the edges
    graph.add_edge(START, "planner")
    graph.add_edge("planner", "executor")
    graph.add_conditional_edges(
        "executor", route, {"executor": "executor", "final": "final"})
    graph.add_edge("final", END)

    # compile the graph
    app = graph.compile()

    # create an image 
    image = app.get_graph().draw_mermaid_png()
    with open("image.png", "wb") as file:
        file.write(image)

    return app