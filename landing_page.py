import streamlit as st
import streamlit.components.v1 as components


def show_landing_page():

    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(115deg, #FFFFFF, #EAF6FF);
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
    }

    .mv-label {
        display: inline-block;
        background: #DDF1FF;
        color: #087EB4;
        padding: 9px 17px;
        border-radius: 30px;
        font-size: 12px;
        font-weight: 750;
        letter-spacing: 1px;
    }

    .mv-brand {
        font-size: clamp(38px, 5vw, 65px);
        font-weight: 850;
        color: #12376B;
        letter-spacing: -2px;
        margin-top: 40px;
    }

    .mv-brand span {
        color: #05A7C7;
    }

    .mv-title {
        color: #173B60;
        font-size: clamp(23px, 2.5vw, 34px);
        line-height: 1.4;
        font-weight: 750;
        margin-top: 25px;
    }

    .mv-description {
        color: #557692;
        font-size: 16px;
        line-height: 1.8;
        margin-top: 18px;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #078FD0, #00A8BB);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 15px 32px;
        font-weight: 750;
        box-shadow: 0 8px 20px #168BB644;
    }
    </style>
    """, unsafe_allow_html=True)

    left, right = st.columns([1.05, 1], gap="large")

    # LEFT SIDE
    with left:

        st.markdown("""
<div class="mv-label">
    ✚ AI-POWERED MEDICAL RESEARCH PLATFORM
</div>

<div class="mv-brand">
    MediVision <span>AI</span>
</div>

<div class="mv-title">
    Multimodal AI-Based Medical Report
    Understanding with Question Answering
    Using Vision Transformer
</div>

<div class="mv-description">
    Explore X-Ray analysis, medical report
    understanding, intelligent question answering
    and evidence-based insights through one
    integrated research platform.
</div>
        """, unsafe_allow_html=True)

        st.write("")

        if st.button(
            "Enter MediVision AI →",
            type="primary",
            use_container_width=True
        ):
            st.session_state["entered"] = True
            st.rerun()

        st.caption(
            "Educational research prototype • "
            "Not for clinical diagnosis"
        )

    # RIGHT SIDE
    with right:

        components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: transparent;
    overflow: hidden;
}

.visual {
    position: relative;
    height: 490px;
    width: 100%;
    background: radial-gradient(
        ellipse at center,
        #B9E4FF,
        #EAF6FF 70%
    );
    border: 1px solid #D0EAFB;
    border-radius: 35px;
    overflow: hidden;
}

.platform {
    position: absolute;
    bottom: 25px;
    left: 10%;
    width: 80%;
    height: 48px;
    border: 3px solid #79C8F2;
    border-radius: 50%;
    background: #B7E8FF55;
    box-shadow: 0 0 35px #58B9F766;
}

.xray {
    position: absolute;
    top: 100px;
    left: 9%;
    width: 50%;
    height: 260px;
    background: linear-gradient(145deg, #082A50, #12679B);
    border: 7px solid #168BC4;
    border-radius: 19px;
    box-shadow: 0 20px 45px #1377B555;
    transform: rotate(-6deg);
    animation: floatXray 4s ease-in-out infinite;
    text-align: center;
    padding: 15px;
    color: white;
}

.lungs {
    font-size: 105px;
    margin-top: 20px;
    filter: drop-shadow(0 0 12px #83DAFF);
}

.report {
    position: absolute;
    right: 4%;
    top: 145px;
    width: 47%;
    background: white;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 15px 35px #387CA944;
    animation: floatCard 5s ease-in-out infinite;
    color: #17466C;
}

.line {
    height: 7px;
    background: #D5EAF7;
    border-radius: 8px;
    margin: 12px 0;
}

.insight {
    background: #E3FAF5;
    color: #087F7A;
    padding: 9px;
    border-radius: 9px;
    font-size: 12px;
    margin-top: 15px;
}

.qa {
    position: absolute;
    right: 8%;
    bottom: 65px;
    width: 54%;
    padding: 16px;
    background: white;
    color: #19527B;
    border-radius: 14px;
    box-shadow: 0 10px 30px #387CA944;
    font-size: 13px;
    animation: floatCard 4.5s ease-in-out infinite;
}

.ambulance {
    position: absolute;
    top: 15px;
    left: -70px;
    font-size: 52px;
    animation: driving 10s linear infinite;
}

.ai {
    position: absolute;
    top: 65px;
    right: 24%;
    font-size: 42px;
    animation: floatCard 3s ease-in-out infinite;
}

.pulse {
    position: absolute;
    left: 8%;
    bottom: 80px;
    font-size: 30px;
    color: #0799BD;
    animation: pulse 2s ease-in-out infinite;
}

@keyframes floatXray {
    0%, 100% {
        transform: translateY(0) rotate(-6deg);
    }
    50% {
        transform: translateY(-12px) rotate(-6deg);
    }
}

@keyframes floatCard {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-12px); }
}

@keyframes driving {
    from { left: -70px; }
    to { left: 110%; }
}

@keyframes pulse {
    0%, 100% { opacity: 0.4; }
    50% { opacity: 1; }
}

@media (prefers-reduced-motion: reduce) {
    .xray, .report, .qa, .ambulance, .ai, .pulse {
        animation: none;
    }
    .xray { transform: rotate(-6deg); }
    .ambulance { left: 70%; }
}
</style>
</head>

<body>

<div class="visual">

    <div class="platform"></div>

    <div class="ambulance">🚑</div>

    <div class="ai">🧠</div>

    <div class="xray">
        <strong>✚ X-RAY ANALYSIS</strong>
        <div class="lungs">🫁</div>
        <small>Vision Transformer</small>
    </div>

    <div class="report">
        <strong>✚ Medical Report</strong>

        <div class="line"></div>
        <div class="line" style="width:75%"></div>
        <div class="line" style="width:90%"></div>

        <div class="insight">
            ✓ AI Report Processing
        </div>
    </div>

    <div class="pulse">♡ ∿∿∿</div>

    <div class="qa">
        <strong>💬 Medical Question Answering</strong>
        <p>Intelligent report understanding</p>
        <span style="color:#079B9B">
            ✓ EvidenceLens
        </span>
    </div>

</div>

</body>
</html>
        """, height=510, scrolling=False)