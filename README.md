# re:HEALTH AI Health Advisor

re:HEALTH AI Health Advisor is a deterministic, rule-based health assessment web application built with Streamlit. It guides users through an intake questionnaire (evaluating baseline demographic factors, family medical history, current clinical symptoms, and lifestyle indicators) and matches them with tailored private health screening packages and targeted add-ons using clinical decision rules.

---

## Project Architecture

The application is structured into modular layers separating state/presentation, configuration data, and deterministic decision logic:

```text
rehealth-ai-advisor/
│
├── RH_AI_Advisor_app.py                    # Presentation & UI Layer (Streamlit)
├── RH_AI_Advisor_recommendation_engine.py  # Business logic & Decision Tree Engine
├── RH_AI_Advisor_constants.py              # Pricing catalog, mappings & package metadata
├── requirements.txt                        # Application dependencies
├── .gitignore                              # Git exclusion rules
└── README.md                               # Project documentation
