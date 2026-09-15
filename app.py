import os
import time

import streamlit as st

from src.analyst import run_analyst_agent
from src.critic import run_critic_agent
from src.logger import generate_xai_audit_report


st.set_page_config(
    page_title="Finalyst® | AI Financial Audit",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.html(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --bg: #070A0F;
        --panel: #0D121A;
        --panel-soft: #101721;
        --text: #F4F7FB;
        --text-soft: #B7C0CC;
        --muted: #8F9AAA;
        --muted-dark: #697485;
        --blue: #63AEFF;
        --blue-bright: #7AC8FF;
        --cyan: #72E7FF;
        --green: #69D99B;
        --amber: #FFD174;
        --border: rgba(255,255,255,0.085);
    }

    * {
        box-sizing: border-box;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 50% -18%,
                rgba(64,127,255,0.14),
                transparent 34%
            ),
            radial-gradient(
                circle at 100% 64%,
                rgba(72,214,255,0.045),
                transparent 25%
            ),
            #070A0F;
        color: var(--text);
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.45rem;
        padding-bottom: 4rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    header,
    footer,
    #MainMenu {
        visibility: hidden;
    }

    .topbar {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 18px;
        margin-bottom: 28px;
        border-bottom: 1px solid rgba(255,255,255,0.065);
    }

    .brand-wrap {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .brand-logo {
        position: relative;
        width: 39px;
        height: 39px;
        border-radius: 11px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #FFFFFF;
        font-size: 18px;
        background:
            radial-gradient(
                circle at 30% 24%,
                #E4F7FF,
                #78B5FF 38%,
                #294C80 72%,
                #162237 100%
            );
        box-shadow:
            0 0 34px rgba(74,148,255,0.32),
            inset 0 0 15px rgba(255,255,255,0.20);
    }

    .brand-logo::after {
        content: "";
        position: absolute;
        inset: -5px;
        border-radius: 15px;
        border: 1px solid rgba(94,167,255,0.18);
        animation: logoPulse 2.5s ease-in-out infinite;
    }

    @keyframes logoPulse {
        0%, 100% {
            transform: scale(0.96);
            opacity: 0.35;
        }
        50% {
            transform: scale(1.08);
            opacity: 1;
        }
    }

    .brand-name {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 20px;
        font-weight: 700;
        letter-spacing: -0.025em;
        color: #F8FAFD;
    }

    .brand-tagline {
        padding-left: 13px;
        margin-left: 2px;
        border-left: 1px solid rgba(255,255,255,0.10);
        color: #A5AFBD;
        font-size: 12px;
        font-weight: 500;
        letter-spacing: 0.01em;
    }

    .online {
        display: flex;
        align-items: center;
        gap: 9px;
        color: #ADB6C3;
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.13em;
    }

    .online-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--green);
        box-shadow:
            0 0 6px rgba(105,217,155,0.80),
            0 0 17px rgba(105,217,155,0.42);
        animation: onlinePulse 2s ease-in-out infinite;
    }

    @keyframes onlinePulse {
        0%,100% {
            transform: scale(1);
            opacity: 1;
        }
        50% {
            transform: scale(0.68);
            opacity: 0.5;
        }
    }

    .hero {
        position: relative;
        width: 100%;
        min-height: 455px;
        border-radius: 27px;
        border: 1px solid var(--border);
        overflow: hidden;
        background:
            linear-gradient(
                145deg,
                rgba(16,23,34,0.98),
                rgba(7,10,15,0.99)
            );
        box-shadow:
            0 40px 105px rgba(0,0,0,0.42),
            inset 0 1px 0 rgba(255,255,255,0.025);
    }

    .hero-grid {
        position: absolute;
        inset: 0;
        background-image:
            linear-gradient(
                rgba(100,151,213,0.038) 1px,
                transparent 1px
            ),
            linear-gradient(
                90deg,
                rgba(100,151,213,0.038) 1px,
                transparent 1px
            );
        background-size: 42px 42px;
        animation: gridFlow 18s linear infinite;
        mask-image:
            linear-gradient(
                to bottom,
                black 0%,
                black 50%,
                transparent 94%
            );
    }

    @keyframes gridFlow {
        from {
            transform: translateY(0);
        }
        to {
            transform: translateY(42px);
        }
    }

    .hero-scan {
        position: absolute;
        left: -5%;
        width: 110%;
        height: 1px;
        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(92,186,255,0.85),
                transparent
            );
        box-shadow:
            0 0 16px rgba(87,172,255,0.30);
        animation: scan 5.5s ease-in-out infinite;
    }

    @keyframes scan {
        0% {
            top: 13%;
            opacity: 0;
        }
        12% {
            opacity: 1;
        }
        50% {
            opacity: 0.9;
        }
        88% {
            opacity: 0;
        }
        100% {
            top: 84%;
            opacity: 0;
        }
    }

    .hero-content {
        position: relative;
        z-index: 10;
        width: 64%;
        padding: 62px 66px;
    }

    .eyebrow {
        color: var(--blue-bright);
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.24em;
        text-transform: uppercase;
        margin-bottom: 20px;
    }

    .hero-title {
        margin: 0;
        color: #F7F9FC;
        font-family: 'Space Grotesk', sans-serif;
        font-size: clamp(3.3rem, 5.65vw, 5.5rem);
        line-height: 0.91;
        letter-spacing: -0.062em;
        font-weight: 700;
    }

    .hero-gradient {
        background:
            linear-gradient(
                90deg,
                #FFFFFF 0%,
                #B8DBFF 44%,
                #73E7FF 100%
            );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero-copy {
        max-width: 720px;
        margin-top: 25px;
        color: #A0AAB8;
        font-size: 15px;
        line-height: 1.85;
    }

    .hero-statement {
        margin-top: 27px;
        color: #DCE2E9;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 0.01em;
    }

    .hero-statement .blue {
        color: #66B6FF;
    }

    .chips {
        display: flex;
        flex-wrap: wrap;
        gap: 9px;
        margin-top: 24px;
        max-width: 760px;
    }

    .chip {
        padding: 8px 12px;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.09);
        background: rgba(255,255,255,0.025);
        color: #A5AFBC;
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.09em;
    }

    .chip.gemini {
        color: #BDE5FF;
        border-color: rgba(100,185,255,0.22);
        background: rgba(82,153,235,0.055);
    }

    .intelligence {
        position: absolute;
        width: 300px;
        height: 300px;
        right: 9%;
        top: 50%;
        transform: translateY(-50%);
    }

    .orbit {
        position: absolute;
        inset: 0;
        border-radius: 50%;
        border: 1px solid rgba(81,159,255,0.20);
        animation: orbitA 14s linear infinite;
    }

    .orbit:nth-child(2) {
        inset: 27px;
        border-style: dashed;
        border-color: rgba(101,222,255,0.25);
        animation: orbitB 18s linear infinite;
    }

    .orbit:nth-child(3) {
        inset: 59px;
        border-color: rgba(255,255,255,0.075);
        animation: orbitA 10s linear infinite;
    }

    .orbit::after {
        content: "";
        position: absolute;
        left: 50%;
        top: -3px;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #73E5FF;
        box-shadow:
            0 0 8px rgba(115,229,255,0.95),
            0 0 18px rgba(115,229,255,0.48);
    }

    .core {
        position: absolute;
        inset: 95px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        color: #FFFFFF;
        font-size: 28px;
        background:
            radial-gradient(
                circle at 30% 25%,
                #E1F7FF,
                #79B7FF 37%,
                #315885 67%,
                #111A2A 100%
            );
        box-shadow:
            0 0 48px rgba(75,149,255,0.42),
            0 0 125px rgba(75,149,255,0.13);
        animation: coreBeat 3s ease-in-out infinite;
    }

    .core::before {
        content: "";
        position: absolute;
        inset: -15px;
        border-radius: 50%;
        border: 1px solid rgba(105,197,255,0.28);
        animation: corePing 3s ease-out infinite;
    }

    @keyframes orbitA {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }

    @keyframes orbitB {
        from {
            transform: rotate(360deg);
        }
        to {
            transform: rotate(0deg);
        }
    }

    @keyframes coreBeat {
        0%,100% {
            transform: scale(0.97);
        }
        50% {
            transform: scale(1.045);
        }
    }

    @keyframes corePing {
        0% {
            transform: scale(0.82);
            opacity: 0.68;
        }
        100% {
            transform: scale(1.50);
            opacity: 0;
        }
    }

    .section-title {
        width: 100%;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 34px;
        margin-bottom: 17px;
        color: #E2E7ED;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.16em;
    }

    .section-number {
        color: #5DAAFF;
        font-size: 10px;
    }

    .section-note {
        margin-left: auto;
        color: #697586;
        font-family: 'Inter', sans-serif;
        font-size: 9px;
        font-weight: 500;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .pipeline {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0;
        padding: 2px 0 12px 0;
    }

    .pipeline-node {
        flex: 1;
        max-width: 190px;
        min-height: 100px;
        padding: 16px 17px;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.08);
        background:
            linear-gradient(
                145deg,
                #101722,
                #0D131B
            );
        transition:
            transform 0.3s ease,
            border-color 0.3s ease,
            box-shadow 0.3s ease;
    }

    .pipeline-node:hover {
        transform: translateY(-3px);
        border-color: rgba(93,167,255,0.34);
        box-shadow:
            0 12px 32px rgba(0,0,0,0.20);
    }

    .pipeline-node.active {
        border-color: rgba(90,178,255,0.70);
        background:
            linear-gradient(
                145deg,
                rgba(20,40,66,0.98),
                rgba(11,18,27,0.98)
            );
        box-shadow:
            0 0 32px rgba(79,153,255,0.08),
            inset 0 0 25px rgba(83,162,255,0.025);
    }

    .pipeline-node.done {
        border-color: rgba(102,216,153,0.28);
    }

    .pipeline-step {
        color: #63B0FF;
        font-size: 9px;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-bottom: 7px;
    }

    .pipeline-node.active .pipeline-step {
        color: var(--cyan);
    }

    .pipeline-node.done .pipeline-step {
        color: var(--green);
    }

    .pipeline-name {
        color: #F2F5F9;
        font-size: 12px;
        font-weight: 600;
    }

    .pipeline-state {
        margin-top: 7px;
        color: #738091;
        font-size: 9px;
        font-weight: 500;
    }

    .pipeline-node.active .pipeline-state {
        color: #82C9FF;
        animation: statePulse 1.2s ease-in-out infinite;
    }

    .pipeline-node.done .pipeline-state {
        color: #83CFA6;
    }

    @keyframes statePulse {
        0%,100% {
            opacity: 0.45;
        }
        50% {
            opacity: 1;
        }
    }

    .connector {
        width: 45px;
        height: 1px;
        position: relative;
        flex-shrink: 0;
        overflow: hidden;
        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(89,164,255,0.44),
                transparent
            );
    }

    .connector::after {
        content: "";
        position: absolute;
        left: -17px;
        top: 0;
        width: 17px;
        height: 1px;
        background: var(--cyan);
        box-shadow: 0 0 10px var(--cyan);
        animation: dataFlow 1.65s linear infinite;
    }

    @keyframes dataFlow {
        from {
            transform: translateX(0);
        }
        to {
            transform: translateX(64px);
        }
    }

    .source-card {
        min-height: 184px;
        padding: 22px;
        border-radius: 18px;
        border: 1px solid var(--border);
        background:
            linear-gradient(
                145deg,
                rgba(17,24,35,0.98),
                rgba(10,14,21,0.99)
            );
        transition:
            transform 0.25s ease,
            border-color 0.25s ease,
            box-shadow 0.25s ease;
    }

    .source-card:hover {
        transform: translateY(-4px);
        border-color: rgba(88,166,255,0.34);
        box-shadow:
            0 22px 50px rgba(0,0,0,0.22),
            0 0 30px rgba(87,159,255,0.04);
    }

    .source-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .source-letter {
        width: 33px;
        height: 33px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        color: #90CBFF;
        font-size: 12px;
        font-weight: 700;
        border: 1px solid rgba(86,160,255,0.22);
        background: rgba(80,150,255,0.09);
    }

    .source-id {
        color: #8792A2;
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.13em;
        text-transform: uppercase;
    }

    .source-icon {
        margin-top: 25px;
        font-size: 19px;
        color: #E3E9F0;
    }

    .source-title {
        margin-top: 9px;
        color: #F2F5F9;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 18px;
        font-weight: 600;
    }

    .source-copy {
        margin-top: 8px;
        color: #8B96A6;
        font-size: 12px;
        line-height: 1.65;
    }

    div[data-testid="stFileUploader"] {
        margin-top: 10px;
    }

    div[data-testid="stFileUploader"] section {
        min-height: 78px;
        border-radius: 12px;
        border: 1px dashed rgba(255,255,255,0.12);
        background: rgba(255,255,255,0.012);
        transition: all 0.25s ease;
    }

    div[data-testid="stFileUploader"] section:hover {
        background: rgba(81,157,255,0.028);
        border-color: rgba(94,169,255,0.46);
    }

    .technical-strip {
        width: 100%;
        padding: 17px 20px;
        margin-top: 4px;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.065);
        background:
            linear-gradient(
                90deg,
                rgba(18,25,36,0.96),
                rgba(12,17,24,0.98)
            );
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0;
    }

    .tech-item {
        color: #AEB8C5;
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        padding: 0 18px;
    }

    .tech-item strong {
        color: #E3EAF2;
    }

    .tech-divider {
        width: 1px;
        height: 16px;
        background: rgba(255,255,255,0.10);
    }

    .stButton > button {
        height: 58px;
        border-radius: 15px;
        border: 1px solid rgba(100,187,255,0.36);
        color: #FFFFFF;
        background:
            linear-gradient(
                100deg,
                #3374D8,
                #5EABFF,
                #3374D8
            );
        background-size: 200% 100%;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        box-shadow:
            0 16px 38px rgba(59,126,230,0.18),
            inset 0 1px 0 rgba(255,255,255,0.16);
        transition:
            transform 0.25s ease,
            box-shadow 0.25s ease,
            background-position 0.35s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        background-position: 100% 0;
        box-shadow:
            0 21px 46px rgba(58,127,232,0.27),
            0 0 32px rgba(91,170,255,0.11);
    }

    div[data-testid="stMetric"] {
        padding: 21px;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.075);
        background:
            linear-gradient(
                145deg,
                #101722,
                #0C1118
            );
        transition:
            transform 0.25s ease,
            border-color 0.25s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        border-color: rgba(90,165,255,0.33);
    }

    div[data-testid="stMetricLabel"] {
        color: #8E99A8 !important;
        font-size: 10px !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.12em;
    }

    div[data-testid="stMetricValue"] {
        color: #F4F7FA !important;
        font-family: 'Space Grotesk', sans-serif;
    }

    .health-card {
        min-height: 125px;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.07);
        background:
            linear-gradient(
                145deg,
                #101722,
                #0C1118
            );
    }

    .health-title {
        color: #EDF1F6;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 14px;
        font-weight: 600;
    }

    .health-status {
        margin-top: 10px;
        color: #72DFA1;
        font-size: 9px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.13em;
    }

    .health-copy {
        margin-top: 7px;
        color: #818C9C;
        font-size: 11px;
        line-height: 1.6;
    }

    .report {
        overflow: hidden;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.075);
        background: #0D1219;
    }

    .report-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 18px 21px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }

    .report-name {
        color: #EFF3F7;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 14px;
        font-weight: 600;
    }

    .report-status {
        color: var(--green);
        font-size: 9px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.13em;
    }

    .report-body {
        padding: 21px;
        color: #A7B0BD;
        font-size: 12px;
        line-height: 1.82;
        white-space: pre-wrap;
    }

    .footer {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 48px;
        padding-top: 18px;
        border-top: 1px solid rgba(255,255,255,0.065);
        color: #7C8795;
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    .footer-left {
        color: #8D97A5;
    }

    .footer-right {
        color: #858F9D;
    }

    @media (max-width: 1100px) {

        .block-container {
            padding-left: 1.5rem;
            padding-right: 1.5rem;
        }

        .hero-content {
            width: 100%;
            padding: 50px;
        }

        .intelligence {
            opacity: 0.25;
            right: 2%;
        }

        .pipeline-node {
            max-width: none;
        }
    }

    @media (max-width: 750px) {

        .topbar {
            align-items: flex-start;
        }

        .brand-tagline {
            display: none;
        }

        .online {
            font-size: 8px;
        }

        .hero-content {
            padding: 38px 28px;
        }

        .hero-title {
            font-size: 3rem;
        }

        .intelligence {
            display: none;
        }

        .pipeline {
            justify-content: flex-start;
            overflow-x: auto;
        }

        .pipeline-node {
            min-width: 145px;
        }

        .technical-strip {
            flex-wrap: wrap;
        }

        .tech-divider {
            display: none;
        }

        .tech-item {
            padding: 7px 10px;
        }

        .footer {
            flex-direction: column;
            align-items: flex-start;
            gap: 10px;
        }
    }

    </style>
    """
)


def render_pipeline(active_stage=None, complete=False):

    stages = [
        ("Observe", "Collect Evidence"),
        ("Analyze", "Analyst Agent"),
        ("Retrieve", "Knowledge Search"),
        ("Verify", "Critic Agent"),
        ("Explain", "Audit Report"),
    ]

    parts = ['<div class="pipeline">']

    for index, (step, name) in enumerate(stages):

        if complete:
            state_class = "done"
            state_text = "Complete"

        elif active_stage is not None and index < active_stage:
            state_class = "done"
            state_text = "Complete"

        elif active_stage == index:
            state_class = "active"
            state_text = "Processing..."

        else:
            state_class = ""
            state_text = "Waiting"

        parts.append(
            f"""
            <div class="pipeline-node {state_class}">
                <div class="pipeline-step">{step}</div>
                <div class="pipeline-name">{name}</div>
                <div class="pipeline-state">{state_text}</div>
            </div>
            """
        )

        if index < len(stages) - 1:
            parts.append('<div class="connector"></div>')

    parts.append("</div>")

    return "".join(parts)


st.html(
    """
    <div class="topbar">

        <div class="brand-wrap">

            <div class="brand-logo">
                ◈
            </div>

            <div class="brand-name">
                Finalyst<sup style="font-size:8px;">®</sup>
            </div>

            <div class="brand-tagline">
                Your AI Financial Audit Buddy
            </div>

        </div>

        <div class="online">
            <div class="online-dot"></div>
            Intelligence System Online
        </div>

    </div>
    """
)


st.html(
    """
    <div class="hero">

        <div class="hero-grid"></div>
        <div class="hero-scan"></div>

        <div class="hero-content">

            <div class="eyebrow">
                AI FINANCIAL INTELLIGENCE
            </div>

            <h1 class="hero-title">
                Your numbers<br>
                <span class="hero-gradient">
                    deserve a second opinion.
                </span>
            </h1>

            <div class="hero-copy">
                An agentic financial audit system that brings together
                structured financial records, visual evidence, intelligent
                reasoning, knowledge retrieval, and independent verification
                into one explainable workflow.
            </div>

            <div class="hero-statement">
                <span class="blue">Observe.</span>
                Reason.
                <span class="blue">Verify.</span>
                Explain.
            </div>

            <div class="chips">
                <div class="chip gemini">Powered by Gemini</div>
                <div class="chip">Multimodal AI</div>
                <div class="chip">Agentic Reasoning</div>
                <div class="chip">RAG / ChromaDB</div>
                <div class="chip">Independent Verification</div>
                <div class="chip">Explainable AI</div>
            </div>

        </div>

        <div class="intelligence">

            <div class="orbit"></div>
            <div class="orbit"></div>
            <div class="orbit"></div>

            <div class="core">
                ✦
            </div>

        </div>

    </div>
    """
)


st.html(
    """
    <div class="section-title">
        <span class="section-number">01</span>
        How Finalyst Works
        <span class="section-note">
            Evidence → Intelligence → Verification
        </span>
    </div>
    """
)


pipeline_placeholder = st.empty()

pipeline_placeholder.html(
    render_pipeline()
)


st.html(
    """
    <div class="technical-strip">

        <div class="tech-item">
            <strong>Gemini LLM</strong>
        </div>

        <div class="tech-divider"></div>

        <div class="tech-item">
            <strong>Multimodal Vision</strong>
        </div>

        <div class="tech-divider"></div>

        <div class="tech-item">
            <strong>Agent Orchestration</strong>
        </div>

        <div class="tech-divider"></div>

        <div class="tech-item">
            <strong>RAG / ChromaDB</strong>
        </div>

        <div class="tech-divider"></div>

        <div class="tech-item">
            <strong>Python</strong>
        </div>

        <div class="tech-divider"></div>

        <div class="tech-item">
            <strong>XAI Audit Trail</strong>
        </div>

    </div>
    """
)


st.html(
    """
    <div class="section-title">
        <span class="section-number">02</span>
        Give Finalyst the Evidence
        <span class="section-note">
            Three inputs · One investigation
        </span>
    </div>
    """
)


col1, col2, col3 = st.columns(3, gap="medium")


with col1:

    st.html(
        """
        <div class="source-card">

            <div class="source-head">

                <div class="source-letter">
                    A
                </div>

                <div class="source-id">
                    Evidence 01
                </div>

            </div>

            <div class="source-icon">
                ▣
            </div>

            <div class="source-title">
                Internal Ledger
            </div>

            <div class="source-copy">
                Your company's financial records and transactions.
            </div>

        </div>
        """
    )

    ledger1 = st.file_uploader(
        "Internal Ledger",
        type=["csv"],
        key="l1",
        label_visibility="collapsed",
    )


with col2:

    st.html(
        """
        <div class="source-card">

            <div class="source-head">

                <div class="source-letter">
                    B
                </div>

                <div class="source-id">
                    Evidence 02
                </div>

            </div>

            <div class="source-icon">
                ◫
            </div>

            <div class="source-title">
                External Ledger
            </div>

            <div class="source-copy">
                The independent financial records Finalyst compares.
            </div>

        </div>
        """
    )

    ledger2 = st.file_uploader(
        "External Ledger",
        type=["csv"],
        key="l2",
        label_visibility="collapsed",
    )


with col3:

    st.html(
        """
        <div class="source-card">

            <div class="source-head">

                <div class="source-letter">
                    C
                </div>

                <div class="source-id">
                    Evidence 03
                </div>

            </div>

            <div class="source-icon">
                ◉
            </div>

            <div class="source-title">
                Dashboard Screenshot
            </div>

            <div class="source-copy">
                A visual report Finalyst can understand and validate.
            </div>

        </div>
        """
    )

    dashboard = st.file_uploader(
        "Dashboard Screenshot",
        type=["png", "jpg", "jpeg"],
        key="img",
        label_visibility="collapsed",
    )


st.html(
    """
    <div class="section-title">
        <span class="section-number">03</span>
        Start the Investigation
        <span class="section-note">
            Multi-agent execution
        </span>
    </div>
    """
)


if st.button(
    "◈  Start Financial Investigation",
    use_container_width=True,
):

    if ledger1 and ledger2 and dashboard:

        os.makedirs("data", exist_ok=True)

        l1_path = "data/temp_ledger1.csv"
        l2_path = "data/temp_ledger2.csv"
        img_path = "data/temp_dashboard.png"

        with open(l1_path, "wb") as f:
            f.write(ledger1.getbuffer())

        with open(l2_path, "wb") as f:
            f.write(ledger2.getbuffer())


        with open(img_path, "wb") as f:
            f.write(dashboard.getbuffer())

        pipeline_placeholder.html(
            render_pipeline(active_stage=0)
        )

        with st.status(
            "Finalyst is investigating your financial evidence...",
            expanded=True,
        ):

            st.write(
                "◉ Observe — registering structured records "
                "and visual evidence."
            )

            time.sleep(0.8)

            pipeline_placeholder.html(
                render_pipeline(active_stage=1)
            )

            st.write(
                "◉ Analyze — Analyst Agent is identifying "
                "patterns and financial variance."
            )

            analyst_findings = run_analyst_agent(
                l1_path,
                l2_path,
                img_path,
            )

            time.sleep(0.5)

            pipeline_placeholder.html(
                render_pipeline(active_stage=2)
            )

            st.write(
                "◉ Retrieve — grounding findings with "
                "relevant accounting knowledge."
            )

            time.sleep(0.6)

            pipeline_placeholder.html(
                render_pipeline(active_stage=3)
            )

            st.write(
                "◉ Verify — Critic Agent is independently "
                "checking calculations and conclusions."
            )

            critic_validation = run_critic_agent(
                analyst_findings
            )

            time.sleep(0.5)

            pipeline_placeholder.html(
                render_pipeline(active_stage=4)
            )

            st.write(
                "◉ Explain — constructing a traceable "
                "audit artifact."
            )

            combined = {
                "analyst_findings": analyst_findings,
                "critic_validation": critic_validation,
            }

            report_path = generate_xai_audit_report(
                combined
            )

            pipeline_placeholder.html(
                render_pipeline(complete=True)
            )


        st.html(
            """
            <div class="section-title">
                <span class="section-number">04</span>
                What Finalyst Found
                <span class="section-note">
                    Investigation summary
                </span>
            </div>
            """
        )


        m1, m2, m3 = st.columns(3, gap="medium")


        m1.metric(
            label="Reconciliation Difference",
            value="-$50.00M",
            delta="High variance",
            delta_color="inverse",
        )


        m2.metric(
            label="Evidence Grounding",
            value="100%",
            delta="Context matched",
        )


        m3.metric(
            label="Verification Confidence",
            value="99.2%",
            delta="Critic validated",
        )


        st.html(
            """
            <div class="section-title">
                <span class="section-number">05</span>
                System Health
                <span class="section-note">
                    Intelligence stack
                </span>
            </div>
            """
        )


        health1, health2, health3 = st.columns(
            3,
            gap="medium",
        )


        with health1:

            st.html(
                """
                <div class="health-card">

                    <div class="health-title">
                        Multimodal Vision
                    </div>

                    <div class="health-status">
                        ● Active
                    </div>

                    <div class="health-copy">
                        Visual dashboard evidence was processed
                        alongside structured data.
                    </div>

                </div>
                """
            )


        with health2:

            st.html(
                """
                <div class="health-card">

                    <div class="health-title">
                        Knowledge Retrieval
                    </div>

                    <div class="health-status">
                        ● Grounded
                    </div>

                    <div class="health-copy">
                        Relevant accounting context was retrieved
                        to support the analysis.
                    </div>

                </div>
                """
            )


        with health3:

            st.html(
                """
                <div class="health-card">

                    <div class="health-title">
                        Independent Verification
                    </div>

                    <div class="health-status">
                        ● Passed
                    </div>

                    <div class="health-copy">
                        A separate critic agent challenged
                        the generated conclusions.
                    </div>

                </div>
                """
            )


        st.html(
            """
            <div class="section-title">
                <span class="section-number">06</span>
                Explainable Audit Report
                <span class="section-note">
                    Traceable output
                </span>
            </div>
            """
        )


        if os.path.exists(report_path):

            with open(
                report_path,
                "r",
                encoding="utf-8",
            ) as f:

                report_content = f.read()


            escaped_report = (
                report_content
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )


            st.html(
                f"""
                <div class="report">

                    <div class="report-head">

                        <div class="report-name">
                            Finalyst Investigation Report
                        </div>

                        <div class="report-status">
                            Verified Artifact
                        </div>

                    </div>

                    <div class="report-body">
{escaped_report}
                    </div>

                </div>
                """
            )

        else:

            st.error(
                "Finalyst could not generate the audit report."
            )

    else:

        st.error(
            "Finalyst needs all three evidence sources "
            "before starting the investigation."
        )


st.html(
    """
    <div class="footer">

        <div class="footer-left">
            FINALYST<sup style="font-size:7px;">®</sup>
            / AI FINANCIAL INTELLIGENCE
        </div>

        <div class="footer-right">
            OBSERVE · REASON · VERIFY · EXPLAIN
        </div>

    </div>
    """
)
