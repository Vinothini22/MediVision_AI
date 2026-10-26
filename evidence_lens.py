import re
from difflib import SequenceMatcher


def normalize(text):
    return re.sub(r"\s+", " ", str(text or "")).strip()


def sentences(text):
    return [
        item.strip()
        for item in re.split(r"(?<=[.!?])\s+", normalize(text))
        if item.strip()
    ]


def find_evidence(pages, evidence):
    """
    Locate supporting evidence in the original report.
    Return the original sentence and its source page.
    """
    target = normalize(evidence)

    if not target:
        return None

    # First: exact evidence match.
    for page in pages:
        original = str(page.get("text", ""))
        if target.lower() in normalize(original).lower():
            return {
                "page": page.get("page", 1),
                "evidence": target,
                "match_type": "Exact"
            }

    # Second: find the closest original sentence.
    best = None
    best_score = 0.0

    for page in pages:
        for sentence in sentences(page.get("text", "")):
            score = SequenceMatcher(
                None,
                target.lower(),
                sentence.lower()
            ).ratio()

            if score > best_score:
                best_score = score
                best = {
                    "page": page.get("page", 1),
                    "evidence": sentence,
                    "match_type": "Approximate"
                }

    if best and best_score >= 0.80:
        return best

    return None


def verify_answer(answer, evidence_result):
    """
    Conservative evidence verification.

    Verified means the answer is directly supported
    by the located report excerpt.

    This is NOT a medical fact-checking model.
    """
    answer = normalize(answer)

    if not answer or not evidence_result:
        return {
            "status": "Unverifiable",
            "reason": "No sufficient original report evidence was located."
        }

    evidence = normalize(evidence_result["evidence"])

    if evidence_result["match_type"] != "Exact":
        return {
            "status": "Unverifiable",
            "reason": (
                "Similar report text was located, but an exact "
                "supporting evidence match was not established."
            )
        }

    if answer.lower() == evidence.lower():
        return {
            "status": "Verified",
            "reason": (
                "The answer exactly matches evidence found "
                "in the original report."
            )
        }

    if answer.lower() in evidence.lower():
        return {
            "status": "Verified",
            "reason": (
                "The answer is directly contained in the "
                "original report evidence."
            )
        }

    return {
        "status": "Unverifiable",
        "reason": (
            "The evidence exists in the report, but this "
            "checker cannot establish that every claim "
            "in the answer is supported."
        )
    }


def evidence_lens(pages, answer, evidence):
    located = find_evidence(pages, evidence)
    verification = verify_answer(answer, located)

    return {
        "located": located,
        "verification": verification
    }