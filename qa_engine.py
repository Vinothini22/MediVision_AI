import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


MEDICAL_TERMS = {
    "hemoglobin": ["hemoglobin", "haemoglobin", "hb", "hgb"],
    "wbc": ["wbc", "white blood cell", "white blood count"],
    "rbc": ["rbc", "red blood cell", "red blood count"],
    "platelets": ["platelet", "platelets", "plt"],
    "hematocrit": ["hematocrit", "haematocrit", "hct"],
    "mcv": ["mcv", "mean corpuscular volume"]
}

REPORT_SECTIONS = {
    "impression": ["impression", "conclusion", "final opinion"],
    "findings": ["findings", "observations"],
    "indication": ["indication", "reason for examination"],
    "comparison": ["comparison", "previous examination"]
}


def extract_pdf_pages(pdf):
    pages = []

    for i, page in enumerate(pdf):
        pages.append({
            "page": i + 1,
            "text": page.get_text()
        })

    return pages


def no_evidence():
    return {
        "answer": (
            "The uploaded report does not contain "
            "clearly matching evidence for this question."
        ),
        "page": None,
        "evidence": "",
        "confidence": 0.0
    }


def extract_sections(text):
    """Extract labelled report sections without returning headings alone."""

    headings = (
        r"Indication|Comparison|Findings|Impression|"
        r"Conclusion|Observations|Final Opinion|"
        r"Reason for Examination|Previous Examination"
    )

    pattern = re.compile(
        rf"(?im)^\s*({headings})\s*:\s*"
    )

    matches = list(pattern.finditer(text))
    sections = {}

    for index, match in enumerate(matches):
        name = match.group(1).lower().strip()

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


def requested_section(question):
    question = question.lower()

    for section, aliases in REPORT_SECTIONS.items():
        for alias in aliases:
            if re.search(
                r"\b" + re.escape(alias) + r"\b",
                question
            ):
                return section

    return None


def answer_question(question, pages):

    question = question.strip()
    question_lower = question.lower()

    if not question:
        return no_evidence()

    # STEP 1: Direct section-based question answering
    section_name = requested_section(question)

    if section_name:

        aliases = REPORT_SECTIONS[section_name]

        for page in pages:

            sections = extract_sections(page.get("text", ""))

            for alias in aliases:

                content = sections.get(alias)

                if content:
                    return {
                        "answer": content,
                        "page": page["page"],
                        "evidence": f"{alias.title()}: {content}",
                        "confidence": 100.0
                    }

        # Do not invent a missing section.
        return no_evidence()

    # STEP 2: Direct CBC measurement extraction
    for name, aliases in MEDICAL_TERMS.items():

        if any(
            re.search(
                r"\b" + re.escape(alias) + r"\b",
                question_lower
            )
            for alias in aliases
        ):

            for page in pages:

                text = page.get("text", "")

                for alias in aliases:

                    pattern = (
                        r"\b" + re.escape(alias) +
                        r"\b\s*[:\-]?\s*"
                        r"(\d[\d,.]*\s*"
                        r"(?:million\s*/\s*[µμu]?[lL]|"
                        r"g\s*/\s*d[lL]|"
                        r"f[Ll]|%|"
                        r"/\s*[µμu]?[lL])?)"
                    )

                    match = re.search(
                        pattern,
                        text,
                        flags=re.IGNORECASE
                    )

                    if match:

                        value = match.group(1).strip()

                        return {
                            "answer": f"{name.upper()}: {value}",
                            "page": page["page"],
                            "evidence": match.group(0),
                            "confidence": 100.0
                        }

            return no_evidence()

    # STEP 3: General evidence retrieval
    chunks = []

    for page in pages:

        text = page.get("text", "").strip()

        if not text:
            continue

        sentences = re.split(
            r"(?<=[.!?])\s+|\n+",
            text
        )

        for sentence in sentences:

            sentence = sentence.strip()

            # Avoid returning section headings alone.
            if (
                len(sentence) >= 8
                and sentence.lower().rstrip(":")
                not in REPORT_SECTIONS
            ):
                chunks.append({
                    "page": page["page"],
                    "text": sentence
                })

    if not chunks:
        return no_evidence()

    documents = [chunk["text"] for chunk in chunks]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    try:
        matrix = vectorizer.fit_transform(
            documents + [question]
        )

        scores = cosine_similarity(
            matrix[-1],
            matrix[:-1]
        )[0]

        best_index = int(scores.argmax())
        score = float(scores[best_index])

        if score < 0.15:
            return no_evidence()

        best = chunks[best_index]

        return {
            "answer": best["text"],
            "page": best["page"],
            "evidence": best["text"],
            "confidence": round(score * 100, 2)
        }

    except ValueError:
        return no_evidence()