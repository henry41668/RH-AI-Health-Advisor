# ==============================================================================
# PRICING TABLES, METADATA & NATURAL LANGUAGE LABELS
# ==============================================================================

BASE_PACKAGES = {
    "Female": {
        "18-29": {"name": "婦女精選健康檢查套餐", "price": 2563},
        "30-39": {"name": "女士30+計劃", "price": 7420},
        "40-49": {"name": "女士40+計劃", "price": 9290},
        "50+": {"name": "女士50+計劃", "price": 17180},
    },
    "Male": {
        "18-29": {"name": "男士精選健康檢查套餐", "price": 1848},
        "30-39": {"name": "男士30+計劃", "price": 4150},
        "40-49": {"name": "男士40+計劃", "price": 7650},
        "50+": {"name": "男士50+計劃", "price": 16590},
    },
}

ADDON_PRICES = {
    "G-NiiB M3CRC 大腸癌風險檢測": 4290,
    "早期鼻咽癌篩查計劃": 2420,
    "男士前列腺全面檢查套餐": 2695,
    "甲狀腺升級全面檢測套餐": 2880,
    "透徹五高心血管檢查計劃": 980,
    "防中風全面磁力共振健康檢查": 10400,
    "全身綜合磁力共振健康檢查": 11250,
    "婚前健康檢查二人同行套餐": 9510,
    "遺傳性癌症基因全面測試組合": 20900,
    "全方位早期癌症風險評估": 66000,
    "腫瘤標記COMBO檢查套餐": 680,
    "癌症及全腹超聲波Plus至尊健康檢查": 6300,
    "專科尊尚全面健康檢查": 2880,
}

CANCER_FAMILY_TAGS = {
    "breast_cancer",
    "ovarian_cancer",
    "colon_cancer",
    "gastric_cancer",
    "lung_cancer",
    "prostate_cancer",
}

HUMAN_TRIGGER_MAP = {
    # Family History
    "colon_cancer": "家族有大腸癌病史",
    "gastric_cancer": "家族有胃癌病史",
    "lung_cancer": "家族有肺癌病史",
    "breast_cancer": "家族有乳癌病史",
    "ovarian_cancer": "家族有卵巢癌病史",
    "prostate_cancer": "家族有前列腺癌病史",
    "stroke": "家族有中風病史",
    "cardiovascular": "家族有心血管疾病史",
    "diabetes": "家族有糖尿病史",
    "npc": "家族有鼻咽癌病史",
    "thyroid": "家族有甲狀腺疾病史",
    # Symptoms
    "blood_stool": "最近出現便血",
    "black_stool": "最近出現黑便",
    "abdominal_pain": "最近出現腹痛",
    "weight_loss": "非刻意體重明顯減輕",
    "shortness_of_breath": "出現氣促或呼吸不暢",
    "palpitation": "出現心悸或心跳律動不適",
    "chronic_cough": "出現持續性慢性咳嗽",
    "prostate_symptom": "出現排尿相關不適",
    "fatigue": "長期容易疲倦乏力",
    # Lifestyle
    "smoking": "有長期吸煙習慣",
    "drinking": "有恆常飲酒習慣",
    "high_stress": "生活長期處於高壓狀態",
    "sedentary": "缺乏運動且長期久坐",
    # Prevention Tags
    "age_below_40_healthy": "40歲以下常規健康預防",
    "age_40_plus_healthy": "40歲或以上中年心血管保健",
}

BASE_PACKAGE_DESCRIPTIONS = {
    "婦女精選健康檢查套餐": {
        "suitable": "適合 18 至 29 歲年輕女性",
        "desc": "著重基礎常規生化指標、全血細胞計數、肝腎功能、基本胸部及尿液常規檢驗，為初入職場或年輕階段建立全面的健康基礎檔案。",
    },
    "女士30+計劃": {
        "suitable": "適合 30 至 39 歲輕熟齡女性",
        "desc": "針對新陳代謝變化、女性荷爾蒙波動及常見隱疾，加強甲狀腺、婦科腹部超聲波、血脂譜及子宮頸抹片篩查，提早預防慢性疾病。",
    },
    "女士40+計劃": {
        "suitable": "適合 40 至 49 歲成熟女性",
        "desc": "進入圍絕經期前後的重要全面排查，重點涵蓋骨質密度、乳房及骨盆腔超聲波、心血管風險指數及早期腫瘤標記，給予全方位關顧。",
    },
    "女士50+計劃": {
        "suitable": "適合 50 歲或以上黃金年齡女性",
        "desc": "尊尚旗艦體檢方案，深度排查更年期後心腦血管動脈硬化、骨質疏鬆、重要器官超聲波造影及多項高敏防癌篩檢，守護長遠身心健康。",
    },
    "男士精選健康檢查套餐": {
        "suitable": "適合 18 至 29 歲年輕男性",
        "desc": "為年輕男性設計的基本健康基線檢查，囊括血常規、肝膽腎臟代謝、尿酸水平及胸腔 X 光，及早掌握個人生理指標狀況。",
    },
    "男士30+計劃": {
        "suitable": "適合 30 至 39 歲事業衝刺期男性",
        "desc": "針對長期外食、工作壓力與應酬作息，深入監測血壓、膽固醇全套、脂肪肝超聲波與早期痛風風險，穩固健康根基。",
    },
    "男士40+計劃": {
        "suitable": "適合 40 至 49 歲中年男性",
        "desc": "專注於心血管動脈健康與內臟脂肪負擔，增設心電圖、腹部全器官超聲波及前列腺特異抗原（PSA）篩查，預防潛在慢性病變。",
    },
    "男士50+計劃": {
        "suitable": "適合 50 歲或以上成熟男士",
        "desc": "最高級別男士專項方案，全盤涵蓋冠狀動脈硬化評估、全腹器官超聲波、泌尿系統機能及全面腫瘤風險指標，提供深度健康保障。",
    },
}

QUESTIONNAIRE_OPTIONS = {
    "family_history": {
        "colon_cancer": "大腸癌 (Colon Cancer)",
        "gastric_cancer": "胃癌 (Gastric Cancer)",
        "lung_cancer": "肺癌 (Lung Cancer)",
        "breast_cancer": "乳癌 (Breast Cancer)",
        "ovarian_cancer": "卵巢癌 (Ovarian Cancer)",
        "prostate_cancer": "前列腺癌 (Prostate Cancer)",
        "stroke": "中風 (Stroke)",
        "cardiovascular": "心血管疾病 (Cardiovascular)",
        "diabetes": "糖尿病 (Diabetes)",
        "npc": "鼻咽癌 (NPC)",
        "thyroid": "甲狀腺疾病/腫瘤 (Thyroid)",
    },
    "symptoms": {
        "blood_stool": "便血（鮮紅血便）",
        "black_stool": "黑便（柏油樣深黑便）",
        "abdominal_pain": "持續或反覆腹痛",
        "weight_loss": "體重非刻意明顯減輕",
        "shortness_of_breath": "活動後氣促 / 呼吸不暢",
        "palpitation": "心悸 / 心跳律動異常",
        "chronic_cough": "長期慢性咳嗽 (>3週)",
        "prostate_symptom": "尿頻 / 夜尿 / 排尿微弱",
        "fatigue": "容易疲倦 / 長期倦怠",
    },
    "lifestyle": {
        "smoking": "長期吸煙習慣",
        "drinking": "習慣性飲酒",
        "high_stress": "生活長期高壓",
        "sedentary": "久坐缺乏常規運動",
    },
}
