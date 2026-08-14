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
    "Day",
    "Month",
    "Year",
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

    # Day/Month/Year: use integers provided by the UI (model trained on separate fields)
    for col in ("Day", "Month", "Year"):
        v = row.get(col)
        try:
            row[col] = int(v) if v not in (None, "") else 0
        except Exception:
            # coerce strings to numeric where possible
            try:
                row[col] = int(pd.to_numeric(v, errors="coerce") or 0)
            except Exception:
                row[col] = 0

    # keep Date_ts and Date as fallback numeric zeros (not used by model trained on Day/Month/Year)
    row["Date_ts"] = 0.0
    row["Date"] = 0.0

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

    # Ensure expected numeric types for common numeric/date-derived fields
    for col in ("amount", "oldbalanceOrg", "newbalanceOrig"):
        if col in out.columns:
            try:
                out[col] = out[col].astype(float)
            except Exception:
                out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0.0)

    # Ensure Day/Month/Year are integers (model trained on separate fields)
    for col in ("Day", "Month", "Year"):
        if col in out.columns:
            try:
                out[col] = out[col].astype(int)
            except Exception:
                out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0).astype(int)

    # If model exposes feature_names_in_, strictly align to that ordering and fill missing
    if hasattr(model, "feature_names_in_"):
        target_cols = list(model.feature_names_in_)
        for c in target_cols:
            if c not in out.columns:
                # fill numeric-looking names with 0, otherwise empty string
                if c.lower() in ("amount", "oldbalanceorg", "newbalanceorig", "date", "date_ts", "day", "month", "year"):
                    out[c] = 0
                else:
                    out[c] = ""
        # cast Day/Month/Year again in case they were created above
        for col in ("Day", "Month", "Year"):
            if col in out.columns:
                out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0).astype(int)
        # Return columns in the exact order expected by the model
        return out[target_cols]

    # If no feature metadata, return dataframe with available columns
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
        today = datetime.now()
        Day = st.number_input("Day", min_value=0, max_value=31, value=today.day, step=1)
        Month = st.number_input("Month", min_value=0, max_value=12, value=today.month, step=1)
        Year = st.number_input("Year", min_value=0, max_value=9999, value=today.year, step=1)
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
            "Day": Day,
            "Month": Month,
            "Year": Year,
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
