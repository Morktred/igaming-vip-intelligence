# ♠ VIP Intelligence

Predictive analytics platform for iGaming VIP lifecycle management, powered by machine learning and Streamlit.

**Deployment by:** Daniel Holguin

## Overview

VIP Intelligence is a machine learning solution designed to analyze transitions within the iGaming VIP lifecycle through two predictive models.

## Predictive Models

| Model | Algorithm | ROC-AUC |
|---|---|---:|
| VIP Churn | Soft Voting Classifier | 0.741 |
| VIP Reactivation | Logistic Regression | 0.675 |

## Features

- Interactive predictive dashboard.
- Individual model scoring.
- Model performance indicators.
- Casino-inspired visual interface.
- Integrated data preprocessing.
- Synthetic profiles for demonstration.

## Technology Stack

Python · Streamlit · Scikit-learn · Pandas · NumPy · Machine Learning

## Deployment

Install dependencies:

`pip install -r requirements.txt`

Run the application:

`streamlit run app.py`

## Privacy and Responsible Use

This repository does not include training datasets or individual customer records. Demonstration profiles are synthetic.

Model scores are experimental estimates, not calibrated probabilities. Further validation, including temporal feature availability, is required before production use.

---

**VIP Intelligence | iGaming & Data Science**
