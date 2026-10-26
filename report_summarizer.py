import re


SECTION_LABELS = {
    "indication": "Reason for Examination",
    "comparison": "Previous Examination",
    "findings": "Main Findings",
    "impression": "Report Impression"
}


def extract_report_sections(text):
    """
    Extract existing labelled sections from a report.
    No new medical findings are generated.
    """

    pattern = re.compile(
        r"(?im)^\s*(Indication|Comparison|Findings|Impression)\s*:\s*"
    )

    matches = list(pattern.finditer(text))
    sections = {}

    for index, match in enumerate(matches):

        name = match.group(1).lower()

        start = match.end()

        end = (
            matches[index + 1].start()
            if index + 1 < len(matches)
            else len(text)
        )

        content = text[start:end].strip()

        if content:
            sections[name] = content

    return sections


def summarize_report(pages):
    """
    Return a structured, extractive summary.
    """

    summary = []

    for page in pages:

        text = page.get("text", "").strip()

        if not text:
            continue

        sections = extract_report_sections(text)

        for name, label in SECTION_LABELS.items():

            if name in sections:

                summary.append({
                    "title": label,
                    "text": sections[name],
                    "page": page["page"]
                })

    return summary