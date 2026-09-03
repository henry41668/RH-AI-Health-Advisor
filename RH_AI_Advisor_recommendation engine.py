# ==============================================================================
# DETERMINISTIC DECISION ENGINE & CLINICAL RISK STRATIFICATION
# ==============================================================================

from constants import (
    ADDON_PRICES,
    BASE_PACKAGES,
    CANCER_FAMILY_TAGS,
)


def run_decision_engine(age: str, gender: str, family_history: list, symptoms: list, lifestyle: list):
    """
    Executes hardcoded business rules strictly based on clinical decision trees.
    No LLM decision making. No external API calls.
    """
    base_info = BASE_PACKAGES[gender][age]
    base_package_name = base_info["name"]
    base_package_price = base_info["price"]

    recommended_addons = {}

    def add_recommendation(addon_name: str, reason_text: str, trigger_keys: list):
        if addon_name not in recommended_addons:
            recommended_addons[addon_name] = {
                "name": addon_name,
                "price": ADDON_PRICES[addon_name],
                "reasons": [reason_text],
                "triggers": set(trigger_keys),
            }
        else:
            recommended_addons[addon_name]["reasons"].append(reason_text)
            recommended_addons[addon_name]["triggers"].update(trigger_keys)

    block_genetic_colon = False
    block_genetic_npc = False
    prostate_triggered = False

    # 1. COLON LOGIC
    colon_symptoms = [s for s in ["blood_stool", "black_stool", "abdominal_pain"] if s in symptoms]
    if colon_symptoms:
        add_recommendation(
            "G-NiiB M3CRC 大腸癌風險檢測",
            "檢測到腸道警訊症狀，建議優先進行腸道菌群與大腸癌微腺瘤標記篩查。",
            colon_symptoms,
        )
        if "colon_cancer" in family_history:
            add_recommendation(
                "癌症及全腹超聲波Plus至尊健康檢查",
                "具大腸癌家族病史且伴隨消化道臨床症狀，建議進一步加強腹部器官結構排查。",
                colon_symptoms + ["colon_cancer"],
            )
        block_genetic_colon = True

    # 2. NPC LOGIC
    npc_matched = []
    if "npc" in family_history:
        npc_matched.append("npc")
    if "chronic_cough" in symptoms:
        npc_matched.append("chronic_cough")
    if "smoking" in lifestyle:
        npc_matched.append("smoking")

    if npc_matched:
        add_recommendation(
            "早期鼻咽癌篩查計劃",
            "存在鼻咽癌高危風險因素（家族史/呼吸道症狀/吸煙習慣），建議加配高敏血清DNA篩查。",
            npc_matched,
        )
        block_genetic_npc = True

    # 3. PROSTATE LOGIC
    prostate_matched = []
    if "prostate_symptom" in symptoms:
        prostate_matched.append("prostate_symptom")
    if "prostate_cancer" in family_history:
        prostate_matched.append("prostate_cancer")

    if prostate_matched:
        prostate_triggered = True
        add_recommendation(
            "男士前列腺全面檢查套餐",
            "具備前列腺臨床症狀或前列腺癌家族傾向，建議專項評估前列腺及泌尿機能。",
            prostate_matched,
        )

    # 4. STROKE LOGIC
    stroke_matched = []
    for tag in ["stroke", "cardiovascular"]:
        if tag in family_history:
            stroke_matched.append(tag)
    for tag in ["palpitation", "shortness_of_breath"]:
        if tag in symptoms:
            stroke_matched.append(tag)

    if stroke_matched:
        add_recommendation(
            "防中風全面磁力共振健康檢查",
            "存在心腦血管家族史或出現心悸、氣促徵候，建議進行腦血管磁力共振深度排查。",
            stroke_matched,
        )

    # 5. THYROID LOGIC
    if "thyroid" in family_history:
        add_recommendation(
            "甲狀腺升級全面檢測套餐",
            "具甲狀腺家族病史，建議專項檢測甲狀腺機能及超聲波結構。",
            ["thyroid"],
        )

    # 6. GENETIC LOGIC
    cancer_family_matches = [f for f in family_history if f in CANCER_FAMILY_TAGS]
    cancer_count = len(cancer_family_matches)

    genetic_blocked = False
    if block_genetic_colon:
        genetic_blocked = True
    if block_genetic_npc:
        genetic_blocked = True
    if prostate_triggered and cancer_count < 2:
        genetic_blocked = True

    if not genetic_blocked:
        has_red_flags = ("weight_loss" in symptoms) or ("shortness_of_breath" in symptoms)
        if cancer_count >= 3 or (cancer_count == 2 and has_red_flags):
            matched_genetic_triggers = list(cancer_family_matches)
            if "weight_loss" in symptoms:
                matched_genetic_triggers.append("weight_loss")
            if "shortness_of_breath" in symptoms:
                matched_genetic_triggers.append("shortness_of_breath")

            add_recommendation(
                "全方位早期癌症風險評估",
                "具多項癌症家族聚集傾向，或家族史合併消瘦/氣促預警症狀，建議進行最高規格多癌種液態活檢排查。",
                matched_genetic_triggers,
            )
        elif len(symptoms) == 0 and cancer_count >= 1:
            add_recommendation(
                "遺傳性癌症基因全面測試組合",
                "目前無自覺不適症狀但具明確癌症家族史，建議透過基因檢測釐清先天致病突變風險。",
                cancer_family_matches,
            )

    # 7. HEALTHY USER LOGIC
    if len(family_history) == 0 and len(symptoms) == 0:
        if age in ["18-29", "30-39"]:
            add_recommendation(
                "腫瘤標記COMBO檢查套餐",
                "無特定家族史與症狀且年齡未達40歲，建議加配腫瘤標記COMBO作為基礎防癌防護。",
                ["age_below_40_healthy"],
            )
        else:
            add_recommendation(
                "透徹五高心血管檢查計劃",
                "無特殊家族史與症狀且年齡滿40歲或以上，建議加強高血壓、高血糖、高血脂等慢性心血管指標監控。",
                ["age_40_plus_healthy"],
            )

    # POST-FILTER RESTRICTION
    if base_package_name == "男士50+計劃":
        if "透徹五高心血管檢查計劃" in recommended_addons:
            del recommended_addons["透徹五高心血管檢查計劃"]

    addons_list = list(recommended_addons.values())
    total_addon_cost = sum(item["price"] for item in addons_list)
    grand_total = base_package_price + total_addon_cost

    return {
        "base_package_name": base_package_name,
        "base_package_price": base_package_price,
        "addons": addons_list,
        "total_cost": grand_total,
    }


