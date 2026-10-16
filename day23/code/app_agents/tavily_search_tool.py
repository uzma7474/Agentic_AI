from langchain_tavily import TavilySearch
import logging

# create logging instance
logger = logging.getLogger(__name__)

def tavily_search(query: str, max_results: int = 4):
    """search using tavily API"""

    # create an object of tavily search
    t_search = TavilySearch(
        max_results=max_results,
        include_answer=True,
        topic="general",
        search_depth="basic"
    )

    # get the result calling the tavily search API
    results = t_search.invoke({"query": query})

    # format the result
    format_result = lambda result: {
        "title": result['title'], 
        "url": result['url'],
        "content": result['content']
    }

    # return the result in a proper structure
    final_result = {
        "query": query,
        "answer": results.get("answer"),
        "results": [format_result(r) for r in results.get('results', [])]
    }
    logger.info(final_result)

    return final_result