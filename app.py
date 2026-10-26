import streamlit as st
import io

from PIL import Image

from landing_page import show_landing_page
from ocr_engine import extract_image_text, extract_scanned_pdf
from multimodal_engine import multimodal_analysis
from trained_vision import predict_xray
from report_matcher import find_matching_report
from suggested_questions import generate_suggested_questions
from report_summarizer import summarize_report
from medical_terms import explain_medical_terms
from evidence_lens import evidence_lens

# NEW: PDF GENERATOR
from pdf_generator import generate_medical_pdf


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="MediVision AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# 2. WELCOME PAGE
# ==========================================

if "entered" not in st.session_state:
    st.session_state["entered"] = False

if not st.session_state["entered"]:
    show_landing_page()
    st.stop()


# ==========================================
# 3. DASHBOARD THEME
# ==========================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        120deg,
        #FFFFFF,
        #F2F9FF 65%,
        #E8F5FF
    );
}

.block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

section[data-testid="stSidebar"] {
    background: #EAF5FD;
    border-right: 1px solid #CBE5F5;
}

h1, h2, h3 {
    color: #123B68;
}

div.stButton > button {
    border-radius: 12px;
    font-weight: 650;
    min-height: 43px;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(
        90deg,
        #078FCB,
        #08A7B8
    );
    color: white;
    border: none;
}

[data-testid="stMetric"] {
    background: white;
    padding: 15px;
    border: 1px solid #D5E9F6;
    border-radius: 14px;
}

[data-testid="stFileUploader"] {
    background: white;
    padding: 10px;
    border: 1px solid #D5E9F6;
    border-radius: 14px;
}

