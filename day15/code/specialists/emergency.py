def run_emergency_agent(user_query: str):
    return """**EMERGENCY GUIDANCE**

        Based on your description, this situation may require immediate medical attention.

        **If you or someone else is experiencing a medical emergency:**

        1. **Call 911** (or your local emergency number) immediately
        2. **Go to the nearest Emergency Room**
        3. **Do not attempt to drive yourself** — call an ambulance or have someone drive you

        **While waiting for emergency services:**
        - Stay calm and try to remain still
        - If you're with someone, have them stay with you
        - If you have known medications (e.g., an EpiPen, nitroglycerin), use as directed
        - Do not eat or drink anything
        - Note when symptoms started and any changes

        **Common Emergency Symptoms:**
        - Chest pain or pressure
        - Difficulty breathing or shortness of breath
        - Sudden severe headache ("worst headache of your life")
        - Uncontrolled bleeding
        - Loss of consciousness or seizure
        - Signs of stroke (FAST: Face drooping, Arm weakness, Speech difficulty, Time to call 911)
        - Severe allergic reaction (swelling, difficulty breathing, hives)
        - Sudden confusion or difficulty speaking

        **Important:** This system is for educational and informational purposes only. It does NOT provide medical diagnosis or treatment. Always seek professional medical help for emergencies.

        ---

        *If this is not an emergency but you need urgent care, consider visiting an urgent care clinic or calling your healthcare provider's nurse hotline.*
    """
