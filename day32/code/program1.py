import json
import asyncio

from dotenv import load_dotenv
from openai import AsyncOpenAI

from ragas.llms import llm_factory
from ragas.embeddings.base import embedding_factory
from ragas.metrics.collections import AnswerRelevancy, Faithfulness

# load the env variables from .env file
load_dotenv()

async def main():
    # load the test data
    with open("./test_data.json") as file:
        data = json.load(file)

    # setup the evaluator model
    client = AsyncOpenAI()
    evaluator_model = llm_factory(model="gpt-4o-mini", client=client)
    embeddings = embedding_factory("openai", model="text-embedding-3-small", client=client)

    # create the metrics functions
    faithfulness = Faithfulness(llm=evaluator_model)
    answer_relevancy = AnswerRelevancy(llm=evaluator_model, embeddings=embeddings)

    # calculate the metrics for all the data instances
    for index, example in enumerate(data):
        # calculate faithfulness
        faithfulness_value = await faithfulness.ascore(
            user_input=example['user_input'],
            response=example['response'],
            retrieved_contexts=example['retrieved_contexts']
        )

        # calculate answer relevancy
        answer_relevancy_value = await answer_relevancy.ascore(
            user_input=example['user_input'],
            response=example['response']
        )

        print(f"[{index + 1}] Faithfulness = {faithfulness_value.value:.2f} | Answer Relevancy = {answer_relevancy_value.value:.2f}")
        print(f"    Question: {example['user_input']}")
        print(f"    Answer  : {example['response']}")
        print()

if __name__ == '__main__':
    asyncio.run(main=main())