[data-testid="stExpander"] {
    background: white;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 4. SESSION STATE
# ==========================================

defaults = {
    "section": "🏠 Overview",
    "xray_data": None,
    "report_data": None,
    "report_summary": None,
    "terms_result": None,
    "vision_result": None,
    "qa_result": None,
    "medical_question": "",
    "last_report_key": None,
    "last_xray_key": None,
    "upload_epoch": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================
# 5. REPORT PROCESSING
# ==========================================

@st.cache_data(show_spinner=False)
def process_report(data, filename):

    if filename.lower().endswith(".pdf"):

        class UploadedPDF:

            def __init__(self, value):
                self.data = value

            def getvalue(self):
                return self.data

        return extract_scanned_pdf(
            UploadedPDF(data)
        )

    image = Image.open(
        io.BytesIO(data)
    ).convert("RGB")

    text = extract_image_text(image)

    return [{
        "page": 1,
        "text": text
    }]


@st.cache_data(show_spinner=False)
def dataset_report(filename):
    return find_matching_report(filename)


# ==========================================
# 6. SAFE NAVIGATION
# ==========================================

def go(destination):

    st.session_state["next_section"] = destination
    st.rerun()


# ==========================================
# 7. EVIDENCELENS
# ==========================================

def show_evidence(pages, result):

    st.divider()
    st.subheader("🔍 EvidenceLens")

    analysis = evidence_lens(
        pages=pages,
        answer=result.get("answer", ""),
        evidence=result.get("evidence", "")
    )

    located = analysis["located"]
    verification = analysis["verification"]

    with st.container(border=True):

        st.markdown("#### Original Report Evidence")

        if located:

            st.info(located["evidence"])

            st.caption(
                f"Source Page: {located['page']} | "
                f"Match: {located['match_type']}"
            )

        else:

            st.warning(
                "Supporting evidence could not be located "
                "in the original report."
            )

    with st.container(border=True):

        st.markdown("#### Answer Verification")

        status = verification["status"]

        if status == "Verified":
            st.success("Verified")

        elif status == "Contradicted":
            st.error("Contradicted")

        else:
            st.warning("Unverifiable")

        st.write(verification["reason"])

        st.caption(
            "Verification checks original report-text "
            "support only, not clinical correctness."
        )


# ==========================================
# 8. FEATURE CARD
# ==========================================

def feature(icon, title, detail, destination):

    with st.container(border=True):

        st.subheader(f"{icon} {title}")
        st.caption(detail)

        if st.button(
            "Open →",
            key="feature_" + destination,
            use_container_width=True
        ):
            go(destination)


# ==========================================
# 9. SIDEBAR NAVIGATION
# ==========================================

navigation = [
    "🏠 Overview",
    "📂 Upload Center",
    "🩻 X-Ray Analysis",
    "📋 Report Summary",
    "📚 Medical Terms",
    "💬 Medical Q&A",
    "📊 Research Results"
]

# Apply navigation BEFORE creating radio widget.

if "next_section" in st.session_state:

    st.session_state["section"] = (
        st.session_state.pop("next_section")
    )

with st.sidebar:

    st.title("🏥 MediVision AI")

    st.caption(
        "MEDICAL INTELLIGENCE WORKSPACE"
    )

    st.divider()

    st.radio(
        "WORKSPACE NAVIGATION",
        navigation,
        key="section"
    )

    st.divider()

    st.caption("PLATFORM MODULES")

    st.write("✓ Vision Transformer")
    st.write("✓ Medical Report OCR")
    st.write("✓ Question Answering")
    st.write("✓ EvidenceLens")

    st.divider()

    st.info(
        "Educational research prototype. "
        "Not intended for clinical diagnosis."
    )

    if st.button(
        "← Back to Welcome Page",
        use_container_width=True
    ):

        st.session_state["entered"] = False
        st.rerun()


# ==========================================
# 10. DASHBOARD HEADER
# ==========================================

top1, top2 = st.columns(
    [4, 1],
    vertical_alignment="center"
)

with top1:

    st.title("🏥 MediVision AI")

    st.caption(
        "MULTIMODAL MEDICAL INTELLIGENCE PLATFORM"
    )

with top2:

    st.success("● Research Mode")


# ==========================================
# PART 2 CONTINUES BELOW
# ==========================================
# ==========================================
# 11. LOAD SAVED FILES
# ==========================================

xray_saved = st.session_state["xray_data"]
report_saved = st.session_state["report_data"]

matched = None

if xray_saved:

    try:

        matched = dataset_report(
            xray_saved["name"]
        )

    except Exception as e:

        st.warning(
            f"Automatic Report Matching Error: {e}"
        )


pages = (
    matched["pages"].copy()
    if matched is not None
    else []
)

active_name = (
    f"IU Dataset Report (UID {matched['uid']})"
    if matched is not None
    else None
)


# ==========================================
# 12. MANUAL REPORT PRIORITY
# ==========================================

if report_saved:

    try:

        pages = process_report(
            report_saved["bytes"],
            report_saved["name"]
        )

        active_name = report_saved["name"]

    except Exception as e:

        st.error(
            f"Report Processing Error: {e}"
        )

        pages = []
        active_name = None


# ==========================================
# 13. RESET OLD RESULTS
# ==========================================

report_key = (
    active_name,
    tuple(
        (
            page.get("page"),
            page.get("text", "")
        )
        for page in pages
    )
)

xray_key = (
    (
        xray_saved["name"],
        xray_saved["bytes"]
    )
    if xray_saved
    else None
)

if st.session_state["last_report_key"] != report_key:

    st.session_state["report_summary"] = None
    st.session_state["terms_result"] = None
    st.session_state["qa_result"] = None
    st.session_state["last_report_key"] = report_key

if st.session_state["last_xray_key"] != xray_key:

    st.session_state["vision_result"] = None
    st.session_state["qa_result"] = None
    st.session_state["last_xray_key"] = xray_key


section = st.session_state["section"]


# ==========================================
# 14. OVERVIEW DASHBOARD
# ==========================================

if section == "🏠 Overview":

    with st.container(border=True):

        st.caption("AI-POWERED RESEARCH WORKSPACE")

        st.header("Intelligent Medical Analysis")

        st.write(
            "A unified workspace for Chest X-Ray processing, "
            "medical report understanding, structured summaries "
            "and evidence-based question answering."
        )

        st.caption(
            "Multimodal AI-Based Medical Report Understanding "
            "with Question Answering Using Vision Transformer"
        )

        st.write("")

        if st.button(
            "Start New Medical Analysis →",
            type="primary",
            use_container_width=True
        ):
            go("📂 Upload Center")

    st.write("")
    st.subheader("Explore AI Modules")

    a, b, c = st.columns(3)

    with a:
        feature(
            "🩻",
            "X-Ray Intelligence",
            "Trained Vision Transformer image classifier.",
            "🩻 X-Ray Analysis"
        )

    with b:
        feature(
            "📄",
            "Medical Report OCR",
            "Extract text from scanned reports.",
            "📂 Upload Center"
        )

    with c:
        feature(
            "💬",
            "Medical Q&A",
            "Ask questions about medical reports.",
            "💬 Medical Q&A"
        )

    a, b, c = st.columns(3)

    with a:
        feature(
            "📋",
            "Smart Summary",
            "Structured English report summarization.",
            "📋 Report Summary"
        )

    with b:
        feature(
            "📚",
            "Medical Terms",
            "Understand medical terminology.",
            "📚 Medical Terms"
        )

    with c:

        with st.container(border=True):

            st.subheader("🔍 EvidenceLens")

            st.caption(
                "Verify answer support in original report text."
            )

            if st.button(
                "Open →",
                key="evidence_feature",
                use_container_width=True
            ):
                go("💬 Medical Q&A")

    st.write("")
    st.subheader("Current Workspace")

    a, b, c = st.columns(3)

    with a:
        st.metric(
            "X-Ray",
            "Uploaded" if xray_saved else "Not Uploaded"
        )

    with b:
        st.metric(
            "Active Report",
            "Available" if pages else "Not Available"
        )

    with c:
        st.metric(
            "Report Pages",
            len(pages)
        )


# ==========================================
# 15. UPLOAD CENTER
# ==========================================

elif section == "📂 Upload Center":

    st.header("📂 Medical Data Upload Center")

    st.caption(
        "Upload an X-Ray image, medical report, or both."
    )

    a, b = st.columns(2)

    # --------------------------------------
    # X-RAY UPLOAD
    # --------------------------------------

    with a:

        with st.container(border=True):

            st.subheader("🩻 Chest X-Ray")

            uploaded_xray = st.file_uploader(
                "Choose X-Ray Image",
                type=["jpg", "jpeg", "png"],
                key=f"xray_upload_{st.session_state['upload_epoch']}"
            )

            if uploaded_xray is not None:

                new_file = {
                    "name": uploaded_xray.name,
                    "bytes": uploaded_xray.getvalue()
                }

                if st.session_state["xray_data"] != new_file:

                    st.session_state["xray_data"] = new_file
                    st.rerun()

            if xray_saved:

                st.image(
                    xray_saved["bytes"],
                    caption=xray_saved["name"],
                    use_container_width=True
                )

                if st.button(
                    "Remove X-Ray",
                    key="remove_xray"
                ):

                    st.session_state["xray_data"] = None
                    st.session_state["upload_epoch"] += 1
                    st.rerun()

    # --------------------------------------
    # MEDICAL REPORT UPLOAD
    # --------------------------------------

    with b:

        with st.container(border=True):

            st.subheader("📄 Medical Report")

            uploaded_report = st.file_uploader(
                "Choose Medical Report (Optional)",
                type=["pdf", "jpg", "jpeg", "png"],
                key=f"report_upload_{st.session_state['upload_epoch']}"
            )

            if uploaded_report is not None:

                new_file = {
                    "name": uploaded_report.name,
                    "bytes": uploaded_report.getvalue()
                }

                if st.session_state["report_data"] != new_file:

                    st.session_state["report_data"] = new_file
                    st.rerun()

            if report_saved:

                st.success(
                    f"Saved Report: {report_saved['name']}"
                )

                if st.button(
                    "Remove Report",
                    key="remove_report"
                ):

                    st.session_state["report_data"] = None
                    st.session_state["upload_epoch"] += 1
                    st.rerun()

    st.divider()

    # --------------------------------------
    # DATASET REPORT MATCHING
    # --------------------------------------

    if matched is not None:

        st.success(
            "Matching IU Dataset Report Found!"
        )

        st.write(
            "Study UID:",
            matched["uid"]
        )

        with st.expander(
            "View Matching Dataset Report"
        ):
            st.text(
                matched["report_text"]
            )

    elif xray_saved:

        st.info(
            "No matching IU Dataset report found. "
            "You can upload a medical report manually."
        )

    # --------------------------------------
    # ACTIVE REPORT PREVIEW
    # --------------------------------------

    if active_name:

        st.info(
            f"Active Report: {active_name}"
        )

        with st.expander(
            "View Active Report Text"
        ):

            for page in pages:

                st.markdown(
                    f"**Page {page['page']}**"
                )

                if page["text"].strip():
                    st.write(page["text"])

                else:
                    st.warning(
                        "No readable text detected."
                    )

                st.divider()

    st.caption(
        "Manual report upload takes priority. "
        "Filename matching alone does not verify "
        "the image content."
    )

    # --------------------------------------
    # NEXT STEP BUTTON
    # --------------------------------------

    st.divider()

    if xray_saved:

        if st.button(
            "Next → X-Ray Analysis",
            type="primary",
            use_container_width=True,
            key="upload_next_xray"
        ):
            go("🩻 X-Ray Analysis")

    elif pages:

        if st.button(
            "Next → Report Summary",
            type="primary",
            use_container_width=True,
            key="upload_next_summary"
        ):
            go("📋 Report Summary")

    else:

        st.info(
            "Upload an X-Ray or medical report "
            "to continue."
        )


# ==========================================
# PART 3 CONTINUES BELOW
# ==========================================
# ==========================================
# 16. X-RAY ANALYSIS
# ==========================================

elif section == "🩻 X-Ray Analysis":

    st.header("🩻 Vision Transformer Analysis")

    st.caption(
        "Experimental Chest X-Ray classification."
    )

    if not xray_saved:

        st.info(
            "Please upload an X-Ray image in Upload Center."
        )

        if st.button(
            "Go to Upload Center →",
            type="primary"
        ):
            go("📂 Upload Center")

    else:

        a, b = st.columns(2)

        with a:

            with st.container(border=True):

                st.subheader("Uploaded Image")

                st.image(
                    xray_saved["bytes"],
                    caption=xray_saved["name"],
                    use_container_width=True
                )

        with b:

            with st.container(border=True):

                st.subheader("AI Model")

                st.write(
                    "Pretrained Vision Transformer "
                    "with optimized classifier."
                )

                if st.button(
                    "Analyze X-Ray with Trained Model",
                    type="primary",
                    use_container_width=True
                ):

                    try:

                        with st.spinner(
                            "Running trained Vision Transformer..."
                        ):

                            prediction = predict_xray(
                                io.BytesIO(
                                    xray_saved["bytes"]
                                )
                            )

                        st.session_state["vision_result"] = (
                            prediction
                        )

                    except Exception as e:

                        st.error(
                            f"Trained Model Error: {e}"
                        )

        result = st.session_state["vision_result"]

        if result:

            st.divider()

            st.subheader("AI Analysis Results")

            st.success(
                result["status"]
            )

            a, b = st.columns(2)

            with a:

                st.metric(
                    "Experimental Prediction",
                    result["prediction"]
                )

            with b:

                st.metric(
                    "Model Score",
                    f"{result['model_score']}%"
                )

            st.write(
                "Extracted Image Features:",
                result["feature_dimension"]
            )

            st.info(
                result["note"]
            )

            st.caption(
                "The model score is an uncalibrated "
                "experimental classifier output, "
                "not medical diagnostic confidence."
            )

            st.divider()

            if pages:

                if st.button(
                    "Next → Report Summary",
                    type="primary",
                    use_container_width=True,
                    key="xray_next_summary"
                ):
                    go("📋 Report Summary")

            else:

                st.warning(
                    "No matching report is available. "
                    "Please upload a medical report "
                    "to continue."
                )

                if st.button(
                    "Upload Medical Report →",
                    type="primary",
                    use_container_width=True,
                    key="xray_next_upload"
                ):
                    go("📂 Upload Center")


# ==========================================
# 17. REPORT SUMMARY
# ==========================================

elif section == "📋 Report Summary":

    st.header("📋 Smart Medical Report Summary")

    st.write(
        "Generate a structured English summary "
        "from the active medical report."
    )

    if not pages:

        st.info(
            "Upload a medical report or IU Dataset "
            "X-Ray with a matching report."
        )

        if st.button(
            "Go to Upload Center →",
            type="primary",
            key="summary_upload"
        ):
            go("📂 Upload Center")

    else:

        st.info(
            f"Active Report: {active_name}"
        )

        if st.button(
            "Generate Smart Summary",
            type="primary",
            use_container_width=True
        ):

            try:

                with st.spinner(
                    "Generating report summary..."
                ):

                    st.session_state["report_summary"] = (
                        summarize_report(pages)
                    )

            except Exception as e:

                st.error(
                    f"Report Summarization Error: {e}"
                )

        summary = st.session_state["report_summary"]

        if summary:

            st.success(
                "Report Summary Generated Successfully!"
            )

            for item in summary:

                with st.container(border=True):

                    st.subheader(
                        item["title"]
                    )

                    st.write(
                        item["text"]
                    )

                    st.caption(
                        f"Source Page: {item['page']}"
                    )

        elif summary == []:

            st.warning(
                "No supported report sections were found."
            )

        st.caption(
            "Extractive English summary only. "
            "Not a clinical interpretation."
        )

        if summary is not None:

            st.divider()

            if st.button(
                "Next → Medical Terms",
                type="primary",
                use_container_width=True,
                key="summary_next_terms"
            ):
                go("📚 Medical Terms")


# ==========================================
# 18. MEDICAL TERMS EXPLANATION
# ==========================================

elif section == "📚 Medical Terms":

    st.header("📚 Medical Terminology Explanation")

    st.write(
        "Understand medical terms found "
        "in the active report."
    )

    if not pages:

        st.info(
            "Please upload a medical report first."
        )

        if st.button(
            "Go to Upload Center →",
            type="primary",
            key="terms_upload"
        ):
            go("📂 Upload Center")

    else:

        st.info(
            f"Active Report: {active_name}"
        )

        if st.button(
            "Explain Medical Terms",
            type="primary",
            use_container_width=True
        ):

            try:

                terms = explain_medical_terms(pages)

                st.session_state["terms_result"] = terms

            except Exception as e:

                st.error(
                    f"Medical Terminology Error: {e}"
                )

        terms = st.session_state["terms_result"]

        if terms:

            st.success(
                f"Found {len(terms)} medical terms."
            )

            for item in terms:

                with st.expander(
                    item["term"],
                    expanded=True
                ):

                    st.write(
                        item["explanation"]
                    )

                    page_numbers = ", ".join(
                        str(page)
                        for page in item["pages"]
                    )

                    st.caption(
                        f"Source Page(s): {page_numbers}"
                    )

        elif terms == []:

            st.info(
                "No terms from the current medical "
                "terminology dictionary were found."
            )

        st.caption(
            "A term appearing in a report does not "
            "necessarily mean the patient has "
            "that condition."
        )

        if terms is not None:

            st.divider()

            if st.button(
                "Next → Medical Q&A",
                type="primary",
                use_container_width=True,
                key="terms_next_qa"
            ):
                go("💬 Medical Q&A")


# ==========================================
# PART 4 CONTINUES BELOW
# ==========================================
# ==========================================
# 16. X-RAY ANALYSIS
# ==========================================

elif section == "🩻 X-Ray Analysis":

    st.header("🩻 Vision Transformer Analysis")

    st.caption(
        "Experimental Chest X-Ray classification."
    )

    if not xray_saved:

        st.info(
            "Please upload an X-Ray image in Upload Center."
        )

        if st.button(
            "Go to Upload Center →",
            type="primary"
        ):
            go("📂 Upload Center")

    else:

        a, b = st.columns(2)

        with a:

            with st.container(border=True):

                st.subheader("Uploaded Image")

                st.image(
                    xray_saved["bytes"],
                    caption=xray_saved["name"],
                    use_container_width=True
                )

        with b:

            with st.container(border=True):

                st.subheader("AI Model")

                st.write(
                    "Pretrained Vision Transformer "
                    "with optimized classifier."
                )

                if st.button(
                    "Analyze X-Ray with Trained Model",
                    type="primary",
                    use_container_width=True
                ):

                    try:

                        with st.spinner(
                            "Running trained Vision Transformer..."
                        ):

                            prediction = predict_xray(
                                io.BytesIO(
                                    xray_saved["bytes"]
                                )
                            )

                        st.session_state["vision_result"] = (
                            prediction
                        )

                    except Exception as e:

                        st.error(
                            f"Trained Model Error: {e}"
                        )

        result = st.session_state["vision_result"]

        if result:

            st.divider()

            st.subheader("AI Analysis Results")

            st.success(
                result["status"]
            )

            a, b = st.columns(2)

            with a:

                st.metric(
                    "Experimental Prediction",
                    result["prediction"]
                )

            with b:

                st.metric(
                    "Model Score",
                    f"{result['model_score']}%"
                )

            st.write(
                "Extracted Image Features:",
                result["feature_dimension"]
            )

            st.info(
                result["note"]
            )

            st.caption(
                "The model score is an uncalibrated "
                "experimental classifier output, "
                "not medical diagnostic confidence."
            )

            st.divider()

            if pages:

                if st.button(
                    "Next → Report Summary",
                    type="primary",
                    use_container_width=True,
                    key="xray_next_summary"
                ):
                    go("📋 Report Summary")

            else:

                st.warning(
                    "No matching report is available. "
                    "Please upload a medical report "
                    "to continue."
                )

                if st.button(
                    "Upload Medical Report →",
                    type="primary",
                    use_container_width=True,
                    key="xray_next_upload"
                ):
                    go("📂 Upload Center")


# ==========================================
# 17. REPORT SUMMARY
# ==========================================

elif section == "📋 Report Summary":

    st.header("📋 Smart Medical Report Summary")

    st.write(
        "Generate a structured English summary "
        "from the active medical report."
    )

    if not pages:

        st.info(
            "Upload a medical report or IU Dataset "
            "X-Ray with a matching report."
        )

        if st.button(
            "Go to Upload Center →",
            type="primary",
            key="summary_upload"
        ):
            go("📂 Upload Center")

    else:

        st.info(
            f"Active Report: {active_name}"
        )

        if st.button(
            "Generate Smart Summary",
            type="primary",
            use_container_width=True
        ):

            try:

                with st.spinner(
                    "Generating report summary..."
                ):

                    st.session_state["report_summary"] = (
                        summarize_report(pages)
                    )

            except Exception as e:

                st.error(
                    f"Report Summarization Error: {e}"
                )

        summary = st.session_state["report_summary"]

        if summary:

            st.success(
                "Report Summary Generated Successfully!"
            )

            for item in summary:

                with st.container(border=True):

                    st.subheader(
                        item["title"]
                    )

                    st.write(
                        item["text"]
                    )

                    st.caption(
                        f"Source Page: {item['page']}"
                    )

        elif summary == []:

            st.warning(
                "No supported report sections were found."
            )

        st.caption(
            "Extractive English summary only. "
            "Not a clinical interpretation."
        )

        if summary is not None:

            st.divider()

            if st.button(
                "Next → Medical Terms",
                type="primary",
                use_container_width=True,
                key="summary_next_terms"
            ):
                go("📚 Medical Terms")


# ==========================================
# 18. MEDICAL TERMS EXPLANATION
# ==========================================

elif section == "📚 Medical Terms":

    st.header("📚 Medical Terminology Explanation")

    st.write(
        "Understand medical terms found "
        "in the active report."
    )

    if not pages:

        st.info(
            "Please upload a medical report first."
        )

        if st.button(
            "Go to Upload Center →",
            type="primary",
            key="terms_upload"
        ):
            go("📂 Upload Center")

    else:

        st.info(
            f"Active Report: {active_name}"
        )

        if st.button(
            "Explain Medical Terms",
            type="primary",
            use_container_width=True
        ):

            try:

                terms = explain_medical_terms(pages)

                st.session_state["terms_result"] = terms

            except Exception as e:

                st.error(
                    f"Medical Terminology Error: {e}"
                )

        terms = st.session_state["terms_result"]

        if terms:

            st.success(
                f"Found {len(terms)} medical terms."
            )

            for item in terms:

                with st.expander(
                    item["term"],
                    expanded=True
                ):

                    st.write(
                        item["explanation"]
                    )

                    page_numbers = ", ".join(
                        str(page)
                        for page in item["pages"]
                    )

                    st.caption(
                        f"Source Page(s): {page_numbers}"
                    )

        elif terms == []:

            st.info(
                "No terms from the current medical "
                "terminology dictionary were found."
            )

        st.caption(
            "A term appearing in a report does not "
            "necessarily mean the patient has "
            "that condition."
        )

        if terms is not None:

            st.divider()

            if st.button(
                "Next → Medical Q&A",
                type="primary",
                use_container_width=True,
                key="terms_next_qa"
            ):
                go("💬 Medical Q&A")


# ==========================================
# PART 4 CONTINUES BELOW
# ==========================================
# ==========================================
# 16. X-RAY ANALYSIS
# ==========================================

elif section == "🩻 X-Ray Analysis":

    st.header("🩻 Vision Transformer Analysis")

    st.caption(
        "Experimental Chest X-Ray classification."
    )

    if not xray_saved:

        st.info(
            "Please upload an X-Ray image in Upload Center."
        )

        if st.button(
            "Go to Upload Center →",
            type="primary"
        ):
            go("📂 Upload Center")

    else:

        a, b = st.columns(2)

        with a:

            with st.container(border=True):

                st.subheader("Uploaded Image")

                st.image(
                    xray_saved["bytes"],
                    caption=xray_saved["name"],
                    use_container_width=True
                )

        with b:

            with st.container(border=True):

                st.subheader("AI Model")

                st.write(
                    "Pretrained Vision Transformer "
                    "with optimized classifier."
                )

                if st.button(
                    "Analyze X-Ray with Trained Model",
                    type="primary",
                    use_container_width=True
                ):

                    try:

                        with st.spinner(
                            "Running trained Vision Transformer..."
                        ):

                            prediction = predict_xray(
                                io.BytesIO(
                                    xray_saved["bytes"]
                                )
                            )

                        st.session_state["vision_result"] = (
                            prediction
                        )

                    except Exception as e:

                        st.error(
                            f"Trained Model Error: {e}"
                        )

        result = st.session_state["vision_result"]

        if result:

            st.divider()

            st.subheader("AI Analysis Results")

            st.success(
                result["status"]
            )

            a, b = st.columns(2)

            with a:

                st.metric(
                    "Experimental Prediction",
                    result["prediction"]
                )

            with b:

                st.metric(
                    "Model Score",
                    f"{result['model_score']}%"
                )

            st.write(
                "Extracted Image Features:",
                result["feature_dimension"]
            )

            st.info(
                result["note"]
            )

            st.caption(
                "The model score is an uncalibrated "
                "experimental classifier output, "
                "not medical diagnostic confidence."
            )

            st.divider()

            if pages:

                if st.button(
                    "Next → Report Summary",
                    type="primary",
                    use_container_width=True,
                    key="xray_next_summary"
                ):
                    go("📋 Report Summary")

            else:

                st.warning(
                    "No matching report is available. "
                    "Please upload a medical report "
                    "to continue."
                )

                if st.button(
                    "Upload Medical Report →",
                    type="primary",
                    use_container_width=True,
                    key="xray_next_upload"
                ):
                    go("📂 Upload Center")


# ==========================================
# 17. REPORT SUMMARY
# ==========================================

elif section == "📋 Report Summary":

    st.header("📋 Smart Medical Report Summary")

    st.write(
        "Generate a structured English summary "
        "from the active medical report."
    )

    if not pages:

        st.info(
            "Upload a medical report or IU Dataset "
            "X-Ray with a matching report."
        )

        if st.button(
            "Go to Upload Center →",
            type="primary",
            key="summary_upload"
        ):
            go("📂 Upload Center")

    else:

        st.info(
            f"Active Report: {active_name}"
        )

        if st.button(
            "Generate Smart Summary",
            type="primary",
            use_container_width=True
        ):

            try:

                with st.spinner(
                    "Generating report summary..."
                ):

                    st.session_state["report_summary"] = (
                        summarize_report(pages)
                    )

            except Exception as e:

                st.error(
                    f"Report Summarization Error: {e}"
                )

        summary = st.session_state["report_summary"]

        if summary:

            st.success(
                "Report Summary Generated Successfully!"
            )

            for item in summary:

                with st.container(border=True):

                    st.subheader(
                        item["title"]
                    )

                    st.write(
                        item["text"]
                    )

                    st.caption(
                        f"Source Page: {item['page']}"
                    )

        elif summary == []:

            st.warning(
                "No supported report sections were found."
            )

        st.caption(
            "Extractive English summary only. "
            "Not a clinical interpretation."
        )

        if summary is not None:

            st.divider()

            if st.button(
                "Next → Medical Terms",
                type="primary",
                use_container_width=True,
                key="summary_next_terms"
            ):
                go("📚 Medical Terms")


# ==========================================
# 18. MEDICAL TERMS EXPLANATION
# ==========================================

elif section == "📚 Medical Terms":

    st.header("📚 Medical Terminology Explanation")

    st.write(
        "Understand medical terms found "
        "in the active report."
    )

    if not pages:

        st.info(
            "Please upload a medical report first."
        )

        if st.button(
            "Go to Upload Center →",
            type="primary",
            key="terms_upload"
        ):
            go("📂 Upload Center")

    else:

        st.info(
            f"Active Report: {active_name}"
        )

        if st.button(
            "Explain Medical Terms",
            type="primary",
            use_container_width=True
        ):

            try:

                terms = explain_medical_terms(pages)

                st.session_state["terms_result"] = terms

            except Exception as e:

                st.error(
                    f"Medical Terminology Error: {e}"
                )

        terms = st.session_state["terms_result"]

        if terms:

            st.success(
                f"Found {len(terms)} medical terms."
            )

            for item in terms:

                with st.expander(
                    item["term"],
                    expanded=True
                ):

                    st.write(
                        item["explanation"]
                    )

                    page_numbers = ", ".join(
                        str(page)
                        for page in item["pages"]
                    )

                    st.caption(
                        f"Source Page(s): {page_numbers}"
                    )

        elif terms == []:

            st.info(
                "No terms from the current medical "
                "terminology dictionary were found."
            )

        st.caption(
            "A term appearing in a report does not "
            "necessarily mean the patient has "
            "that condition."
        )

        if terms is not None:

            st.divider()

            if st.button(
                "Next → Medical Q&A",
                type="primary",
                use_container_width=True,
                key="terms_next_qa"
            ):
                go("💬 Medical Q&A")


# ==========================================
# PART 4 CONTINUES BELOW
# ==========================================# ==========================================
# 16. X-RAY ANALYSIS
# ==========================================

elif section == "🩻 X-Ray Analysis":

    st.header("🩻 Vision Transformer Analysis")

    st.caption(
        "Experimental Chest X-Ray classification."
    )

    if not xray_saved:

        st.info(
            "Please upload an X-Ray image in Upload Center."
        )

        if st.button(
            "Go to Upload Center →",
            type="primary"
        ):
            go("📂 Upload Center")

    else:

        a, b = st.columns(2)

        with a:

            with st.container(border=True):

                st.subheader("Uploaded Image")

                st.image(
                    xray_saved["bytes"],
                    caption=xray_saved["name"],
                    use_container_width=True
                )

        with b:

            with st.container(border=True):

                st.subheader("AI Model")

                st.write(
                    "Pretrained Vision Transformer "
                    "with optimized classifier."
                )

                if st.button(
                    "Analyze X-Ray with Trained Model",
                    type="primary",
                    use_container_width=True
                ):

                    try:

                        with st.spinner(
                            "Running trained Vision Transformer..."
                        ):

                            prediction = predict_xray(
                                io.BytesIO(
                                    xray_saved["bytes"]
                                )
                            )

                        st.session_state["vision_result"] = (
                            prediction
                        )

                    except Exception as e:

                        st.error(
                            f"Trained Model Error: {e}"
                        )

        result = st.session_state["vision_result"]

        if result:

            st.divider()

            st.subheader("AI Analysis Results")

            st.success(
                result["status"]
            )

            a, b = st.columns(2)

            with a:

                st.metric(
                    "Experimental Prediction",
                    result["prediction"]
                )

            with b:

                st.metric(
                    "Model Score",
                    f"{result['model_score']}%"
                )

            st.write(
                "Extracted Image Features:",
                result["feature_dimension"]
            )

            st.info(
                result["note"]
            )

            st.caption(
                "The model score is an uncalibrated "
                "experimental classifier output, "
                "not medical diagnostic confidence."
            )

            st.divider()

            if pages:

                if st.button(
                    "Next → Report Summary",
                    type="primary",
                    use_container_width=True,
                    key="xray_next_summary"
                ):
                    go("📋 Report Summary")

            else:

                st.warning(
                    "No matching report is available. "
                    "Please upload a medical report "
                    "to continue."
                )

                if st.button(
                    "Upload Medical Report →",
                    type="primary",
                    use_container_width=True,
                    key="xray_next_upload"
                ):
                    go("📂 Upload Center")


# ==========================================
# 17. REPORT SUMMARY
# ==========================================

elif section == "📋 Report Summary":

    st.header("📋 Smart Medical Report Summary")

    st.write(
        "Generate a structured English summary "
        "from the active medical report."
    )

    if not pages:

        st.info(
            "Upload a medical report or IU Dataset "
            "X-Ray with a matching report."
        )

        if st.button(
            "Go to Upload Center →",
            type="primary",
            key="summary_upload"
        ):
            go("📂 Upload Center")

    else:

        st.info(
            f"Active Report: {active_name}"
        )

        if st.button(
            "Generate Smart Summary",
            type="primary",
            use_container_width=True
        ):

            try:

                with st.spinner(
                    "Generating report summary..."
                ):

                    st.session_state["report_summary"] = (
                        summarize_report(pages)
                    )

            except Exception as e:

                st.error(
                    f"Report Summarization Error: {e}"
                )

        summary = st.session_state["report_summary"]

        if summary:

            st.success(
                "Report Summary Generated Successfully!"
            )

            for item in summary:

                with st.container(border=True):

                    st.subheader(
                        item["title"]
                    )

                    st.write(
                        item["text"]
                    )

                    st.caption(
                        f"Source Page: {item['page']}"
                    )

        elif summary == []:

            st.warning(
                "No supported report sections were found."
            )

        st.caption(
            "Extractive English summary only. "
            "Not a clinical interpretation."
        )

        if summary is not None:

            st.divider()

            if st.button(
                "Next → Medical Terms",
                type="primary",
                use_container_width=True,
                key="summary_next_terms"
            ):
                go("📚 Medical Terms")


# ==========================================
# 18. MEDICAL TERMS EXPLANATION
# ==========================================

elif section == "📚 Medical Terms":

    st.header("📚 Medical Terminology Explanation")

    st.write(
        "Understand medical terms found "
        "in the active report."
    )

    if not pages:

        st.info(
            "Please upload a medical report first."
        )

        if st.button(
            "Go to Upload Center →",
            type="primary",
            key="terms_upload"
        ):
            go("📂 Upload Center")

    else:

        st.info(
            f"Active Report: {active_name}"
        )

        if st.button(
            "Explain Medical Terms",
            type="primary",
            use_container_width=True
        ):

            try:

                terms = explain_medical_terms(pages)

                st.session_state["terms_result"] = terms

            except Exception as e:

                st.error(
                    f"Medical Terminology Error: {e}"
                )

        terms = st.session_state["terms_result"]

        if terms:

            st.success(
                f"Found {len(terms)} medical terms."
            )

            for item in terms:

                with st.expander(
                    item["term"],
                    expanded=True
                ):

                    st.write(
                        item["explanation"]
                    )

                    page_numbers = ", ".join(
                        str(page)
                        for page in item["pages"]
                    )

                    st.caption(
                        f"Source Page(s): {page_numbers}"
                    )

        elif terms == []:

            st.info(
                "No terms from the current medical "
                "terminology dictionary were found."
            )

        st.caption(
            "A term appearing in a report does not "
            "necessarily mean the patient has "
            "that condition."
        )

        if terms is not None:

            st.divider()

            if st.button(
                "Next → Medical Q&A",
                type="primary",
                use_container_width=True,
                key="terms_next_qa"
            ):
                go("💬 Medical Q&A")


# ==========================================
# PART 4 CONTINUES BELOW
# ==========================================# 
# ==========================================
# 19. MEDICAL QUESTION ANSWERING
# ==========================================

elif section == "💬 Medical Q&A":

    st.header("💬 Ask MediVision AI")

    st.caption(
        f"Active Report: {active_name or 'None'}"
    )

    # --------------------------------------
    # SUGGESTED QUESTIONS
    # --------------------------------------

    suggestions = (
        generate_suggested_questions(pages)
        if pages
        else []
    )

    if suggestions:

        st.markdown("### 💡 Suggested Questions")

        selected_question = st.selectbox(
            "Choose a Question",
            options=[
                "Type my own question"
            ] + suggestions,
            key="suggested_question"
        )

        if selected_question != "Type my own question":

            if st.button(
                "Use Selected Question",
                key="use_suggested_question"
            ):

                st.session_state["medical_question"] = (
                    selected_question
                )

                st.rerun()

    else:

        st.info(
            "Upload a report to see suggested questions."
        )

    # --------------------------------------
    # USER QUESTION
    # --------------------------------------

    question = st.text_input(
        "Enter Your Medical Question",
        placeholder=(
            "What is the impression of this report?"
        ),
        key="medical_question"
    )

    if st.button(
        "Analyze with MediVision AI",
        type="primary",
        use_container_width=True,
        key="analyze_medical_question"
    ):

        if not xray_saved and not pages:

            st.warning(
                "Please upload an X-Ray or Medical Report."
            )

        elif not question.strip():

            st.warning(
                "Please enter your question."
            )

        else:

            try:

                with st.spinner(
                    "Performing Multimodal AI Analysis..."
                ):

                    xray_input = (
                        io.BytesIO(
                            xray_saved["bytes"]
                        )
                        if xray_saved
                        else None
                    )

                    result = multimodal_analysis(
                        question=question,
                        xray=xray_input,
                        pages=pages
                    )

                st.session_state["qa_result"] = {
                    "result": result,
                    "question": question,
                    "report_name": active_name
                }

            except Exception as e:

                st.error(
                    f"Multimodal Analysis Error: {e}"
                )

    # --------------------------------------
    # QUESTION ANSWERING RESULT
    # --------------------------------------

    saved_qa = st.session_state["qa_result"]

    if saved_qa:

        result = saved_qa["result"]

        st.divider()

        st.subheader("AI Analysis Result")

        st.info(
            f"Analysis Mode: {result['mode']}"
        )

        with st.container(border=True):

            st.markdown("#### Your Question")

            st.write(
                saved_qa["question"]
            )

            st.markdown("#### AI Response")

            st.write(
                result["answer"]
            )

        # ----------------------------------
        # IMAGE PROCESSING INFORMATION
        # ----------------------------------

        if result["image_processed"]:

            st.success(
                "Vision Transformer Processing Successful"
            )

            st.metric(
                "Extracted Image Features",
                result["image_features"]
            )

        # ----------------------------------
        # SUPPORTING REPORT EVIDENCE
        # ----------------------------------

        if result["page"] is not None:

            with st.container(border=True):

                st.markdown(
                    "#### Supporting Evidence"
                )

                st.success(
                    f"Source: {saved_qa['report_name']} | "
                    f"Page: {result['page']}"
                )

                st.info(
                    result["evidence"]
                )

                st.metric(
                    "Evidence Matching Indicator",
                    f"{result['confidence']}%"
                )

                st.caption(
                    "This is a prototype retrieval/matching "
                    "indicator, not calibrated medical "
                    "confidence. Direct extraction may "
                    "show 100%."
                )

        else:

            st.warning(
                "No sufficient matching report evidence "
                "was identified for this question."
            )

        # ----------------------------------
        # EVIDENCELENS VERIFICATION
        # ----------------------------------

        if pages:

            try:

                show_evidence(
                    pages,
                    result
                )

            except Exception as e:

                st.error(
                    f"EvidenceLens Error: {e}"
                )

        # ----------------------------------
        # NEXT BUTTON
        # ----------------------------------

        st.divider()

        if st.button(
            "Next → Research Results",
            type="primary",
            use_container_width=True,
            key="qa_next_research"
        ):

            go("📊 Research Results")


# ==========================================
# 20. RESEARCH RESULTS
# ==========================================

elif section == "📊 Research Results":

    st.header(
        "📊 Research Performance Dashboard"
    )

    st.info(
        "Held-out experimental evaluation using "
        "report-derived binary labels. These are "
        "not clinical diagnostic performance metrics."
    )

    # --------------------------------------
    # PERFORMANCE METRICS
    # --------------------------------------

    a, b, c, d = st.columns(4)

    with a:
        st.metric("Accuracy", "71.38%")

    with b:
        st.metric("Precision", "80.57%")

    with c:
        st.metric("Recall", "72.34%")

    with d:
        st.metric("F1 Score", "76.23%")

    st.write("")

    # --------------------------------------
    # MODEL ARCHITECTURE
    # --------------------------------------

    with st.container(border=True):

        st.subheader(
            "Experimental Model Architecture"
        )

        st.write(
            "Pretrained google/vit-base-patch16-224-in21k "
            "feature extractor with 768-dimensional CLS "
            "features and balanced Logistic Regression."
        )

        st.write(
            "Selected regularization parameter: C = 0.01"
        )

    # --------------------------------------
    # DATASET SPLIT
    # --------------------------------------

    st.subheader("Dataset Split")

    a, b, c = st.columns(3)

    with a:
        st.metric("Training", "5,237")

    with b:
        st.metric("Validation", "1,118")

    with c:
        st.metric("Testing", "1,111")

    st.caption(
        "Study UID-based dataset splitting."
    )

    st.divider()

    # --------------------------------------
    # CONFUSION MATRIX
    # --------------------------------------

    st.subheader(
        "Held-Out Test Confusion Matrix"
    )

    st.table({
        "Actual Class": [
            "Normal Report Label",
            "Other Report Labels"
        ],
        "Predicted Normal": [
            283,
            195
        ],
        "Predicted Other": [
            123,
            510
        ]
    })

    st.caption(
        "Rows represent actual report-derived labels. "
        "Columns represent experimental predictions."
    )

    st.warning(
        "Report-derived labels may contain noise. "
        "This prototype is not validated for "
        "patient diagnosis."
    )

    # --------------------------------------
    # WORKFLOW COMPLETED
    # --------------------------------------

    st.divider()

    st.success(
        "You have reached the final section "
        "of the MediVision AI workflow."
    )

    if st.button(
        "← Return to Overview",
        type="primary",
        use_container_width=True,
        key="research_back_overview"
    ):

        go("🏠 Overview")


# ==========================================
# 21. PDF DOWNLOAD FEATURE
# ==========================================

st.divider()

st.subheader("📥 Download Medical Analysis Report")

pdf_results = {}

if xray_saved:

    pdf_results["X-Ray File"] = xray_saved["name"]

if active_name:

    pdf_results["Active Medical Report"] = active_name

if pages:

    pdf_results["Extracted Report Text"] = "\n\n".join(
        f"Page {page.get('page', '-')}\n"
        f"{page.get('text', '')}"
        for page in pages
    )

vision = st.session_state["vision_result"]

if vision:

    pdf_results["X-Ray Analysis"] = (
        f"Prediction: {vision.get('prediction', 'N/A')}\n"
        f"Model Score: {vision.get('model_score', 'N/A')}%\n"
        f"Image Features: {vision.get('feature_dimension', 'N/A')}\n"
        f"Status: {vision.get('status', 'N/A')}\n"
        f"Note: {vision.get('note', '')}"
    )

summary = st.session_state["report_summary"]

if summary:

    pdf_results["Medical Report Summary"] = "\n\n".join(
        f"{item.get('title', 'Section')}\n"
        f"{item.get('text', '')}\n"
        f"Source Page: {item.get('page', '-')}"
        for item in summary
    )

terms = st.session_state["terms_result"]

if terms:

    pdf_results["Medical Terminology"] = "\n\n".join(
        f"{item.get('term', 'Term')}: "
        f"{item.get('explanation', '')}\n"
        f"Source Pages: "
        f"{', '.join(str(p) for p in item.get('pages', []))}"
        for item in terms
    )

saved_qa = st.session_state["qa_result"]

if saved_qa:

    qa = saved_qa["result"]

    pdf_results["Medical Question and Answer"] = (
        f"Question: {saved_qa.get('question', '')}\n\n"
        f"Answer: {qa.get('answer', '')}\n\n"
        f"Analysis Mode: {qa.get('mode', 'N/A')}\n"
        f"Supporting Evidence: {qa.get('evidence', '')}\n"
        f"Source Page: {qa.get('page', 'N/A')}"
    )

    if pages:

        try:

            pdf_evidence = evidence_lens(
                pages=pages,
                answer=qa.get("answer", ""),
                evidence=qa.get("evidence", "")
            )

            located = pdf_evidence.get("located")
            verification = pdf_evidence.get("verification", {})

            pdf_results["EvidenceLens Verification"] = (
                f"Status: {verification.get('status', 'N/A')}\n"
                f"Reason: {verification.get('reason', '')}\n"
                f"Located Evidence: "
                f"{located.get('evidence', '') if located else 'Not located'}\n"
                f"Source Page: "
                f"{located.get('page', 'N/A') if located else 'N/A'}"
            )

        except Exception:

            pdf_results["EvidenceLens Verification"] = (
                "Verification could not be generated."
            )


if pdf_results:

    st.caption(
        "Download the available results from your "
        "current analysis as a PDF document."
    )

    try:

        pdf_bytes = generate_medical_pdf(pdf_results)

        st.download_button(
            label="📄 Download Analysis PDF",
            data=pdf_bytes,
            file_name="MediVision_AI_Analysis_Report.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True,
            key="download_medivision_pdf"
        )

    except Exception as e:

        st.error(
            f"PDF Generation Error: {e}"
        )

else:

    st.info(
        "Upload an X-Ray or medical report "
        "to enable PDF download."
    )


# ==========================================
# 22. FOOTER
# ==========================================

st.divider()

st.caption(
    "MediVision AI | Medical Research Prototype"
)

st.caption(
    "IU Dataset reports are retrieved using image "
    "filenames and study UIDs. Filename matching "
    "alone does not verify image content."
)

st.caption(
    "Image classification and report QA are separate "
    "components, not a jointly trained fusion model."
)

st.caption(
    "Educational and research purposes only. "
    "Not intended for clinical diagnosis or treatment."
)


# ==========================================
# END OF COMPLETE APP.PY
# ==========================================