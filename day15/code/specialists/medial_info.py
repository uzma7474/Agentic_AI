from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
from config import MODEL, MODEL_PROVIDER

MEDICAL_KNOWLEDGE = {
    "mri": {
        "title": "MRI (Magnetic Resonance Imaging)",
        "content": (
            "MRI uses strong magnetic fields and radio waves to create detailed images of organs and tissues. "
            "It does not use ionizing radiation (unlike X-rays or CT scans). Common uses include imaging the brain, "
            "spinal cord, joints, and abdominal organs. An MRI scan typically takes 30-60 minutes. "
            "Patients with certain metal implants or pacemakers may not be able to have an MRI."
        ),
    },
    "hba1c": {
        "title": "HbA1c (Hemoglobin A1c)",
        "content": (
            "HbA1c is a blood test that measures average blood sugar levels over the past 2-3 months. "
            "It shows what percentage of hemoglobin is coated with sugar (glycated). Normal: below 5.7%, "
            "Pre-diabetes: 5.7% to 6.4%, Diabetes: 6.5% or higher. The test requires no fasting and is "
            "typically done every 3-6 months for people with diabetes."
        ),
    },
    "fasting": {
        "title": "Fasting Before Blood Tests",
        "content": (
            "Fasting means not eating or drinking anything (except water) for 8-12 hours before a blood test. "
            "It is required for tests that measure blood sugar, lipids (cholesterol, triglycerides), and some "
            "other metabolic markers. Fasting ensures that recent food intake does not affect test results. "
            "You can usually drink water during the fasting period. Always follow your healthcare provider's "
            "specific instructions."
        ),
    },
    "blood_pressure": {
        "title": "Blood Pressure",
        "content": (
            "Blood pressure measures the force of blood pushing against artery walls. It has two numbers: "
            "systolic (top, when heart beats) and diastolic (bottom, when heart rests). Normal: less than "
            "120/80 mmHg. Elevated: 120-129/<80. High Blood Pressure Stage 1: 130-139/80-89. "
            "High Blood Pressure Stage 2: 140+/90+. Hypertensive Crisis: 180+/120+ (seek emergency care)."
        ),
    },
    "cholesterol": {
        "title": "Cholesterol",
        "content": (
            "Cholesterol is a waxy substance in your blood. HDL ('good') cholesterol helps remove excess. "
            "LDL ('bad') cholesterol can build up in arteries. Total cholesterol: Desirable < 200 mg/dL, "
            "Borderline high 200-239, High 240+. LDL: Optimal < 100, Near optimal 100-129, Borderline high "
            "130-159, High 160-189, Very high 190+. HDL: High (protective) 60+, Low < 40."
        ),
    },
    "ecg": {
        "title": "ECG/EKG (Electrocardiogram)",
        "content": (
            "An ECG records the electrical activity of the heart. Small electrodes are placed on the chest, "
            "arms, and legs. The test takes about 5-10 minutes and is painless. It detects heart rhythm "
            "abnormalities, heart attacks, enlarged heart, and electrolyte imbalances. It is a common, "
            "non-invasive diagnostic tool."
        ),
    },
}

@tool
def search_medical_info(query: str) -> str:
    """Search for general medical information. Provide a keyword like 'mri', 'hba1c', 'fasting', 'blood pressure', 'cholesterol', or 'ecg'."""
    query_lower = query.lower().strip()
    for key, info in MEDICAL_KNOWLEDGE.items():
        if key in query_lower or query_lower in key:
            return f"{info['title']}:\n\n{info['content']}"
    topics = ", ".join(MEDICAL_KNOWLEDGE.keys())
    return f"Information not found for '{query}'. Available topics: {topics}"


MEDICAL_INFO_SYSTEM = """You are a helpful healthcare information assistant. You provide GENERAL
educational information only. You do NOT diagnose conditions, prescribe treatments, or replace
professional medical advice. Always recommend consulting a healthcare provider for personal medical
concerns. Use the search_medical_info tool to look up reliable medical information."""


def run_medical_info_agent(query: str) -> str:
    """Run the LangChain-based medical information agent."""
    llm = init_chat_model(model=MODEL, model_provider=MODEL_PROVIDER, temperature=0)
    llm_with_tools = llm.bind_tools([search_medical_info])

    messages = [
        SystemMessage(content=MEDICAL_INFO_SYSTEM),
        HumanMessage(content=query),
    ]
    response = llm_with_tools.invoke(messages)

    if hasattr(response, "tool_calls") and response.tool_calls:
        tool_results = []
        for tc in response.tool_calls:
            if tc["name"] == "search_medical_info":
                result = search_medical_info.invoke(tc["args"])
                tool_results.append(result)
        context = "\n\n".join(tool_results)
        final_messages = [
            SystemMessage(content=MEDICAL_INFO_SYSTEM),
            HumanMessage(content=f"User question: {query}\n\nRetrieved information:\n{context}\n\nPlease provide a clear, helpful response based on this information."),
        ]
        final_response = llm.invoke(final_messages)
        return final_response.content

    return response.content
