import re

MEDICAL_TERMS = {
    "cardiomegaly": "Enlargement of the heart.",
    "atelectasis": "Partial collapse of a lung or part of a lung.",
    "pleural effusion": "Fluid buildup in the space around the lungs.",
    "pneumonia": "An infection that causes inflammation in the lungs.",
    "pneumothorax": "Air trapped between the lung and chest wall.",
    "bronchiectasis": "Long-term widening and damage of the airways.",
    "consolidation": "A lung area filled with material such as fluid instead of air.",
    "pulmonary edema": "Fluid buildup inside the lungs.",
    "infiltrate": "An abnormal appearance in lung tissue seen on an image.",
    "opacity": "An area that appears whiter than expected on an X-ray.",
    "nodule": "A small rounded area seen on a medical image.",
    "mass": "An abnormal area or growth of tissue.",
    "fibrosis": "Scarring of tissue.",
    "emphysema": "A condition involving damage to the air sacs in the lungs.",
    "hyperinflation": "The lungs appear to contain more air than usual.",
    "cardiopulmonary": "Related to the heart and lungs.",
    "mediastinum": "The central area of the chest between the lungs.",
    "acute": "A condition or change that develops relatively quickly.",
    "chronic": "A condition that lasts for a long time.",
    "stable": "No significant change compared with an earlier examination.",
    "unremarkable": "No notable abnormality is described.",
    "bilateral": "Present on both sides.",
    "benign": "Not cancerous.",
    "lesion": "An area of abnormal tissue."
}


def explain_medical_terms(pages):
    """
    Find known medical terms in report pages and
    return their simple English explanations.
    """

    results = []

    if not pages:
        return results

    for term, explanation in MEDICAL_TERMS.items():

        matching_pages = []

        pattern = rf"\b{re.escape(term)}\b"

        for page in pages:

            text = str(page.get("text", ""))

            if re.search(pattern, text, flags=re.IGNORECASE):
                matching_pages.append(page.get("page", 1))

        if matching_pages:

            results.append({
                "term": term.title(),
                "explanation": explanation,
                "pages": matching_pages
            })

    return results