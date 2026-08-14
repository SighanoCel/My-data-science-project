import os
from datetime import datetime

import pandas as pd
import streamlit as st
import json
import ast
import re
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score, precision_score, confusion_matrix
import numpy as np

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


def train_model_from_csv(uploaded_file, params):
    if uploaded_file is None:
        raise RuntimeError("No dataset provided")
    if CatBoostClassifier is None:
        raise RuntimeError("CatBoost is not installed in this environment")

    df = pd.read_csv(uploaded_file)
    # Drop nameOrig if present
    if "nameOrig" in df.columns:
        df = df.drop(["nameOrig"], axis=1)

    # Parse Date if present
    if "Date" in df.columns:
        try:
            df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%y")
        except Exception:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Day"] = df["Date"].dt.day
        df["Month"] = df["Date"].dt.month
        df["Year"] = df["Date"].dt.year
        df["Month_name"] = df["Date"].dt.month_name()

    # Prepare X,y
    if "isFraud" not in df.columns:
        raise RuntimeError("Dataset must contain 'isFraud' target column")

    X = df.copy()
    drop_cols = [c for c in ["Date", "Month_name"] if c in X.columns]
    X = X.drop(drop_cols + ["isFraud"], axis=1, errors="ignore")
    y = df["isFraud"]

    categorical_features = [c for c in ["City", "type", "Card Type", "Exp Type", "Gender"] if c in X.columns]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model_params = params.copy()
    if "class_weights" not in model_params:
        model_params["class_weights"] = [1, 4.5]

    model = CatBoostClassifier(**model_params)

    model.fit(X_train, y_train, cat_features=categorical_features if len(categorical_features) else None,
              eval_set=(X_test, y_test), early_stopping_rounds=20)

    y_pred = model.predict(X_test)
    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    models_dir = os.path.join(os.getcwd(), "streamlit_app", "models")
    os.makedirs(models_dir, exist_ok=True)
    model_path = os.path.join(models_dir, "catboost_model.cbm")
    model.save_model(model_path)

    return model, model_path, {"recall": recall, "precision": precision, "confusion_matrix": cm}


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

    # Training UI: allow user to upload dataset and run training locally
    with st.sidebar.expander("Train model from dataset"):
        data_upload = st.file_uploader("Upload dataset CSV to train model", type=["csv"], key="train_csv")
        train_button = st.button("Train CatBoost model using notebook pipeline")

    if train_button:
        try:
            # Try to parse notebook params
            nb_path = os.path.join(os.getcwd(), "notebooks", "Bank_transaction_fraud_detection.ipynb")
            nb_params = None
            try:
                with open(nb_path, "r", encoding="utf-8") as f:
                    nb = json.load(f)
                for cell in nb.get("cells", []):
                    if cell.get("cell_type") != "code":
                        continue
                    src = "".join(cell.get("source", []))
                    if "final_model = CatBoostClassifier" in src:
                        idx = src.find("CatBoostClassifier")
                        idx = src.find("(", idx)
                        count = 0
                        end = None
                        for i in range(idx, len(src)):
                            if src[i] == "(":
                                count += 1
                            elif src[i] == ")":
                                count -= 1
                                if count == 0:
                                    end = i
                                    break
                        if end:
                            params_str = src[idx + 1: end]
                            ps = re.sub(r"\s+", " ", params_str.strip())
                            ps2 = re.sub(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*=", r'"\1":', ps)
                            dict_str = "{" + ps2 + "}"
                            try:
                                nb_params = ast.literal_eval(dict_str)
                            except Exception:
                                nb_params = None
                        break
            except Exception:
                nb_params = None

            if nb_params is None:
                nb_params = dict(iterations=700, learning_rate=0.05, depth=4, loss_function="Logloss",
                                 eval_metric="AUC", class_weights=[1, 4.5], l2_leaf_reg=3,
                                 random_strength=1, bagging_temperature=1, verbose=100)

            with st.spinner("Training model — this may take several minutes..."):
                model_trained, model_path, metrics = train_model_from_csv(data_upload, nb_params)
            st.success(f"Training finished. Model saved to {model_path}")
            st.write("Metrics:", metrics)
            model = model_trained
        except Exception as e:
            st.error(f"Training failed: {e}")

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
