from test_generator import generate_answer

from app_crews.evaluator import evaluator_crew

def run_rag_evaluation(question: str):
    # iteration = 1
    # while:

    # step 1: generate the answer using generator
    result = generate_answer(question)

    # get the result splitted into parts
    context = result['context']
    answer = result['answer']

    # pass the generated result to the evaluator to evaluate
    final_result = evaluator_crew.kickoff(inputs={
        "question": question,
        "context": context,
        "answer": answer
    })

    # read the result 
    result = final_result.pydantic
    print(f"groundedness: {result.groundedness}")
    print(f"relevance: {result.relevance}")
    print(f"completeness: {result.completeness}")
    print(f"citation_quality: {result.citation_quality}")
    print(f"overall_score: {result.overall_score}")
    print('-' * 80)
    print(f"passed: {result.passed}")
    print('-' * 80)
    print(f"issues: {result.issues}")
    print('-' * 80)
    print(f"feedback: {result.feedback}")
    print('-' * 80)
    print(f"recommended_action: {result.recommended_action}")
    print('-' * 80)

    # if result.recommended_action == 'PASS':
    #     break
    # elif no_iterations >= threshold:
    #     break
 
if __name__ == '__main__':
    run_rag_evaluation('What is a Kubernetes Deployment?')