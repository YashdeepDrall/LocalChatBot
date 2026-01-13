def analyze_response(question: str, answer: str) -> list[str]:
    """
    Analyzes the chatbot response to identify potential issues or specific patterns.
    Returns a list of flags based on the criteria.
    """
    flags = []
    answer_lower = answer.lower()

    # 1. Unable to answer
    unable_phrases = [
        "i don't know", "i cannot answer", "i can't answer", 
        "i am unable to answer", "i'm unable to answer",
        "i do not have enough information to answer"
    ]
    if any(phrase in answer_lower for phrase in unable_phrases):
        flags.append("unable_to_answer")

    # 4. Apology ("I apologize or sorry")
    apology_phrases = ["sorry", "apologize", "apologies", "pardon me"]
    if any(word in answer_lower for word in apology_phrases):
        flags.append("apology")

    # 5. Needs more information
    needs_info_phrases = [
        "need more information", "needs more information", 
        "provide more details", "please clarify", 
        "more context is needed", "could you provide"
    ]
    if any(phrase in answer_lower for phrase in needs_info_phrases):
        flags.append("needs_more_info")

    # 2 & 3. Wrong or Not Relevant
    # These are subjective and difficult to detect automatically without user feedback.
    # We can flag answers that express high uncertainty as a proxy.
    uncertainty_phrases = ["i am not sure", "i'm not sure", "might be", "could be"]
    if any(phrase in answer_lower for phrase in uncertainty_phrases):
        flags.append("uncertain_answer")
        
    return flags