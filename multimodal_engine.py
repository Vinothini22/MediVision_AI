from vision_model import analyze_xray
from qa_engine import answer_question


def multimodal_analysis(question, xray=None, pages=None):

    result = {
        "mode": None,
        "answer": "",
        "image_processed": False,
        "image_features": None,
        "source": None,
        "page": None,
        "evidence": "",
        "confidence": 0.0
    }

    # X-Ray processing
    if xray is not None:

        vision_result = analyze_xray(xray)

        result["image_processed"] = True

        result["image_features"] = (
            vision_result["feature_dimension"]
        )

    # Medical report question answering
    if pages and any(p.get("text", "").strip() for p in pages):

        qa_result = answer_question(question, pages)

        result["answer"] = qa_result["answer"]
        result["page"] = qa_result["page"]
        result["evidence"] = qa_result["evidence"]
        result["confidence"] = qa_result["confidence"]

        result["source"] = "Uploaded Medical Report"

    # Determine analysis mode
    if result["image_processed"] and pages:

        result["mode"] = "X-Ray + Medical Report"

    elif result["image_processed"]:

        result["mode"] = "X-Ray Only"

    elif pages:

        result["mode"] = "Medical Report Only"

    else:

        result["mode"] = "No Input"

    # No report evidence
    if not result["answer"]:

        result["answer"] = (
            "X-Ray image features were extracted successfully. "
            "However, medical image question answering is not "
            "yet available without a validated medical model "
            "or supporting report evidence."
        )

    return result