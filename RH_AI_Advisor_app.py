# ==============================================================================
# re:HEALTH AI Health Advisor - STREAMLIT PRESENTATION LAYER
# ==============================================================================

import streamlit as st
import streamlit.components.v1 as components

from constants import (
    BASE_PACKAGE_DESCRIPTIONS,
    HUMAN_TRIGGER_MAP,
    QUESTIONNAIRE_OPTIONS,
)
from recommendation_engine import (
    determine_health_risk,
    run_decision_engine,
)

# Page Setup
st.set_page_config(
    page_title="re:HEALTH 智選醫療顧問",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Premium Hong Kong Private Healthcare Styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;600;700;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        --re-dark-green: #064433;
        --re-primary-green: #007A55;
        --re-accent-mint: #E8F5F1;
        --re-warm-white: #FAFDFB;
        --re-card-bg: #FFFFFF;
        --re-text-main: #1C2D27;
        --re-text-muted: #536B63;
        --re-gold: #B38F4D;
        --re-border: #DDEBE5;
        --re-card-shadow: 0 10px 25px rgba(6, 68, 51, 0.05);
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Noto Sans TC', -apple-system, sans-serif;
        color: var(--re-text-main);
    }

    .main {
        background-color: #F6FAF8;
    }

    .executive-header {
        background: linear-gradient(135deg, #06392B 0%, #007A55 100%);
        border-radius: 18px;
        padding: 36px 40px;
        color: #FFFFFF;
        box-shadow: 0 12px 30px rgba(0, 122, 85, 0.16);
        margin-bottom: 30px;
    }

    .brand-title-wrap {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
    }

    .brand-name {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: 0.5px;
    }

    .brand-name span {
        color: #64E7B8;
    }

    .brand-subtitle {
        font-size: 13.5px;
        color: rgba(255, 255, 255, 0.85);
        margin-top: 6px;
        letter-spacing: 0.8px;
    }

    .form-card {
        background: #FFFFFF;
        border: 1px solid var(--re-border);
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: var(--re-card-shadow);
    }

    .form-card-title {
        font-size: 15px;
        font-weight: 700;
        color: var(--re-primary-green);
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 14px;
        padding-bottom: 8px;
        border-bottom: 1px solid #EEF4F1;
    }

    .section-header-wrap {
        margin-top: 36px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .section-pill-num {
        background-color: var(--re-accent-mint);
        color: var(--re-primary-green);
        font-size: 13px;
        font-weight: 800;
        padding: 4px 10px;
        border-radius: 8px;
        border: 1px solid #A4DEC8;
    }

    .section-heading-text {
        font-size: 22px;
        font-weight: 800;
        color: var(--re-dark-green);
        margin: 0;
    }

    .premium-card {
        background: #FFFFFF;
        border: 1px solid var(--re-border);
        border-radius: 16px;
        padding: 28px 30px;
        box-shadow: var(--re-card-shadow);
        margin-bottom: 20px;
        position: relative;
    }

    .base-card-highlight {
        background: linear-gradient(180deg, #FFFFFF 0%, #F4FAF7 100%);
        border: 2px solid #8FD2BD;
    }

    .addon-card-item {
        background: #FFFFFF;
        border: 1px solid #D6E8E0;
        border-radius: 14px;
        padding: 22px 24px;
        box-shadow: 0 4px 12px rgba(0, 122, 85, 0.04);
        margin-bottom: 18px;
    }

    .addon-card-item:hover {
        border-color: #7BC8AF;
        box-shadow: 0 8px 20px rgba(0, 122, 85, 0.08);
    }

    .currency-symbol {
        font-size: 15px;
        font-weight: 700;
        color: var(--re-primary-green);
        margin-right: 2px;
    }

    .price-num-hero {
        font-size: 32px;
        font-weight: 800;
        color: var(--re-dark-green);
        letter-spacing: -0.5px;
    }

    .price-num-card {
        font-size: 22px;
        font-weight: 800;
        color: var(--re-primary-green);
    }

    .price-num-highlight {
        font-size: 42px;
        font-weight: 900;
        color: #FFFFFF;
        letter-spacing: -1px;
    }

    .trigger-natural-badge {
        display: inline-flex;
        align-items: center;
        background-color: #EBF8F4;
        color: #065F43;
        border: 1px solid #A6E2CE;
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 6px;
    }

    .cost-summary-box {
        background: linear-gradient(135deg, #06392B 0%, #006043 100%);
        border-radius: 18px;
        padding: 32px 36px;
        color: #FFFFFF;
        box-shadow: 0 14px 30px rgba(6, 57, 43, 0.22);
    }

    .action-step-card {
        background: #FFFFFF;
        border: 1px solid var(--re-border);
        border-top: 4px solid var(--re-primary-green);
        border-radius: 12px;
        padding: 22px 20px;
        height: 100%;
        box-shadow: var(--re-card-shadow);
    }

    @media print {
        header, footer, [data-testid="stToolbar"], .no-print {
            display: none !important;
        }
        .main {
            background-color: #FFFFFF !important;
        }
        .premium-card, .addon-card-item, .action-step-card {
            box-shadow: none !important;
            border: 1px solid #DDD !important;
            break-inside: avoid;
        }
        .cost-summary-box {
            background: #F4FAF7 !important;
            color: #000 !important;
            border: 2px solid #007A55 !important;
        }
        .cost-summary-box * {
            color: #000 !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header Banner
st.markdown(
    """
    <div class="executive-header">
        <div class="brand-title-wrap">
            <div>
                <div class="brand-name">re:<span>HEALTH</span> 香港仁和體檢健康管理顧問</div>
                <div class="brand-subtitle">香港仁和體檢 ｜ AI 個人化健康評估顧問</div>
            </div>
            <div style="text-align: right; opacity: 0.85; font-size: 12px; font-weight: 500;">
                Clinical Logic Consultation Standard<br>
                香港私家醫療中心確定性評估體系
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Session State Management
if "calculated" not in st.session_state:
    st.session_state.calculated = False
if "form_data" not in st.session_state:
    st.session_state.form_data = {}


def reset_questionnaire():
    st.session_state.calculated = False
    st.session_state.form_data = {}
    st.rerun()


# Questionnaire Layout
with st.container():
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="form-card"><div class="form-card-title">步驟一：基本資料 (Basic Information)</div>', unsafe_allow_html=True)
        c_age, c_gen = st.columns(2)
        with c_age:
            age_selected = st.selectbox("受檢年齡組別 (Age)", ["18-29", "30-39", "40-49", "50+"], index=0)
        with c_gen:
            gender_selected = st.selectbox(
                "生理性別 (Gender)",
                ["Female", "Male"],
                format_func=lambda x: "女性 (Female)" if x == "Female" else "男性 (Male)",
            )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="form-card"><div class="form-card-title">步驟二：家族病史 (Family History)</div>', unsafe_allow_html=True)
        st.caption("請勾選一等親或直系血親曾確診之病況（可多選）：")
        family_history_selected = []
        fh_c1, fh_c2 = st.columns(2)
        fh_items = list(QUESTIONNAIRE_OPTIONS["family_history"].items())
        half_fh = len(fh_items) // 2 + 1
        for idx, (k, v) in enumerate(fh_items):
            target = fh_c1 if idx < half_fh else fh_c2
            if target.checkbox(v, key=f"fh_{k}"):
                family_history_selected.append(k)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="form-card"><div class="form-card-title">步驟三：自覺症狀 (Symptoms)</div>', unsafe_allow_html=True)
        st.caption("請勾選近期反覆或持續存在的不適徵候（可多選）：")
        symptoms_selected = []
        sym_c1, sym_c2 = st.columns(2)
        sym_items = list(QUESTIONNAIRE_OPTIONS["symptoms"].items())
        half_sym = len(sym_items) // 2 + 1
        for idx, (k, v) in enumerate(sym_items):
            target = sym_c1 if idx < half_sym else sym_c2
            if target.checkbox(v, key=f"sym_{k}"):
                symptoms_selected.append(k)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="form-card"><div class="form-card-title">步驟四：生活型態 (Lifestyle)</div>', unsafe_allow_html=True)
        st.caption("日常習慣評估（可多選）：")
        lifestyle_selected = []
        l_c1, l_c2 = st.columns(2)
        for idx, (k, v) in enumerate(QUESTIONNAIRE_OPTIONS["lifestyle"].items()):
            target = l_c1 if idx % 2 == 0 else l_c2
            if target.checkbox(v, key=f"life_{k}"):
                lifestyle_selected.append(k)
        st.markdown("</div>", unsafe_allow_html=True)

# Action Buttons
btn_col1, btn_col2, _ = st.columns([2.5, 1.3, 3])
with btn_col1:
    calculate_clicked = st.button("📋 生成個人化專屬健康報告", use_container_width=True, type="primary")
with btn_col2:
    st.button("🔄 重新評估 (Reset)", on_click=reset_questionnaire, use_container_width=True)

if calculate_clicked:
    st.session_state.calculated = True
    st.session_state.form_data = {
        "age": age_selected,
        "gender": gender_selected,
        "family_history": family_history_selected,
        "symptoms": symptoms_selected,
        "lifestyle": lifestyle_selected,
    }

# ==============================================================================
# REPORT PRESENTATION SECTION
# ==============================================================================

if st.session_state.calculated:
    data = st.session_state.form_data
    results = run_decision_engine(
        age=data["age"],
        gender=data["gender"],
        family_history=data["family_history"],
        symptoms=data["symptoms"],
        lifestyle=data["lifestyle"],
    )

    risk_info = determine_health_risk(data["symptoms"], data["family_history"])
    base_meta = BASE_PACKAGE_DESCRIPTIONS.get(
        results["base_package_name"],
        {
            "suitable": f"適合 {data['age']} 歲組別{'女性' if data['gender'] == 'Female' else '男性'}",
            "desc": "針對該年齡層與生理性別精心規劃之年度核心健康篩查方案。",
        },
    )

    st.markdown("<div style='margin: 40px 0 25px 0; border-bottom: 2px solid #DDEBE5;'></div>", unsafe_allow_html=True)

    # Top Utility Actions: Print, PDF, Reset
    action_left, action_right = st.columns([1.5, 2.5])
    with action_left:
        st.markdown(
            f"""
            <div style="font-size: 13.5px; color: var(--re-text-muted); padding-top: 6px;">
                受檢對象：<strong>{'女士' if data['gender'] == 'Female' else '男士'}（{data['age']} 歲）</strong> ｜ 檔案編號：<strong>RH-{abs(hash(str(data))) % 1000000:06d}</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with action_right:
        act_c1, act_c2, act_c3 = st.columns([1.2, 1.2, 1.4])
        with act_c1:
            components.html(
                """
                <button onclick="window.print()" style="
                    width: 100%;
                    height: 38px;
                    background: #007A55;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-weight: 700;
                    font-size: 13px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                ">🖨️ 列印報告</button>
                """,
                height=42,
            )
        with act_c2:
            components.html(
                """
                <button onclick="window.print()" style="
                    width: 100%;
                    height: 38px;
                    background: #FFFFFF;
                    color: #007A55;
                    border: 1.5px solid #007A55;
                    border-radius: 8px;
                    font-weight: 700;
                    font-size: 13px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                ">📥 下載 PDF</button>
                """,
                height=42,
            )
        with act_c3:
            st.button("➕ 開始全新評估", on_click=reset_questionnaire, use_container_width=True)

    # SECTION 1: Health Risk Summary
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
        <div class="premium-card" style="background-color: {risk_info['bg_color']}; border: 1.5px solid {risk_info['border_color']};">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; margin-bottom: 12px;">
                <div style="font-size: 13px; font-weight: 700; color: {risk_info['badge_color']}; letter-spacing: 1px; text-transform: uppercase;">
                    CLINICAL RISK STRATIFICATION
                </div>
                <div style="background-color: {risk_info['badge_color']}; color: #FFFFFF; font-size: 13px; font-weight: 800; padding: 6px 16px; border-radius: 20px; letter-spacing: 0.5px;">
                    {risk_info['level']} ｜ {risk_info['en_level']}
                </div>
            </div>
            <div style="font-size: 20px; font-weight: 800; color: var(--re-dark-green); margin-bottom: 10px;">
                個人化健康風險指標分級
            </div>
            <div style="font-size: 14.5px; line-height: 1.7; color: var(--re-text-main);">
                {risk_info['desc']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # SECTION 2: Recommended Base Package
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
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
                <div>
                    <div style="font-size: 12px; font-weight: 700; color: var(--re-gold); letter-spacing: 1px; margin-bottom: 4px;">RECOMMENDED FOUNDATION</div>
                    <div style="font-size: 26px; font-weight: 800; color: var(--re-dark-green); margin-bottom: 6px;">
                        {results['base_package_name']}
                    </div>
                    <div style="display: inline-block; background: #E8F5F1; color: var(--re-primary-green); font-size: 12.5px; font-weight: 700; padding: 3px 12px; border-radius: 6px; margin-bottom: 14px;">
                        🎯 {base_meta['suitable']}
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 12px; color: var(--re-text-muted); font-weight: 600;">基礎套餐價格</div>
                    <div style="display: flex; align-items: baseline; justify-content: flex-end; gap: 4px;">
                        <span class="currency-symbol">HKD</span>
                        <span class="price-num-hero">{results['base_package_price']:,}</span>
                    </div>
                </div>
            </div>
            <div style="font-size: 14px; line-height: 1.7; color: var(--re-text-muted); border-top: 1px solid #E1EBE6; padding-top: 14px; margin-top: 6px;">
                {base_meta['desc']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # SECTION 3: Recommended Add-On Packages
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
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px; margin-bottom: 12px;">
                        <div>
                            <div style="font-size: 18px; font-weight: 800; color: var(--re-dark-green); margin-bottom: 4px;">
                                {addon['name']}
                            </div>
                            <div style="font-size: 12px; color: var(--re-text-muted);">
                                專項早期深度預防檢測
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <span class="currency-symbol">HKD</span>
                            <span class="price-num-card">{addon['price']:,}</span>
                        </div>
                    </div>
                    <div style="margin-bottom: 12px;">
                        <div style="font-size: 12px; font-weight: 700; color: var(--re-text-muted); margin-bottom: 6px;">
                            吻合臨床評估指標：
                        </div>
                        <div>
                            {trigger_badges_html}
                        </div>
                    </div>
                    <div style="background: #F6FAF8; border-radius: 8px; padding: 12px 16px; border-left: 3px solid var(--re-primary-green); font-size: 13.5px; color: var(--re-text-main); line-height: 1.6;">
                        <strong>推薦理由：</strong>{addon['reasons'][0]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            """
            <div class="premium-card" style="text-align: center; padding: 36px 20px;">
                <div style="font-size: 26px; margin-bottom: 8px;">🛡️</div>
                <div style="font-size: 17px; font-weight: 800; color: var(--re-dark-green); margin-bottom: 6px;">當前無額外專項加配項目</div>
                <div style="font-size: 13.5px; color: var(--re-text-muted); max-width: 580px; margin: 0 auto; line-height: 1.6;">
                    根據您目前所填報之生理數據、自覺症狀與家族背景，推薦之核心基礎套餐已能全面覆蓋當前健康監測所需，毋須額外增加非必要之篩查項目。
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # SECTION 4: Estimated Cost
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
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 24px;">
                <div style="flex: 1; min-width: 260px;">
                    <div style="font-size: 12.5px; font-weight: 700; color: #64E7B8; letter-spacing: 1px; text-transform: uppercase;">
                        TOTAL ESTIMATED INVESTMENT
                    </div>
                    <div style="font-size: 22px; font-weight: 800; margin-top: 4px; margin-bottom: 12px;">
                        體檢方案費用總覽
                    </div>
                    <div style="font-size: 14px; opacity: 0.9; line-height: 1.8;">
                        • 核心基礎套餐費用：<strong>HKD {results['base_package_price']:,}</strong><br>
                        • 專項加配項目費用（共 {len(results['addons'])} 項）：<strong>HKD {addon_total_price:,}</strong>
                    </div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.08); border: 1.5px solid rgba(255, 255, 255, 0.18); border-radius: 14px; padding: 20px 32px; text-align: right; min-width: 240px;">
                    <div style="font-size: 12.5px; font-weight: 600; color: rgba(255, 255, 255, 0.85); letter-spacing: 0.5px;">
                        預估總費用 (TOTAL COST)
                    </div>
                    <div style="display: flex; align-items: baseline; justify-content: flex-end; gap: 6px; margin-top: 4px;">
                        <span style="font-size: 20px; font-weight: 700; color: #64E7B8;">HKD</span>
                        <span class="price-num-highlight">{results['total_cost']:,}</span>
                    </div>
                    <div style="font-size: 11.5px; color: rgba(255, 255, 255, 0.7); margin-top: 4px;">
                        包含專科醫療團隊一對一報告解讀諮詢
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # SECTION 5: Why We Recommend These Packages
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
                <div class="premium-card" style="border-left: 5px solid var(--re-primary-green); padding: 22px 26px; margin-bottom: 16px;">
                    <div style="font-size: 17px; font-weight: 800; color: var(--re-dark-green); margin-bottom: 8px;">
                        針對項目：{addon['name']}
                    </div>
                    <div style="font-size: 14px; color: var(--re-text-main); margin-bottom: 8px; line-height: 1.6;">
                        <strong>因為您在評估中提到：</strong>
                        <span style="color: var(--re-primary-green); font-weight: 600;">{triggers_str}</span>
                    </div>
                    <div style="font-size: 13.5px; color: var(--re-text-muted); line-height: 1.7;">
                        <strong>醫療團隊臨床分析：</strong>{addon['reasons'][0]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            f"""
            <div class="premium-card" style="border-left: 5px solid var(--re-primary-green); padding: 22px 26px;">
                <div style="font-size: 17px; font-weight: 800; color: var(--re-dark-green); margin-bottom: 8px;">
                    針對方案：{results['base_package_name']}
                </div>
                <div style="font-size: 14px; color: var(--re-text-main); margin-bottom: 8px;">
                    <strong>臨床邏輯分析：</strong>
                    您目前並未出現消化系統不適、心血管警訊或顯著癌症家族聚集病史。
                </div>
                <div style="font-size: 13.5px; color: var(--re-text-muted); line-height: 1.7;">
                    根據預防醫學常規指引，當前階段毋須進行過度的侵入性或高階基因測試。集中進行 <strong>{results['base_package_name']}</strong> 所包含的血液代謝功能、重要器官影像與基本生理監控，即可提供最理想且合乎成本效益的健康防護。
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # SECTION 6: Suggested Next Step
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
        <div class="premium-card" style="background-color: #F4FAF7; border: 1.5px solid #C1E4D6; margin-bottom: 24px;">
            <div style="font-size: 16px; font-weight: 700; color: var(--re-dark-green); margin-bottom: 6px;">
                💡 專業醫療顧問提示
            </div>
            <div style="font-size: 14.5px; line-height: 1.7; color: var(--re-text-main);">
                根據您的問卷評估結果，我們建議您攜帶此報告選項與註冊西醫或醫療專業顧問進一步討論最合適的檢查細節。<br>
                <span style="font-size: 13px; color: var(--re-text-muted);">
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
                <div style="font-size: 12px; font-weight: 700; color: var(--re-primary-green); margin-bottom: 4px;">STEP 01</div>
                <div style="font-size: 16px; font-weight: 800; color: var(--re-dark-green); margin-bottom: 8px;">預約私家醫療諮詢</div>
                <div style="font-size: 13px; color: var(--re-text-muted); line-height: 1.6;">
                    攜帶本建議書前往 re:HEALTH 醫療中心或您的家庭醫生診所，確認加配篩查項目的臨床合適性並確定檔期。
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with action_c2:
        st.markdown(
            """
            <div class="action-step-card">
                <div style="font-size: 12px; font-weight: 700; color: var(--re-primary-green); margin-bottom: 4px;">STEP 02</div>
                <div style="font-size: 16px; font-weight: 800; color: var(--re-dark-green); margin-bottom: 8px;">檢前生活準備</div>
                <div style="font-size: 13px; color: var(--re-text-muted); line-height: 1.6;">
                    體檢前 8 小時請保持空腹（可少量飲水）。若包含無創基因或便潛血檢查，醫療顧問將預先提供專用無菌採樣包。
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with action_c3:
        st.markdown(
            """
            <div class="action-step-card">
                <div style="font-size: 12px; font-weight: 700; color: var(--re-primary-green); margin-bottom: 4px;">STEP 03</div>
                <div style="font-size: 16px; font-weight: 800; color: var(--re-dark-green); margin-bottom: 8px;">註冊醫生專屬解讀</div>
                <div style="font-size: 13px; color: var(--re-text-muted); line-height: 1.6;">
                    檢查完成後，由香港註冊西醫為您逐項分析健康數據，並度身訂造後續的預防醫學跟進與生活飲食指導。
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Patient Notice & Legal Disclaimer
    st.markdown(
        """
        <div style="margin-top: 36px; padding: 22px 24px; background: #EEF4F1; border-radius: 12px; font-size: 12.5px; color: #536B63; line-height: 1.7;">
            <strong>重要聲明 (Important Notice)：</strong><br>
            本報告僅供預防性個人健康管理與初步篩查參考，非正式臨床診斷依據 (This report is intended for preventive health management only)。報告中所有推薦項目均透過專家臨床確定性邏輯規則樹生成，絕無使用黑箱 AI 自行揣測。若您目前正出現急性劇烈疼痛、大量便血或其他緊急不適，請立即前往就近醫院急症室或尋求急症醫療協助。
        </div>
        """,
        unsafe_allow_html=True,
    )
