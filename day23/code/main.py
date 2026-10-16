import config
import asyncio
from supervisor import build_workflow

async def main():
    # build the workflow
    workflow = build_workflow()

    # Prepare the query to pass it a parameter 
    query = (
        "Plan a 7-day trip to Goa in December 2026 for 3 people from Pune. "
        "We love food and hiking. "
        "Show flights, hotels, activities, and the total budget."
    )

    # execute the workflow
    async for event in workflow.run(query, stream=True):
        # get the event type
        event_type = getattr(event, "type", "unknown")
        print(f"[{event_type}]")

        # check if the event type is final one
        if event_type == 'output':
            print("\n\n")
            print("--- final result ---")
            print(str(getattr(event, "data")))
            

if __name__ == '__main__':
    asyncio.run(main=main())