import os
from datetime import datetime
from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np

try:
    import joblib
except Exception:
    joblib = None

try:
    from catboost import CatBoostClassifier
except Exception:
    CatBoostClassifier = None

import shutil

# Default model path provided by user (original downloaded location)
DEFAULT_MODEL_PATH = r"C:\Users\LENOVO\Downloads\Fraud_catboost_classifier.joblib"
# Copy destination inside the repo so app loads from repo-local file
MODEL_COPY_DIR = Path(__file__).parent / "models"
MODEL_COPY_DIR.mkdir(parents=True, exist_ok=True)
MODEL_COPY_PATH = MODEL_COPY_DIR / "model.joblib"

EXPECTED_FEATURES = [
    "Date",
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "City",
    "type",
    "Card Type",
    "Exp Type",
    "Gender",
]


def load_model_from_file(path: str):
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Model file not found: {path}")
    ext = p.suffix.lower()
    if ext in (".pkl", ".joblib"):
        if joblib is None:
            raise RuntimeError("joblib is not available")
        return joblib.load(str(p))
    if ext in (".cbm", ".bin"):
        if CatBoostClassifier is None:
            raise RuntimeError("catboost is not installed")
        m = CatBoostClassifier()
        m.load_model(str(p))
        return m
    # fallback to pickle
    import pickle

    with open(p, "rb") as f:
        return pickle.load(f)


@st.cache_resource
def cached_load(path: str):
    return load_model_from_file(path)


def extract_categories_from_model(model) -> dict:
    """Attempt to extract categorical value lists for features from scikit pipelines or encoders.
    Returns a dict {feature_name: [categories]}."""
    cats = {}
    try:
        # ColumnTransformer inside Pipeline
        if hasattr(model, "named_steps"):
            for name, step in model.named_steps.items():
                # look for ColumnTransformer
                if hasattr(step, "transformers_"):
                    ct = step
                    try:
                        for tr_name, transformer, cols in ct.transformers_:
                            enc = transformer
                            if hasattr(transformer, "named_steps"):
                                # pipeline
                                enc = list(transformer.named_steps.values())[-1]
                            if hasattr(enc, "categories_"):
                                for col, c in zip(cols, enc.categories_):
                                    cats[col] = list(map(str, c))
                    except Exception:
                        continue
        # direct ColumnTransformer
        if hasattr(model, "transformers_"):
            for tr_name, transformer, cols in model.transformers_:
                enc = transformer
                if hasattr(transformer, "named_steps"):
                    enc = list(transformer.named_steps.values())[-1]
                if hasattr(enc, "categories_"):
                    for col, c in zip(cols, enc.categories_):
                        cats[col] = list(map(str, c))
        # simple classifiers with fitted label encoders stored as attributes
        for attr in dir(model):
            if attr.endswith("_classes") or attr.endswith("_classes_"):
                try:
                    vals = getattr(model, attr)
                    # try to derive feature name
                    fname = attr.replace("_classes_", "").replace("_classes", "")
                    cats[fname] = list(map(str, vals))
                except Exception:
                    pass
    except Exception:
        pass
    return cats


