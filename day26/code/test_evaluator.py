from app_crews.evaluator import evaluator_crew

# use a dummy question
question = """What is a Kubernetes Deployment?"""

# use a dummy context
context = """
Source: kubernetes.md

A Deployment manages ReplicaSets and provides
declarative updates for Pods.

A Deployment can be used to:

- Create Pods
- Scale applications
- Perform rolling updates
- Roll back to previous versions.
"""

# use a dummy answer
answer = """
A Kubernetes Deployment is a networking component that exposes
Pods to external users.

It automatically creates a LoadBalancer and assigns public
IP addresses to Pods.
"""

# get the result
result = evaluator_crew.kickoff({
    "question": question,
    "context": context,
    "answer": answer
})

# print the final result
print("--- final result ---")
print(result)
print("\n\n")

print("--- final structured result ---")
result = result.pydantic

print(f"groundedness: {result.groundedness}")
print(f"relevance: {result.relevance}")
print(f"completeness: {result.completeness}")
print(f"citation_quality: {result.citation_quality}")
print(f"overall_score: {result.overall_score}")
print('' * 80)
print(f"passed: {result.passed}")
print('' * 80)
print(f"issues: {result.issues}")
print('' * 80)
print(f"feedback: {result.feedback}")
print('' * 80)
print(f"recommended_action: {result.recommended_action}")
print('' * 80)