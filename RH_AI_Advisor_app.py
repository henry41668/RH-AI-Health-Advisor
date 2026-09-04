# ==============================================================================
# re:HEALTH 香港仁和體檢健康管理顧問 - STREAMLIT APPLICATION (RH_AI_Advisor_app.py)
# ==============================================================================

import streamlit as st
import streamlit.components.v1 as components

try:
    from RH_AI_Advisor_constants import (
        BASE_PACKAGE_DESCRIPTIONS,
        HUMAN_TRIGGER_MAP,
        QUESTIONNAIRE_OPTIONS,
    )
    from RH_AI_Advisor_recommendation_engine import (
        determine_health_risk,
        run_decision_engine,
    )
except ImportError:
    from constants import (
        BASE_PACKAGE_DESCRIPTIONS,
        HUMAN_TRIGGER_MAP,
        QUESTIONNAIRE_OPTIONS,
    )
    from recommendation_engine import (
        determine_health_risk,
        run_decision_engine,
    )

# ------------------------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="re:HEALTH 香港仁和體檢健康管理顧問",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------------------------------------
# re:HEALTH Executive Blue Color Palette & Design System
# ------------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        --brand-primary: #426B9D;
        --brand-dark: #1E2D6D;
        --brand-accent: #2477CD;
        --brand-light-bg: #EDF4FB;
        --brand-border: #D9E5F2;
        --text-main: #243242;
        --text-secondary: #6B7A90;
        --card-bg: #FFFFFF;
        --card-shadow: 0 10px 30px rgba(30, 45, 109, 0.06);
        --card-shadow-hover: 0 14px 36px rgba(30, 45, 109, 0.12);
        --whatsapp-green: #25D366;
        --whatsapp-green-hover: #1EBE5D;
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Noto Sans TC', -apple-system, sans-serif;
        color: var(--text-main);
    }

    .main {
        background-color: #F5F8FC;
    }

    /* Streamlit Global Button Overrides */
    button[kind="primary"] {
        background-color: var(--brand-accent) !important;
        border-color: var(--brand-accent) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        padding: 0.55rem 1.25rem !important;
        box-shadow: 0 4px 12px rgba(36, 119, 205, 0.22) !important;
        transition: all 0.25s ease !important;
    }
    button[kind="primary"]:hover {
        background-color: var(--brand-dark) !important;
        border-color: var(--brand-dark) !important;
        box-shadow: 0 6px 18px rgba(30, 45, 109, 0.3) !important;
    }
    button[kind="secondary"] {
        background-color: #FFFFFF !important;
        border-color: var(--brand-border) !important;
        color: var(--text-main) !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        transition: all 0.25s ease !important;
    }
    button[kind="secondary"]:hover {
        border-color: var(--brand-primary) !important;
        color: var(--brand-dark) !important;
        background-color: var(--brand-light-bg) !important;
    }

    /* Executive Hero Header */
    .executive-hero {
        background: linear-gradient(135deg, var(--brand-dark) 0%, var(--brand-primary) 100%);
        border-radius: 20px;
        padding: 34px 40px;
        color: #FFFFFF;
        box-shadow: 0 16px 36px rgba(30, 45, 109, 0.2);
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
    }
    .executive-hero::after {
        content: "";
        position: absolute;
        top: -50px;
        right: -50px;
        width: 220px;
        height: 220px;
        background: radial-gradient(circle, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0) 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    .hero-header-wrap {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
    }
    .hero-title {
        font-size: 27px;
        font-weight: 900;
        letter-spacing: 0.6px;
        margin: 0;
        color: #FFFFFF;
    }
    .hero-title span {
        color: #8CC4FF;
    }
    .hero-subtitle {
        font-size: 14px;
        color: #EDF4FB;
        margin-top: 6px;
        letter-spacing: 0.8px;
        font-weight: 500;
    }
    .hero-badge-tag {
        font-size: 12px;
        background: rgba(255, 255, 255, 0.14);
        padding: 6px 14px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.22);
        color: #EDF4FB;
        font-weight: 600;
        text-align: right;
    }

    /* Wizard Content Card */
    .wizard-card {
        background: #FFFFFF;
        border: 1px solid var(--brand-border);
        border-radius: 18px;
        padding: 34px 38px;
        margin-bottom: 26px;
        box-shadow: var(--card-shadow);
    }
    .wizard-card-header {
        border-bottom: 1px solid var(--brand-border);
        padding-bottom: 16px;
        margin-bottom: 26px;
    }
    .wizard-card-step-badge {
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1px;
        color: var(--brand-accent);
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .wizard-card-title {
        font-size: 22px;
        font-weight: 900;
        color: var(--brand-dark);
        margin: 0;
    }
    .wizard-card-desc {
        font-size: 14px;
        color: var(--text-secondary);
        margin-top: 6px;
        line-height: 1.6;
    }

    /* Review Summary Page */
    .review-grid-card {
        background: var(--brand-light-bg);
        border: 1px solid var(--brand-border);
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 16px;
    }
    .review-grid-label {
        font-size: 12px;
        font-weight: 800;
        color: var(--brand-primary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .review-grid-val {
        font-size: 15.5px;
        font-weight: 700;
        color: var(--text-main);
        line-height: 1.5;
    }

    /* Report Section Containers */
    .section-header-wrap {
        margin-top: 42px;
        margin-bottom: 18px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .section-pill-num {
        background-color: var(--brand-light-bg);
        color: var(--brand-accent);
        font-size: 13px;
        font-weight: 800;
        padding: 5px 12px;
        border-radius: 8px;
        border: 1px solid var(--brand-border);
    }
    .section-heading-text {
        font-size: 23px;
        font-weight: 900;
        color: var(--brand-dark);
        margin: 0;
        letter-spacing: -0.2px;
    }

    /* Premium Report Cards */
    .premium-card {
        background: #FFFFFF;
        border: 1px solid var(--brand-border);
        border-radius: 18px;
        padding: 30px 34px;
        box-shadow: var(--card-shadow);
        margin-bottom: 22px;
        position: relative;
    }

    .base-card-highlight {
        background: linear-gradient(180deg, #FFFFFF 0%, var(--brand-light-bg) 100%);
        border: 2px solid var(--brand-primary);
    }

    .addon-card-item {
        background: #FFFFFF;
        border: 1px solid var(--brand-border);
        border-radius: 16px;
        padding: 24px 28px;
        box-shadow: var(--card-shadow);
        margin-bottom: 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .addon-card-item:hover {
        border-color: var(--brand-accent);
        box-shadow: var(--card-shadow-hover);
        transform: translateY(-2px);
    }

    /* Currency and Prices */
    .currency-symbol {
        font-size: 15px;
        font-weight: 700;
        color: var(--brand-accent);
        margin-right: 3px;
    }
    .price-num-hero {
        font-size: 34px;
        font-weight: 900;
        color: var(--brand-dark);
        letter-spacing: -0.5px;
    }
    .price-num-card {
        font-size: 24px;
        font-weight: 900;
        color: var(--brand-accent);
    }
    .price-num-highlight {
        font-size: 44px;
        font-weight: 900;
        color: #FFFFFF;
        letter-spacing: -1px;
    }

    /* Blue Natural Badges */
    .trigger-natural-badge {
        display: inline-flex;
        align-items: center;
        background-color: var(--brand-light-bg);
        color: var(--brand-dark);
        border: 1px solid var(--brand-border);
        padding: 5px 13px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 6px;
    }

    /* Executive Cost Summary */
    .cost-summary-box {
        background: linear-gradient(135deg, var(--brand-dark) 0%, var(--brand-primary) 100%);
        border-radius: 20px;
        padding: 36px 40px;
        color: #FFFFFF;
        box-shadow: 0 18px 40px rgba(30, 45, 109, 0.24);
        border: 1px solid rgba(255, 255, 255, 0.12);
    }

    /* Call-To-Action (CTA) Section */
    .cta-container {
        background: #FFFFFF;
        border: 1px solid var(--brand-border);
        border-radius: 18px;
        padding: 34px 38px;
        margin-top: 26px;
        margin-bottom: 22px;
        box-shadow: var(--card-shadow);
        text-align: center;
    }
    .cta-title {
        font-size: 22px;
        font-weight: 900;
        color: var(--brand-dark);
        margin-bottom: 10px;
    }
    .cta-desc {
        font-size: 14.5px;
        color: var(--text-secondary);
        line-height: 1.7;
        margin-bottom: 26px;
    }
    .cta-btn-group {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 20px;
        flex-wrap: wrap;
    }
    .cta-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 15px 36px;
        font-size: 16px;
        font-weight: 700;
        border-radius: 12px;
        text-decoration: none !important;
        transition: all 0.25s ease;
        min-width: 220px;
        box-sizing: border-box;
    }
    .cta-btn-primary {
        background-color: var(--brand-accent);
        color: #FFFFFF !important;
        box-shadow: 0 4px 14px rgba(36, 119, 205, 0.28);
    }
    .cta-btn-primary:hover {
        background-color: var(--brand-dark);
        box-shadow: 0 6px 18px rgba(30, 45, 109, 0.35);
        transform: translateY(-2px);
    }
    .cta-btn-whatsapp {
        background-color: var(--whatsapp-green);
        color: #FFFFFF !important;
        box-shadow: 0 4px 14px rgba(37, 211, 102, 0.28);
    }
    .cta-btn-whatsapp:hover {
        background-color: var(--whatsapp-green-hover);
        box-shadow: 0 6px 18px rgba(37, 211, 102, 0.38);
        transform: translateY(-2px);
    }
    @media (max-width: 768px) {
        .cta-btn-group {
            flex-direction: column;
            gap: 14px;
        }
        .cta-btn {
            width: 100%;
        }
    }

    /* Action Next Step Cards */
    .action-step-card {
        background: #FFFFFF;
        border: 1px solid var(--brand-border);
        border-top: 4px solid var(--brand-accent);
        border-radius: 14px;
        padding: 24px 22px;
        height: 100%;
        box-shadow: var(--card-shadow);
        transition: transform 0.2s ease;
    }
    .action-step-card:hover {
        transform: translateY(-2px);
    }

    /* Print Specific Cleanups */
    @media print {
        header, footer, [data-testid="stToolbar"], .no-print {
            display: none !important;
        }
        .main {
            background-color: #FFFFFF !important;
        }
        .premium-card, .addon-card-item, .action-step-card, .cta-container {
            box-shadow: none !important;
            border: 1px solid #D9E5F2 !important;
            break-inside: avoid;
        }
        .cost-summary-box {
            background: #EDF4FB !important;
            color: #1E2D6D !important;
            border: 2px solid #426B9D !important;
        }
        .cost-summary-box * {
            color: #1E2D6D !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------------------
# Executive Header Banner
# ------------------------------------------------------------------------------
st.markdown(
    """
    <div class="executive-hero">
        <div class="hero-header-wrap">
            <div>
                <h1 class="hero-title">re:<span>HEALTH</span> 香港仁和體檢健康管理顧問</h1>
                <div class="hero-subtitle">AI 健康風險評估及體檢方案建議系統 ｜ 個人化預防醫學篩查門戶</div>
            </div>
            <div class="hero-badge-tag">
                香港私家醫療標準<br>
                100% 臨床確定性規則引擎
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------------------
# Session State Initialization
# ------------------------------------------------------------------------------
if "wizard_step" not in st.session_state:
    st.session_state.wizard_step = 1
if "calculated" not in st.session_state:
    st.session_state.calculated = False

if "selected_age" not in st.session_state:
    st.session_state.selected_age = None
if "selected_gender" not in st.session_state:
    st.session_state.selected_gender = None
if "selected_family_history" not in st.session_state:
    st.session_state.selected_family_history = []
if "selected_symptoms" not in st.session_state:
    st.session_state.selected_symptoms = []
if "selected_lifestyle" not in st.session_state:
    st.session_state.selected_lifestyle = []


def reset_assessment():
    st.session_state.wizard_step = 1
    st.session_state.calculated = False
    st.session_state.selected_age = None
    st.session_state.selected_gender = None
    st.session_state.selected_family_history = []
    st.session_state.selected_symptoms = []
    st.session_state.selected_lifestyle = []
    st.rerun()


# ==============================================================================
# MULTI-STEP WIZARD EXPERIENCE
# ==============================================================================

if not st.session_state.calculated:
    current_step = st.session_state.wizard_step

    step_labels = {
        1: "Step 1 基本資料",
        2: "Step 2 家族病史",
        3: "Step 3 自覺症狀",
        4: "Step 4 生活習慣",
        5: "Step 5 確認資料",
    }

    # --------------------------------------------------------------------------
    # Streamlit-Native Step Indicator
    # --------------------------------------------------------------------------
    progress_ratio = current_step / 5
    progress_percentage = int(progress_ratio * 100)

    prog_col1, prog_col2 = st.columns([4, 1])
    with prog_col1:
        st.write(f"### 步驟 {current_step} / 5 ： {step_labels[current_step]}")
    with prog_col2:
        st.metric(label="評估進度", value=f"{progress_percentage}%")

    st.progress(progress_ratio)
    st.write("")

    # --------------------------------------------------------------------------
    # Step 1: 基本資料 (Age, Gender) with Validation
    # --------------------------------------------------------------------------
    if current_step == 1:
        st.markdown(
            """
            <div class="wizard-card">
                <div class="wizard-card-header">
                    <div class="wizard-card-step-badge">STEP 01 / 05</div>
                    <h2 class="wizard-card-title">基本資料 (Basic Information)</h2>
                    <div class="wizard-card-desc">請選取受檢者之年齡組別與生理性別。系統將依此直接鎖定對應之專屬年度核心基礎體檢套餐。</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        age_opts = ["18-29", "30-39", "40-49", "50+"]
        gen_opts = ["Female", "Male"]

        age_curr_idx = age_opts.index(st.session_state.selected_age) if st.session_state.selected_age in age_opts else None
        gen_curr_idx = gen_opts.index(st.session_state.selected_gender) if st.session_state.selected_gender in gen_opts else None

        c_age, c_gen = st.columns(2)
        with c_age:
            age_input = st.selectbox(
                "受檢年齡組別 (Age) *",
                age_opts,
                index=age_curr_idx,
                placeholder="-- 請選擇受檢年齡組別 --",
                help="依據香港私家醫療標準之年齡分層體檢方案",
            )
        with c_gen:
            gen_input = st.selectbox(
                "生理性別 (Gender) *",
                gen_opts,
                index=gen_curr_idx,
                format_func=lambda x: "女性 (Female)" if x == "Female" else "男性 (Male)",
                placeholder="-- 請選擇生理性別 --",
                help="基礎篩檢項目涵蓋男女器官專項超聲波與代謝指標",
            )

        st.markdown("<div style='margin-top: 36px;'></div>", unsafe_allow_html=True)
        _, nav_next = st.columns([4, 1.2])
        with nav_next:
            if st.button("下一步 (Next) ➔", use_container_width=True, type="primary"):
                if age_input is None or gen_input is None:
                    st.error("⚠️ 必須選取「年齡組別」及「生理性別」，方可繼續前往下一步。")
                else:
                    st.session_state.selected_age = age_input
                    st.session_state.selected_gender = gen_input
                    st.session_state.wizard_step = 2
                    st.rerun()

    # --------------------------------------------------------------------------
    # Step 2: 家族病史 (Multi-select)
    # --------------------------------------------------------------------------
    elif current_step == 2:
        st.markdown(
            """
            <div class="wizard-card">
                <div class="wizard-card-header">
                    <div class="wizard-card-step-badge">STEP 02 / 05</div>
                    <h2 class="wizard-card-title">家族病史 (Family History)</h2>
                    <div class="wizard-card-desc">請勾選一等親或直系血親（父母、兄弟姐妹、子女）曾確診之疾病項目。若無相關家族病史，請直接點擊「下一步」。</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        fh_options = list(QUESTIONNAIRE_OPTIONS["family_history"].items())
        half_fh = len(fh_options) // 2 + 1
        curr_fh = set(st.session_state.selected_family_history)

        fh_col1, fh_col2 = st.columns(2)
        new_fh = []
        for idx, (k, label) in enumerate(fh_options):
            col_target = fh_col1 if idx < half_fh else fh_col2
            if col_target.checkbox(label, value=(k in curr_fh), key=f"step2_fh_{k}"):
                new_fh.append(k)

        st.session_state.selected_family_history = new_fh

        st.markdown("<div style='margin-top: 36px;'></div>", unsafe_allow_html=True)
        nav_prev, _, nav_next = st.columns([1.2, 2.6, 1.2])
        with nav_prev:
            if st.button("⬅ 上一步 (Previous)", use_container_width=True):
                st.session_state.wizard_step = 1
                st.rerun()
        with nav_next:
            if st.button("下一步 (Next) ➔", use_container_width=True, type="primary"):
                st.session_state.wizard_step = 3
                st.rerun()

    # --------------------------------------------------------------------------
    # Step 3: 自覺症狀 (Multi-select)
    # --------------------------------------------------------------------------
    elif current_step == 3:
        st.markdown(
            """
            <div class="wizard-card">
                <div class="wizard-card-header">
                    <div class="wizard-card-step-badge">STEP 03 / 05</div>
                    <h2 class="wizard-card-title">自覺症狀 (Current Symptoms)</h2>
                    <div class="wizard-card-desc">請勾選近期出現或反覆發生之身體警訊。若近期自覺狀態平穩無任何不適，請直接點擊「下一步」。</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        sym_options = list(QUESTIONNAIRE_OPTIONS["symptoms"].items())
        half_sym = len(sym_options) // 2 + 1
        curr_sym = set(st.session_state.selected_symptoms)

        sym_col1, sym_col2 = st.columns(2)
        new_sym = []
        for idx, (k, label) in enumerate(sym_options):
            col_target = sym_col1 if idx < half_sym else sym_col2
            if col_target.checkbox(label, value=(k in curr_sym), key=f"step3_sym_{k}"):
                new_sym.append(k)

        st.session_state.selected_symptoms = new_sym

        st.markdown("<div style='margin-top: 36px;'></div>", unsafe_allow_html=True)
        nav_prev, _, nav_next = st.columns([1.2, 2.6, 1.2])
        with nav_prev:
            if st.button("⬅ 上一步 (Previous)", use_container_width=True):
                st.session_state.wizard_step = 2
                st.rerun()
        with nav_next:
            if st.button("下一步 (Next) ➔", use_container_width=True, type="primary"):
                st.session_state.wizard_step = 4
                st.rerun()

    # --------------------------------------------------------------------------
    # Step 4: 生活習慣 (Multi-select)
    # --------------------------------------------------------------------------
    elif current_step == 4:
        st.markdown(
            """
            <div class="wizard-card">
                <div class="wizard-card-header">
                    <div class="wizard-card-step-badge">STEP 04 / 05</div>
                    <h2 class="wizard-card-title">生活習慣 (Lifestyle Factors)</h2>
                    <div class="wizard-card-desc">請勾選符合您目前日常作息的個人習慣，系統將納入早期黏膜或心腦血管之評估分析。</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        life_options = list(QUESTIONNAIRE_OPTIONS["lifestyle"].items())
        curr_life = set(st.session_state.selected_lifestyle)

        life_col1, life_col2 = st.columns(2)
        new_life = []
        for idx, (k, label) in enumerate(life_options):
            col_target = life_col1 if idx % 2 == 0 else life_col2
            if col_target.checkbox(label, value=(k in curr_life), key=f"step4_life_{k}"):
                new_life.append(k)

        st.session_state.selected_lifestyle = new_life

        st.markdown("<div style='margin-top: 36px;'></div>", unsafe_allow_html=True)
        nav_prev, _, nav_next = st.columns([1.2, 2.6, 1.2])
        with nav_prev:
            if st.button("⬅ 上一步 (Previous)", use_container_width=True):
                st.session_state.wizard_step = 3
                st.rerun()
        with nav_next:
            if st.button("前往確認 (Review) ➔", use_container_width=True, type="primary"):
                st.session_state.wizard_step = 5
                st.rerun()

    # --------------------------------------------------------------------------
    # Step 5: 確認資料 (Summary Page)
    # --------------------------------------------------------------------------
    elif current_step == 5:
        st.markdown(
            """
            <div class="wizard-card">
                <div class="wizard-card-header">
                    <div class="wizard-card-step-badge">STEP 05 / 05</div>
                    <h2 class="wizard-card-title">確認資料 (Review & Confirm)</h2>
                    <div class="wizard-card-desc">請仔細核對以下所填報之各項健康資訊。確認無誤後，請點擊下方按鈕以運行臨床確定性決策邏輯。</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        sum_col1, sum_col2 = st.columns(2)
        with sum_col1:
            gender_txt = "女性 (Female)" if st.session_state.selected_gender == "Female" else "男性 (Male)"
            st.markdown(
                f"""
                <div class="review-grid-card">
                    <div class="review-grid-label">1. 受檢基本資料 (Age & Gender)</div>
                    <div class="review-grid-val">{gender_txt} ｜ {st.session_state.selected_age} 歲組別</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            fh_names = [QUESTIONNAIRE_OPTIONS["family_history"][k] for k in st.session_state.selected_family_history]
            fh_str = "、".join(fh_names) if fh_names else "無特別申報直系家族病史"
            st.markdown(
                f"""
                <div class="review-grid-card">
                    <div class="review-grid-label">2. 直系家族病史 (共 {len(st.session_state.selected_family_history)} 項)</div>
                    <div class="review-grid-val" style="font-size: 14.5px; font-weight: 600;">{fh_str}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with sum_col2:
            sym_names = [QUESTIONNAIRE_OPTIONS["symptoms"][k] for k in st.session_state.selected_symptoms]
            sym_str = "、".join(sym_names) if sym_names else "近期無自覺異常症狀"
            st.markdown(
                f"""
                <div class="review-grid-card">
                    <div class="review-grid-label">3. 自覺身體症狀 (共 {len(st.session_state.selected_symptoms)} 項)</div>
                    <div class="review-grid-val" style="font-size: 14.5px; font-weight: 600;">{sym_str}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            life_names = [QUESTIONNAIRE_OPTIONS["lifestyle"][k] for k in st.session_state.selected_lifestyle]
            life_str = "、".join(life_names) if life_names else "作息規律良好，無高危生活因子"
            st.markdown(
                f"""
                <div class="review-grid-card">
                    <div class="review-grid-label">4. 個人生活習慣 (共 {len(st.session_state.selected_lifestyle)} 項)</div>
                    <div class="review-grid-val" style="font-size: 14.5px; font-weight: 600;">{life_str}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<div style='margin-top: 36px;'></div>", unsafe_allow_html=True)
        nav_prev, _, nav_submit = st.columns([1.2, 1.4, 2.4])
        with nav_prev:
            if st.button("⬅ 返回修改 (Previous)", use_container_width=True):
                st.session_state.wizard_step = 4
                st.rerun()
        with nav_submit:
            if st.button("生成個人化專屬健康報告", use_container_width=True, type="primary"):
                st.session_state.calculated = True
                st.rerun()


# ==============================================================================
# EXECUTIVE HEALTHCARE REPORT PAGE
# ==============================================================================

if st.session_state.calculated:
    age_eval = st.session_state.selected_age
    gender_eval = st.session_state.selected_gender
    fh_eval = st.session_state.selected_family_history
    sym_eval = st.session_state.selected_symptoms
    life_eval = st.session_state.selected_lifestyle

    results = run_decision_engine(
        age=age_eval,
        gender=gender_eval,
        family_history=fh_eval,
        symptoms=sym_eval,
        lifestyle=life_eval,
    )

    risk_info = determine_health_risk(sym_eval, fh_eval)

    if risk_info.get("en_level") == "Low Risk":
        risk_bg = "#EDF4FB"
        risk_border = "#D9E5F2"
        risk_badge = "#2477CD"
    elif risk_info.get("en_level") == "Medium Risk":
        risk_bg = "#FEF9EE"
        risk_border = "#F8DEAE"
        risk_badge = "#D97706"
    else:
        risk_bg = "#FDEDEC"
        risk_border = "#F5B7B1"
        risk_badge = "#C0392B"

    base_meta = BASE_PACKAGE_DESCRIPTIONS.get(
        results["base_package_name"],
        {
            "suitable": f"適合 {age_eval} 歲組別{'女性' if gender_eval == 'Female' else '男性'}",
            "desc": "針對該年齡層與生理性別精心規劃之年度核心健康篩查方案。",
        },
    )

    st.markdown("<div style='margin: 32px 0 26px 0; border-bottom: 2px solid #D9E5F2;'></div>", unsafe_allow_html=True)

    action_col_left, action_col_right = st.columns([2.4, 1.6])
    with action_col_left:
        st.markdown(
            f"""
            <div style="font-size: 14px; color: var(--text-secondary); padding-top: 8px;">
                受檢對象：<strong style="color: var(--brand-dark);">{'女士' if gender_eval == 'Female' else '男士'}（{age_eval} 歲）</strong> ｜ 檔案編號：<strong style="color: var(--brand-dark);">RH-{abs(hash(str(age_eval) + str(gender_eval) + str(fh_eval))) % 1000000:06d}</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with action_col_right:
        act_c1, act_c2 = st.columns([1, 1])

        with act_c1:
            components.html(
                """
                <button onclick="window.print()" style="
                    width: 100%;
                    height: 42px;
                    background: #2477CD;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    font-weight: 700;
                    font-size: 13px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 3px 8px rgba(36, 119, 205, 0.22);
                ">
                    📄 匯出報告
                </button>
                """,
                height=48,
            )

        with act_c2:
            st.button(
                "➕ 開始全新評估",
                on_click=reset_assessment,
                use_container_width=True,
                type="secondary"
        )

    # --------------------------------------------------------------------------
    # 1. Health Risk Summary
    # --------------------------------------------------------------------------
    st.markdown(
        """
        <div class="section-header-wrap">
            <span class="section-pill-num">SECTION 1</span>
            <h3 class="section-heading-text">健康風險綜合評估 (Health Risk Summary)</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="premium-card" style="background-color: {risk_bg}; border: 1.5px solid {risk_border};">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; margin-bottom: 12px;">
                <div style="font-size: 13px; font-weight: 800; color: {risk_badge}; letter-spacing: 1px; text-transform: uppercase;">
                    CLINICAL RISK STRATIFICATION
                </div>
                <div style="background-color: {risk_badge}; color: #FFFFFF; font-size: 13px; font-weight: 800; padding: 6px 18px; border-radius: 20px; letter-spacing: 0.5px;">
                    {risk_info['level']} ｜ {risk_info['en_level']}
                </div>
            </div>
            <div style="font-size: 20px; font-weight: 900; color: var(--brand-dark); margin-bottom: 10px;">
                個人化健康風險指標分級
            </div>
            <div style="font-size: 14.5px; line-height: 1.7; color: var(--text-main);">
                {risk_info['desc']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------------------------
    # 2. Recommended Base Package
    # --------------------------------------------------------------------------
    st.markdown(
        """
        <div class="section-header-wrap">
            <span class="section-pill-num">SECTION 2</span>
            <h3 class="section-heading-text">推薦年度核心基礎套餐 (Recommended Base Package)</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="premium-card base-card-highlight">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 14px;">
                <div>
                    <div style="font-size: 12.5px; font-weight: 800; color: var(--brand-primary); letter-spacing: 1px; margin-bottom: 4px;">RECOMMENDED FOUNDATION</div>
                    <div style="font-size: 27px; font-weight: 900; color: var(--brand-dark); margin-bottom: 6px;">
                        {results['base_package_name']}
                    </div>
                    <div style="display: inline-block; background: #FFFFFF; border: 1px solid var(--brand-border); color: var(--brand-accent); font-size: 13px; font-weight: 700; padding: 4px 14px; border-radius: 6px; margin-bottom: 14px;">
                        🎯 {base_meta['suitable']}
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 12.5px; color: var(--text-secondary); font-weight: 600;">基礎套餐價格</div>
                    <div style="display: flex; align-items: baseline; justify-content: flex-end; gap: 4px;">
                        <span class="currency-symbol">HKD</span>
                        <span class="price-num-hero">{results['base_package_price']:,}</span>
                    </div>
                </div>
            </div>
            <div style="font-size: 14.5px; line-height: 1.75; color: var(--text-secondary); border-top: 1px solid var(--brand-border); padding-top: 16px; margin-top: 8px;">
                {base_meta['desc']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------------------------
    # 3. Recommended Add-On Packages
    # --------------------------------------------------------------------------
    st.markdown(
        """
        <div class="section-header-wrap">
            <span class="section-pill-num">SECTION 3</span>
            <h3 class="section-heading-text">專項精準加配檢查 (Recommended Add-On Packages)</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if results["addons"]:
        for addon in results["addons"]:
            trigger_badges_html = "".join([
                f'<span class="trigger-natural-badge">✓ {HUMAN_TRIGGER_MAP.get(t, t)}</span>'
                for t in addon["triggers"]
            ])

            st.markdown(
                f"""
                <div class="addon-card-item">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px; margin-bottom: 14px;">
                        <div>
                            <div style="font-size: 19px; font-weight: 800; color: var(--brand-dark); margin-bottom: 4px;">
                                {addon['name']}
                            </div>
                            <div style="font-size: 12.5px; color: var(--text-secondary);">
                                專項早期深度預防檢測
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <span class="currency-symbol">HKD</span>
                            <span class="price-num-card">{addon['price']:,}</span>
                        </div>
                    </div>
                    <div style="margin-bottom: 14px;">
                        <div style="font-size: 12px; font-weight: 700; color: var(--text-secondary); margin-bottom: 6px;">
                            吻合臨床評估指標：
                        </div>
                        <div>
                            {trigger_badges_html}
                        </div>
                    </div>
                    <div style="background: var(--brand-light-bg); border-radius: 10px; padding: 14px 18px; border-left: 4px solid var(--brand-accent); font-size: 14px; color: var(--text-main); line-height: 1.65;">
                        <strong style="color: var(--brand-dark);">推薦理由：</strong>{addon['reasons'][0]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            """
            <div class="premium-card" style="text-align: center; padding: 40px 20px;">
                <div style="font-size: 28px; margin-bottom: 8px;">🛡️</div>
                <div style="font-size: 18px; font-weight: 800; color: var(--brand-dark); margin-bottom: 6px;">當前無額外專項加配項目</div>
                <div style="font-size: 14px; color: var(--text-secondary); max-width: 600px; margin: 0 auto; line-height: 1.65;">
                    根據您目前所填報之生理數據、自覺症狀與家族背景，推薦之核心基礎套餐已能全面覆蓋當前健康監測所需，毋須額外增加非必要之篩查項目。
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------------------------
    # 4. Estimated Cost
    # --------------------------------------------------------------------------
    st.markdown(
        """
        <div class="section-header-wrap">
            <span class="section-pill-num">SECTION 4</span>
            <h3 class="section-heading-text">預算與費用總計 (Estimated Cost)</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    addon_total_price = sum(item["price"] for item in results["addons"])

    st.markdown(
        f"""
        <div class="cost-summary-box">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 26px;">
                <div style="flex: 1; min-width: 280px;">
                    <div style="font-size: 12.5px; font-weight: 800; color: #8CC4FF; letter-spacing: 1px; text-transform: uppercase;">
                        TOTAL ESTIMATED INVESTMENT
                    </div>
                    <div style="font-size: 23px; font-weight: 900; margin-top: 4px; margin-bottom: 12px;">
                        體檢方案費用總覽
                    </div>
                    <div style="font-size: 14px; opacity: 0.92; line-height: 1.85;">
                        • 核心基礎套餐費用：<strong>HKD {results['base_package_price']:,}</strong><br>
                        • 專項加配項目費用（共 {len(results['addons'])} 項）：<strong>HKD {addon_total_price:,}</strong>
                    </div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.1); border: 1.5px solid rgba(255, 255, 255, 0.22); border-radius: 16px; padding: 22px 34px; text-align: right; min-width: 250px;">
                    <div style="font-size: 12.5px; font-weight: 700; color: rgba(255, 255, 255, 0.9); letter-spacing: 0.5px;">
                        預估總費用 (TOTAL COST)
                    </div>
                    <div style="display: flex; align-items: baseline; justify-content: flex-end; gap: 6px; margin-top: 4px;">
                        <span style="font-size: 20px; font-weight: 700; color: #8CC4FF;">HKD</span>
                        <span class="price-num-highlight">{results['total_cost']:,}</span>
                    </div>
                    <div style="font-size: 12px; color: rgba(255, 255, 255, 0.78); margin-top: 4px;">
                        包含專科醫療團隊一對一報告解讀諮詢
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------------------------
    # CALL-TO-ACTION (CTA) SECTION
    # --------------------------------------------------------------------------
    st.markdown(
        """
        <div class="cta-container">
            <h3 class="cta-title">立即開始您的健康管理旅程</h3>
            <div class="cta-desc">
                已準備好進一步了解您的檢查方案？<br>
                立即預約或聯絡健康顧問，我們將協助安排最適合您的健康檢查服務。
            </div>
            <div class="cta-btn-group">
                <a href="https://rehealth.com.hk/contact-us/#to_form" target="_blank" rel="noopener noreferrer" class="cta-btn cta-btn-primary">
                    立即預約
                </a>
                <a href="https://api.whatsapp.com/send?phone=85257264497&text=%E4%BD%A0%E5%A5%BD%EF%BC%8C%E6%88%91%E6%83%B3%E4%BA%86%E8%A7%A3%E6%9B%B4%E5%A4%9A%E9%97%9C%E6%96%BC%E9%A6%99%E6%B8%AF%E4%BB%81%E5%92%8C%E9%AB%94%E6%AA%A2%E7%9A%84%E6%9C%8D%E5%8B%99%EF%BC%88T307%EF%BC%89" target="_blank" rel="noopener noreferrer" class="cta-btn cta-btn-whatsapp">
                    WhatsApp 查詢
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------------------------
    # 5. Why We Recommend These Packages
    # --------------------------------------------------------------------------
    st.markdown(
        """
        <div class="section-header-wrap">
            <span class="section-pill-num">SECTION 5</span>
            <h3 class="section-heading-text">推薦醫學理據與分析 (Why We Recommend These Packages)</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if results["addons"]:
        for addon in results["addons"]:
            natural_triggers = [f"「{HUMAN_TRIGGER_MAP.get(t, t)}」" for t in addon["triggers"]]
            triggers_str = "、".join(natural_triggers)

            st.markdown(
                f"""
                <div class="premium-card" style="border-left: 5px solid var(--brand-accent); padding: 24px 28px; margin-bottom: 18px;">
                    <div style="font-size: 18px; font-weight: 800; color: var(--brand-dark); margin-bottom: 8px;">
                        針對項目：{addon['name']}
                    </div>
                    <div style="font-size: 14.5px; color: var(--text-main); margin-bottom: 8px; line-height: 1.65;">
                        <strong>因為您在評估中提到：</strong>
                        <span style="color: var(--brand-accent); font-weight: 700;">{triggers_str}</span>
                    </div>
                    <div style="font-size: 14px; color: var(--text-secondary); line-height: 1.7;">
                        <strong>醫療團隊臨床分析：</strong>{addon['reasons'][0]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            f"""
            <div class="premium-card" style="border-left: 5px solid var(--brand-accent); padding: 24px 28px;">
                <div style="font-size: 18px; font-weight: 800; color: var(--brand-dark); margin-bottom: 8px;">
                    針對方案：{results['base_package_name']}
                </div>
                <div style="font-size: 14.5px; color: var(--text-main); margin-bottom: 8px;">
                    <strong>臨床邏輯分析：</strong>
                    您目前並未出現消化系統不適、心血管警訊或顯著癌症家族聚集病史。
                </div>
                <div style="font-size: 14px; color: var(--text-secondary); line-height: 1.7;">
                    根據預防醫學常規指引，當前階段毋須進行過度的侵入性或高階基因測試。集中進行 <strong>{results['base_package_name']}</strong> 所包含的血液代謝功能、重要器官影像與基本生理監控，即可提供最理想且合乎成本效益的健康防護。
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------------------------
    # 6. Suggested Next Step
    # --------------------------------------------------------------------------
    st.markdown(
        """
        <div class="section-header-wrap">
            <span class="section-pill-num">SECTION 6</span>
            <h3 class="section-heading-text">後續建議跟進行動 (Suggested Next Step)</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="premium-card" style="background-color: var(--brand-light-bg); border: 1.5px solid var(--brand-border); margin-bottom: 26px;">
            <div style="font-size: 16.5px; font-weight: 800; color: var(--brand-dark); margin-bottom: 6px;">
                💡 專業醫療顧問提示
            </div>
            <div style="font-size: 14.5px; line-height: 1.75; color: var(--text-main);">
                根據您的問卷評估結果，我們建議您攜帶此報告選項與註冊西醫或醫療專業顧問進一步討論最合適的檢查細節。<br>
                <span style="font-size: 13px; color: var(--text-secondary);">
                    （Based on your questionnaire results, we recommend discussing these screening options with a healthcare professional.）
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    action_c1, action_c2, action_c3 = st.columns(3)

    with action_c1:
        st.markdown(
            """
            <div class="action-step-card">
                <div style="font-size: 12px; font-weight: 800; color: var(--brand-accent); margin-bottom: 4px;">STEP 01</div>
                <div style="font-size: 17px; font-weight: 800; color: var(--brand-dark); margin-bottom: 8px;">預約私家醫療諮詢</div>
                <div style="font-size: 13.5px; color: var(--text-secondary); line-height: 1.65;">
                    攜帶本建議書前往 re:HEALTH 仁和體檢中心或您的家庭醫生診所，確認加配篩查項目的臨床合適性並預約檔期。
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with action_c2:
        st.markdown(
            """
            <div class="action-step-card">
                <div style="font-size: 12px; font-weight: 800; color: var(--brand-accent); margin-bottom: 4px;">STEP 02</div>
                <div style="font-size: 17px; font-weight: 800; color: var(--brand-dark); margin-bottom: 8px;">檢前生活準備</div>
                <div style="font-size: 13.5px; color: var(--text-secondary); line-height: 1.65;">
                    體檢前 8 小時請保持空腹（可少量飲水）。若包含無創基因或便潛血檢查，醫療顧問將預先寄送專用無菌採樣包。
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with action_c3:
        st.markdown(
            """
            <div class="action-step-card">
                <div style="font-size: 12px; font-weight: 800; color: var(--brand-accent); margin-bottom: 4px;">STEP 03</div>
                <div style="font-size: 17px; font-weight: 800; color: var(--brand-dark); margin-bottom: 8px;">註冊醫生專屬解讀</div>
                <div style="font-size: 13.5px; color: var(--text-secondary); line-height: 1.65;">
                    檢查完成後，由香港註冊西醫為您逐項分析健康數據，並度身訂造後續的預防醫學跟進與生活飲食指導。
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Patient Notice & Legal Disclaimer
    st.markdown(
        """
        <div style="margin-top: 38px; padding: 22px 26px; background: #EBF2FA; border-radius: 14px; font-size: 12.5px; color: #5B6B80; line-height: 1.75; border: 1px solid #D9E5F2;">
            <strong>重要聲明 (Important Notice)：</strong><br>
            本報告僅供預防性個人健康管理與初步篩查參考，非正式臨床診斷依據 (This report is intended for preventive health management only)。報告中所有推薦項目均透過專家臨床確定性邏輯規則樹生成，絕無使用黑箱 AI 自行揣測。若您目前正出現急性劇烈疼痛、大量便血或其他緊急不適，請立即前往就近醫院急症室或尋求急症醫療協助。
        </div>
        """,
        unsafe_allow_html=True,
    )
