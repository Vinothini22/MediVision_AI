import re


SECTION_QUESTIONS = {
    "impression": "What is the impression of this report?",
    "findings": "What are the main findings in this report?",
    "indication": "What is the reason for this examination?",
    "comparison": "What does the report say about previous examinations?"
}


def generate_suggested_questions(pages):
    """
    Generate suggested questions from available
    report sections. Does not invent medical findings.
    """

    if not pages:
        return []

    report_text = "\n".join(
        str(page.get("text", ""))
        for page in pages
    )

    suggestions = []

    for section, question in SECTION_QUESTIONS.items():

        pattern = rf"(?im)^\s*{re.escape(section)}\s*:"

        if re.search(pattern, report_text):
            suggestions.append(question)

    if report_text.strip():
        suggestions.append(
            "Summarize the main information in this report."
        )

    return suggestions