def build_input_dataframe(values: dict) -> pd.DataFrame:
    # Build DataFrame in expected order; unknown keys will be added as empty
    row = {k: values.get(k, None) for k in EXPECTED_FEATURES}

    # numeric conversions
    for num in ("amount", "oldbalanceOrg", "newbalanceOrig"):
        v = row.get(num)
        try:
            row[num] = float(v) if v not in (None, "") else 0.0
        except Exception:
            row[num] = 0.0

    # Date: convert to datetime and numeric timestamp + Day/Month/Year
    d = row.get("Date")
    if isinstance(d, (str,)):
        try:
            d = pd.to_datetime(d, errors="coerce")
        except Exception:
            d = None
    elif isinstance(d, datetime):
        d = pd.to_datetime(d)

    if pd.isna(d) or d is None:
        # default zeros
        row["Date_ts"] = 0
        row["Day"] = 0
        row["Month"] = 0
        row["Year"] = 0
    else:
        row["Date_ts"] = int(d.value // 10**9)
        row["Day"] = int(d.day)
        row["Month"] = int(d.month)
        row["Year"] = int(d.year)

    # Ensure categorical fields are strings (CatBoost accepts strings)
    for c in ("City", "type", "Card Type", "Exp Type", "Gender"):
        v = row.get(c)
        row[c] = str(v) if v is not None else ""

    # Return DataFrame
    df = pd.DataFrame([row])
    return df


def preprocess_before_predict(df: pd.DataFrame, model) -> pd.DataFrame:
    # Align columns expected by model if possible
    out = df.copy()
    # if model has feature_names_in_, align to that
    target_cols = None
    if hasattr(model, "feature_names_in_"):
        target_cols = list(model.feature_names_in_)
    # CatBoost models may not have feature_names_in_, so we avoid strict alignment
    if target_cols:
        for c in target_cols:
            if c not in out.columns:
                out[c] = 0
        out = out[target_cols]
    return out


def main():
    st.set_page_config(page_title="Bank Transaction Fraud Predictor", layout="centered")
    st.title("Bank Transaction Fraud Detection — Predict (fixed)")

    # Use notebook-trained model by default; disallow uploads
    st.sidebar.markdown("### Model (fixed)")
    st.sidebar.write("Using the notebook-trained model and its parameters. Uploads and training are disabled in this app.")
    model_path_input = DEFAULT_MODEL_PATH

    model = None
    load_path = None
    # If a repo-local copy doesn't exist but the original download exists, copy it into repo
    try:
        orig = Path(model_path_input)
        if not MODEL_COPY_PATH.exists() and orig.exists():
            try:
                shutil.copy(str(orig), str(MODEL_COPY_PATH))
                st.sidebar.info(f"Copied model into app folder: {MODEL_COPY_PATH}")
            except Exception as e:
                st.sidebar.warning(f"Could not copy model into app folder: {e}")

        # Prefer loading from the repo-local copy if present
        load_path = str(MODEL_COPY_PATH) if MODEL_COPY_PATH.exists() else str(orig)
        model = cached_load(load_path)
        # Show confirmation with filename and last-modified timestamp
        try:
            p = Path(load_path)
            mtime = datetime.fromtimestamp(p.stat().st_mtime).isoformat()
            st.sidebar.success(f"Loaded model: {p.name} (modified: {mtime})")
        except Exception:
            st.sidebar.success(f"Model loaded from: {load_path}")
    except Exception as e:
        st.sidebar.error(f"Failed to load default model at {model_path_input}: {e}")

    # Show extracted categories if possible
    if model is not None:
        cats = extract_categories_from_model(model)
        if cats:
            st.sidebar.subheader("Discovered categories from model encoders")
            for feat in ("Card Type", "Exp Type", "type"):
                if feat in cats:
                    st.sidebar.markdown(f"**{feat}**: {cats[feat]}")
        else:
            st.sidebar.info("No encoder categories discovered from model. If you have training data, upload it below to show categories.")

    st.subheader("Transaction input")
    with st.form("input_form"):
        date_val = st.date_input("Date")
        amount = st.number_input("Amount", min_value=0.0, value=0.0, format="%.2f")
        oldbalanceOrg = st.number_input("Old Balance Origin", min_value=0.0, value=0.0, format="%.2f")
        newbalanceOrig = st.number_input("New Balance Origin", min_value=0.0, value=0.0, format="%.2f")
        City = st.text_input("City")
        ttype = st.text_input("Type (e.g., PAYMENT, TRANSFER)")
        card_type = st.text_input("Card Type")
        exp_type = st.text_input("Exp Type")
        gender = st.text_input("Gender")
        submitted = st.form_submit_button("Predict")

    if submitted:
        if model is None:
            st.error("Please upload or provide a valid model before predicting.")
            st.stop()

        vals = {
            "Date": date_val,
            "amount": amount,
            "oldbalanceOrg": oldbalanceOrg,
            "newbalanceOrig": newbalanceOrig,
            "City": City,
            "type": ttype,
            "Card Type": card_type,
            "Exp Type": exp_type,
            "Gender": gender,
        }
        X = build_input_dataframe(vals)
        X_proc = preprocess_before_predict(X, model)
        try:
            # predict
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(X_proc)
                prob = float(proba[0][1]) if proba is not None else None
                pred = int((prob >= 0.5)) if prob is not None else int(model.predict(X_proc)[0])
            else:
                pred = int(model.predict(X_proc)[0])
                prob = None
        except Exception as e:
            st.error(f"Prediction failed: {e}")
            st.stop()

        st.write("**Prediction**")
        if prob is None:
            st.info(f"Predicted class: {pred}")
        else:
            st.info(f"Predicted class: {pred} — probability fraud: {prob:.3f}")

    # Uploads of training/data are disabled in this deployment.


if __name__ == "__main__":
    main()
