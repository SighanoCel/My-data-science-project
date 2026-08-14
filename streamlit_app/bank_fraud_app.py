import os
from datetime import datetime

import pandas as pd
import streamlit as st

try:
    import joblib
except Exception:
    joblib = None

try:
    from catboost import CatBoostClassifier
except Exception:
    CatBoostClassifier = None


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


def load_model_from_file(path):
    if path is None:
        return None
    _, ext = os.path.splitext(path)
    ext = ext.lower()
    if ext in (".pkl", ".joblib"):
        if joblib is None:
            raise RuntimeError("joblib is not available in this environment")
        return joblib.load(path)
    if ext in (".cbm", ".bin"):
        if CatBoostClassifier is None:
            raise RuntimeError("catboost is not installed in this environment")
        model = CatBoostClassifier()
        model.load_model(path)
        return model
    # try pickle fallback
    try:
        import pickle

        with open(path, "rb") as f:
            return pickle.load(f)
    except Exception:
        raise RuntimeError(f"Unsupported model format: {ext}")


def predict(model, X: pd.DataFrame):
    # Try sklearn-like predict_proba
    try:
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(X)
            # assume binary, take class 1 probability
            prob = float(proba[0][1])
            pred = int((prob >= 0.5))
            return pred, prob
    except Exception:
        pass

    # CatBoostClassifier object path: try model.predict_proba
    try:
        if hasattr(model, "predict") and hasattr(model, "predict_proba"):
            proba = model.predict_proba(X)
            prob = float(proba[0][1])
            pred = int((prob >= 0.5))
            return pred, prob
    except Exception:
        pass

    # fallback to predict
    try:
        pred = model.predict(X)
        pred = int(pred[0])
        return pred, None
    except Exception as e:
        raise RuntimeError(f"Model prediction failed: {e}")


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
    # Date: convert to ISO string
    d = row.get("Date")
    if isinstance(d, datetime):
        row["Date"] = d.isoformat()
    return pd.DataFrame([row])


def main():
    st.set_page_config(page_title="Bank Transaction Fraud Predictor", layout="centered")
    st.title("Bank Transaction Fraud Detection — Predict")

    st.markdown(
        "Upload a trained model file (`.pkl`, `.joblib`, or CatBoost `.cbm`).\n\nIf you don't have a file yet, place it in `streamlit_app/models/` and reload."
    )

    # Sidebar: model options
    with st.sidebar.expander("Model"):
        uploaded = st.file_uploader("Upload model file (.pkl/.joblib/.cbm)", type=["pkl", "joblib", "cbm", "bin"])
        model_path_input = st.text_input("Or local model path (relative to repo)", value="streamlit_app/models/catboost_model.cbm")
        st.markdown("---")
        use_catboost_default = st.checkbox("Prefer CatBoost and use notebook defaults if no model provided", value=True)
        st.markdown("**CatBoost defaults (from notebook):**")
        st.caption("iterations=700, learning_rate=0.05, depth=4, class_weights=[1,4.5], l2_leaf_reg=3")
        st.caption("random_strength=1, bagging_temperature=1, eval_metric='AUC'")

    model = None
    # prefer uploaded
    if uploaded is not None:
        temp_path = os.path.join(".", "streamlit_uploaded_model")
        with open(temp_path, "wb") as f:
            f.write(uploaded.getbuffer())
        try:
            model = load_model_from_file(temp_path)
        except Exception as e:
            st.sidebar.error(f"Failed to load uploaded model: {e}")
    else:
        if os.path.exists(model_path_input):
            try:
                model = load_model_from_file(model_path_input)
            except Exception as e:
                st.sidebar.error(f"Failed to load model at {model_path_input}: {e}")

    # If still no model and the user wants CatBoost defaults, instantiate default CatBoostClassifier
    if model is None and use_catboost_default:
        if CatBoostClassifier is None:
            st.sidebar.warning("CatBoost is not installed; add 'catboost' to requirements.txt to enable defaults.")
        else:
            default_params = dict(
                iterations=700,
                learning_rate=0.05,
                depth=4,
                loss_function='Logloss',
                eval_metric='AUC',
                class_weights=[1, 4.5],
                l2_leaf_reg=3,
                random_strength=1,
                bagging_temperature=1,
                verbose=0,
            )
            try:
                model = CatBoostClassifier(**default_params)
                st.sidebar.info("Default CatBoostClassifier instantiated (untrained). Upload a trained .cbm to make predictions.")
            except Exception as e:
                st.sidebar.error(f"Failed to instantiate CatBoostClassifier: {e}")

    if model is None:
        st.warning("No model loaded yet. Upload a model or place it at the local path and reload.")

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
            return

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

        try:
            pred, prob = predict(model, X)
        except Exception as e:
            st.error(f"Prediction failed: {e}")
            return

        st.write("**Prediction**")
        if prob is None:
            st.info(f"Predicted class: {pred}")
        else:
            st.info(f"Predicted class: {pred} — probability fraud: {prob:.3f}")


if __name__ == "__main__":
    main()
