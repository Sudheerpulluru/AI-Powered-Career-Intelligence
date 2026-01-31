def chatbot_response(message, history=None, context=None):
    """
    Personalized AI Career Assistant
    Uses dashboard prediction data (session-based)
    Mentor-safe, explainable, offline
    """

    if history is None:
        history = []

    if context is None:
        context = {}

    demand = context.get("demand")
    career_risk = (
        context.get("career_risk", {}).get("risk_category")
        if isinstance(context.get("career_risk"), dict)
        else None
    )
    ai_probability = context.get("ai_probability")

    if not message or not message.strip():
        return "Please ask something about careers, skills, or job trends 🙂"

    msg = message.lower().strip()

    # ===============================
    # FIRST MESSAGE
    # ===============================
    if len(history) == 0:
        return (
            "👋 Hi! I’m your **AI Career Assistant**.\n\n"
            "I analyze your job prediction results and help with:\n"
            "• Job demand insights\n"
            "• Career risk\n"
            "• AI takeover probability\n"
            "• Skill recommendations\n\n"
            "Ask me anything or use the quick buttons 👆"
        )

    # ===============================
    # JOB DEMAND (PERSONALIZED)
    # ===============================
    if "job demand" in msg or "my demand" in msg:
        if demand:
            return (
                f"📈 **Your Job Demand: {demand}**\n\n"
                "This means your role has strong market relevance.\n"
                "💡 Tip: Keep upgrading skills to maintain demand."
            )
        return "You haven’t generated a job prediction yet. Try predicting first 📊"

    # ===============================
    # CAREER RISK
    # ===============================
    if "career risk" in msg:
        if career_risk:
            return (
                f"⚠ **Your Career Risk: {career_risk}**\n\n"
                "This reflects stability based on automation, demand, and skills.\n"
                "Upskilling can reduce long-term risk."
            )
        return "Career risk is available after prediction. Please run it once."

    # ===============================
    # AI TAKEOVER RISK
    # ===============================
    if "ai" in msg or "automation" in msg:
        if ai_probability is not None:
            return (
                f"🤖 **AI Takeover Risk: {ai_probability}%**\n\n"
                "Higher risk roles benefit from creative, analytical, or leadership skills.\n"
                "AI augments careers—skills protect them."
            )
        return "AI risk will appear after running a job prediction."

    # ===============================
    # SKILLS
    # ===============================
    if "skill" in msg or "learn" in msg:
        return (
            "🧠 **Recommended Skills (India-focused):**\n"
            "• Python & SQL\n"
            "• Data Analysis / ML\n"
            "• Cloud (AWS / Azure)\n"
            "• Problem Solving\n\n"
            "Projects + consistency = growth 📈"
        )

    # ===============================
    # SALARY
    # ===============================
    if "salary" in msg or "ctc" in msg:
        return (
            "💰 **Average Salaries (India):**\n"
            "• Software Engineer: ₹6–12 LPA\n"
            "• Data Scientist: ₹8–18 LPA\n"
            "• Data Analyst: ₹5–10 LPA\n\n"
            "Actual salary depends on skills & experience."
        )

    # ===============================
    # HELP
    # ===============================
    if "help" in msg or "what can you do" in msg:
        return (
            "I can analyze:\n"
            "• Your job demand\n"
            "• Career risk\n"
            "• AI impact\n"
            "• Skill roadmap\n\n"
            "Ask anything career-related 🚀"
        )

    # ===============================
    # FALLBACK
    # ===============================
    return (
        "🤔 I didn’t fully understand that.\n\n"
        "Try asking:\n"
        "• What is my job demand?\n"
        "• What is my career risk?\n"
        "• Is my job safe from AI?\n"
        "• What skills should I learn?"
    )