def determine_health_risk(symptoms: list, family_history: list):
    """
    Evaluates health risk tier strictly based on business rules:
    HIGH:
      2 or more symptoms exist
      OR
      1 symptom + cancer family history
    MEDIUM:
      1 symptom
      OR
      1 family history
    LOW:
      otherwise
    """
    sym_count = len(symptoms)
    has_cancer_history = any(f in CANCER_FAMILY_TAGS for f in family_history)
    has_any_family_history = len(family_history) > 0

    if sym_count >= 2 or (sym_count >= 1 and has_cancer_history):
        return {
            "level": "高風險關注",
            "en_level": "High Risk",
            "badge_color": "#C0392B",
            "bg_color": "#FDEDEC",
            "border_color": "#F5B7B1",
            "desc": "評估顯示您申報了 2 項或以上自覺身體症狀，或同時出現不適症狀伴隨家族癌症病史。此情況強烈建議您儘早預約專業註冊醫生作針對性檢查，及早排除嚴重隱疾。",
        }
    elif sym_count == 1 or has_any_family_history:
        return {
            "level": "中度風險留意",
            "en_level": "Medium Risk",
            "badge_color": "#D35400",
            "bg_color": "#FEF5E7",
            "border_color": "#FAD7A0",
            "desc": "評估顯示您目前有單一自覺症狀或具備直系親屬慢性疾病病史。建議在常規年度檢查基礎上，針對性配置器官影像或早期篩查項目，做好防範與追蹤。",
        }
    else:
        return {
            "level": "常態健康低風險",
            "en_level": "Low Risk",
            "badge_color": "#007A55",
            "bg_color": "#E8F5F1",
            "border_color": "#A3E4D7",
            "desc": "您目前無申報顯著不適症狀或直系家族病史，整體健康狀況平穩。建議定期進行年度基礎身體檢查，維持良好運動及生活習慣，持續保持健康基線。",
        }