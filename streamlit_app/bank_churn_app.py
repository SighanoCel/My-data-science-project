import json
import os

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, precision_score, recall_score

try:
    import joblib
except Exception:
    joblib = None

try:
    import tensorflow as tf
    from tensorflow import keras
except Exception:
    tf = None
    keras = None

try:
    from imblearn.over_sampling import SMOTE
except Exception:
    SMOTE = None


# Categorical options exactly as they appear in Customer-Churn-Records.csv.
GEOGRAPHY_OPTIONS = ["France", "Germany", "Spain"]
GENDER_OPTIONS = ["Female", "Male"]
CARD_TYPE_OPTIONS = ["DIAMOND", "GOLD", "PLATINUM", "SILVER"]

# Feature order must match the notebook:
# data = concat([get_dummies(objects, drop_first=True), numerics]) then X = data.drop('churn').
# drop_first removes Geography_France, Gender_Female and Card Type_DIAMOND.
EXPECTED_FEATURES = [
    "Geography_Germany",
    "Geography_Spain",
    "Gender_Male",
    "Card Type_GOLD",
    "Card Type_PLATINUM",
    "Card Type_SILVER",
    "CreditScore",
    "Age",
    "Tenure",
    "Balance",
    "NumOfProducts",
    "HasCrCard",
    "IsActiveMember",
    "EstimatedSalary",
    "Satisfaction Score",
    "Point Earned",
]

MODELS_DIR = os.path.join("streamlit_app", "models")
MODEL_PATH = os.path.join(MODELS_DIR, "churn_keras_model.keras")
SCALER_PATH = os.path.join(MODELS_DIR, "churn_scaler.joblib")
FEATURES_PATH = os.path.join(MODELS_DIR, "churn_features.json")
# Single-file alternative written by the notebook: {'model', 'scaler', 'features'}.
BUNDLE_PATH = os.path.join(MODELS_DIR, "churn_model_bundle.joblib")
DEFAULT_CSV_PATH = os.path.join("streamlit_app", "data", "Customer-Churn-Records.csv")

# Notebook defaults.
DEFAULT_THRESHOLD = 0.4
DEFAULT_CONTACT_COST = 3
DEFAULT_REVENUE_PROFIT = 40


def load_model_from_file(path):
    """Load a Keras model saved as .keras / .h5, or a joblib bundle/pickled model.

    Returns either the model, or the {'model', 'scaler', 'features'} dict the
    notebook's bundle contains — unpack_bundle() sorts out which.
    """
    if path is None or not os.path.exists(path):
        return None
    ext = os.path.splitext(path)[1].lower()
    if ext in (".joblib", ".pkl"):
        if joblib is None:
            raise RuntimeError("joblib is not available in this environment")
        return joblib.load(path)
    if keras is None:
        raise RuntimeError("TensorFlow/Keras is not installed in this environment")
    return keras.models.load_model(path)


def unpack_bundle(obj):
    """Split a loaded artifact into (model, scaler, feature_order)."""
    if isinstance(obj, dict):
        return obj.get("model"), obj.get("scaler"), obj.get("features")
    return obj, None, None


def load_scaler_from_file(path):
    if path is None or not os.path.exists(path):
        return None
    if joblib is None:
        raise RuntimeError("joblib is not available in this environment")
    return joblib.load(path)


def load_feature_order(path):
    if path is None or not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def build_input_dataframe(values: dict, feature_order=None) -> pd.DataFrame:
    """One-hot encode a single customer the same way the notebook does, in training order."""
    features = feature_order or EXPECTED_FEATURES

    geography = values.get("Geography")
    gender = values.get("Gender")
    card_type = values.get("Card Type")

    row = {
        "Geography_Germany": int(geography == "Germany"),
        "Geography_Spain": int(geography == "Spain"),
        "Gender_Male": int(gender == "Male"),
        "Card Type_GOLD": int(card_type == "GOLD"),
        "Card Type_PLATINUM": int(card_type == "PLATINUM"),
        "Card Type_SILVER": int(card_type == "SILVER"),
        "CreditScore": int(values.get("CreditScore", 0)),
        "Age": int(values.get("Age", 0)),
        "Tenure": int(values.get("Tenure", 0)),
        "Balance": float(values.get("Balance", 0.0)),
        "NumOfProducts": int(values.get("NumOfProducts", 1)),
        "HasCrCard": int(values.get("HasCrCard", 0)),
        "IsActiveMember": int(values.get("IsActiveMember", 0)),
        "EstimatedSalary": float(values.get("EstimatedSalary", 0.0)),
        "Satisfaction Score": int(values.get("Satisfaction Score", 3)),
        "Point Earned": int(values.get("Point Earned", 0)),
    }

    # Any feature the saved model expects but we don't produce defaults to 0.
    ordered = {k: row.get(k, 0) for k in features}
    return pd.DataFrame([ordered])


def predict_proba(model, scaler, X: pd.DataFrame) -> float:
    """Return the sigmoid output = probability of churn (class 1)."""
    if scaler is not None:
        X_input = scaler.transform(X)
    else:
        X_input = X.values
    try:
        proba = model.predict(X_input, verbose=0)
    except TypeError:
        proba = model.predict(X_input)
    return float(np.asarray(proba).ravel()[0])


def prepare_dataframe(df: pd.DataFrame):
    """Notebook cleaning pipeline: drop IDs, rename target, drop the leaking 'Complain'."""
    df = df.drop(["RowNumber", "CustomerId", "Surname"], axis=1, errors="ignore")
    if "Exited" in df.columns:
        df = df.rename(columns={"Exited": "churn"})
    if "churn" not in df.columns:
        raise RuntimeError("Dataset must contain an 'Exited' (or 'churn') target column")
    # 'Complain' is ~100% correlated with the target -> data leakage.
    df = df.drop("Complain", axis=1, errors="ignore")

    features_object = df.select_dtypes(include="object")
    features_digit = df.select_dtypes(exclude="object")
    object_encoded = pd.get_dummies(features_object, drop_first=True, dtype=int)
    data = pd.concat([object_encoded, features_digit], axis=1)

    X = data.drop("churn", axis=1)
    y = df["churn"].values
    return X, y


def build_keras_model(n_features: int):
    """Sequential 64 -> 32 -> 1 with dropout and L2, exactly as in the notebook."""
    model = keras.Sequential()
    model.add(keras.layers.Input(shape=(n_features,)))
    model.add(
        keras.layers.Dense(
            units=64,
            activation="relu",
            kernel_initializer="he_normal",
            kernel_regularizer=keras.regularizers.l2(0.001),
        )
    )
    model.add(keras.layers.Dropout(0.2))
    model.add(
        keras.layers.Dense(
            units=32,
            activation="relu",
            kernel_initializer="he_normal",
            kernel_regularizer=keras.regularizers.l2(0.001),
        )
    )
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Dense(units=1, activation="sigmoid", kernel_initializer="glorot_uniform"))
    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=[keras.metrics.Recall(name="recall")],
    )
    return model


def train_model_from_dataframe(df: pd.DataFrame, epochs: int = 60, threshold: float = DEFAULT_THRESHOLD):
    if keras is None:
        raise RuntimeError("TensorFlow is not installed in this environment")
    if SMOTE is None:
        raise RuntimeError("imbalanced-learn is not installed in this environment")

    X, y = prepare_dataframe(df)
    feature_order = list(X.columns)

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1, test_size=0.3, stratify=y)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    # The notebook re-fits the scaler on the test set; transform() is the correct call
    # and is what inference below relies on, so we use it here too.
    X_test_scaled = scaler.transform(X_test)

    # SMOTE only oversamples: if the data is already less imbalanced than the target
    # ratio it raises, so skip it rather than fail the whole training run.
    counts = np.bincount(y_train.astype(int))
    current_ratio = counts.min() / counts.max() if counts.max() else 0
    if current_ratio < 0.4:
        over_smote = SMOTE(sampling_strategy=0.4, random_state=1, k_neighbors=2)
        X_train_smote, y_train_smote = over_smote.fit_resample(X_train_scaled, y_train)
    else:
        X_train_smote, y_train_smote = X_train_scaled, y_train

    model = build_keras_model(X_train_smote.shape[1])
    model.fit(X_train_smote, y_train_smote, epochs=epochs, verbose=0)

    prediction = model.predict(X_test_scaled, verbose=0).ravel()
    prediction_binary = (prediction > threshold).astype(int)

    metrics = {
        "recall": recall_score(y_test, prediction_binary),
        "precision": precision_score(y_test, prediction_binary, zero_division=0),
        "confusion_matrix": confusion_matrix(y_test, prediction_binary),
        "report": classification_report(y_test, prediction_binary, zero_division=0),
        "threshold": threshold,
    }

    os.makedirs(MODELS_DIR, exist_ok=True)
    model.save(MODEL_PATH)
    if joblib is not None:
        joblib.dump(scaler, SCALER_PATH)
    with open(FEATURES_PATH, "w", encoding="utf-8") as f:
        json.dump(feature_order, f)

    return model, scaler, feature_order, metrics, {"y_test": y_test, "score": prediction}


def roi_table(y_test, score, contact_cost: float, revenue_profit: float) -> pd.DataFrame:
    """Bin churn scores in 1% steps and cumulate cost vs retained revenue (notebook ROI analysis)."""
    class_score = np.arange(0.0, 1.01, 0.01)
    roi_analysis = pd.DataFrame({"target": np.asarray(y_test).ravel(), "score": np.asarray(score).ravel()})
    roi_analysis["score_bin"] = pd.cut(roi_analysis["score"], bins=class_score, include_lowest=True, labels=False)

    agg = roi_analysis.groupby("score_bin").agg(reported=("target", "count"), hit=("target", "sum"))
    # Bins are ascending; targeting starts with the highest scores, so cumulate downwards.
    agg = agg.sort_index(ascending=False)
    agg["reported_cum"] = agg["reported"].cumsum()
    agg["hit_cum"] = agg["hit"].cumsum()

    tot_churn_test = int(np.sum(np.asarray(y_test) == 1))
    agg["precision"] = agg["hit_cum"] / agg["reported_cum"]
    agg["recall"] = agg["hit_cum"] / tot_churn_test if tot_churn_test else np.nan
    agg["tot_contact_cost"] = agg["reported_cum"] * contact_cost
    agg["tot_revenue_profit"] = agg["hit_cum"] * revenue_profit
    agg["return_on_investment"] = agg["tot_revenue_profit"] - agg["tot_contact_cost"]

    agg = agg.sort_index()
    agg.index = (agg.index.astype(float) / 100).round(2)
    agg.index.name = "score_threshold"
    return agg


def main():
    st.set_page_config(page_title="Bank Customer Churn Predictor", layout="centered")
    st.title("Customer Banking Churn Prediction — Keras Sequential Model")

    st.markdown(
        "Predict whether a bank customer is likely to churn, using the TensorFlow Keras "
        "Sequential network from the project notebook.\n\n"
        "The model needs a fitted `StandardScaler` alongside it. Load either the "
        "`churn_model_bundle.joblib` saved by the notebook, or a `.keras` model plus its "
        "scaler, in the sidebar — or train from the `Customer-Churn-Records.csv` dataset "
        "in **Train model from dataset**."
    )

    if keras is None:
        st.error("TensorFlow is not installed in this environment. Add `tensorflow-cpu` to requirements.txt.")

    model = st.session_state.get("churn_model")
    scaler = st.session_state.get("churn_scaler")
    feature_order = st.session_state.get("churn_features")

    # Sidebar: model options
    with st.sidebar.expander("Model", expanded=True):
        uploaded_model = st.file_uploader(
            "Upload model (.keras/.h5) or joblib bundle", type=["keras", "h5", "joblib", "pkl"]
        )
        uploaded_scaler = st.file_uploader("Upload fitted scaler (.joblib/.pkl)", type=["joblib", "pkl"])
        default_model_path = BUNDLE_PATH if (not os.path.exists(MODEL_PATH) and os.path.exists(BUNDLE_PATH)) else MODEL_PATH
        model_path_input = st.text_input("Or local model path", value=default_model_path)
        scaler_path_input = st.text_input("Or local scaler path", value=SCALER_PATH)
        st.markdown("---")
        st.markdown("**Network architecture (from notebook):**")
        st.caption("Dense(64, relu, he_normal, L2=0.001) → Dropout(0.2)")
        st.caption("Dense(32, relu, he_normal, L2=0.001) → Dropout(0.2)")
        st.caption("Dense(1, sigmoid) · adam · binary_crossentropy · recall")
        st.caption("SMOTE(sampling_strategy=0.4, k_neighbors=2) · 60 epochs")

    def store_loaded(obj):
        """Accept a bare model or a bundle, keeping any scaler/features it carries."""
        loaded_model, loaded_scaler, loaded_features = unpack_bundle(obj)
        if loaded_model is not None:
            st.session_state["churn_model"] = loaded_model
        if loaded_scaler is not None:
            st.session_state["churn_scaler"] = loaded_scaler
        if loaded_features:
            st.session_state["churn_features"] = list(loaded_features)
        return loaded_model, loaded_scaler, loaded_features

    if uploaded_model is not None:
        temp_model_path = os.path.join(".", "streamlit_uploaded_model" + os.path.splitext(uploaded_model.name)[1])
        with open(temp_model_path, "wb") as f:
            f.write(uploaded_model.getbuffer())
        try:
            model, bundled_scaler, bundled_features = store_loaded(load_model_from_file(temp_model_path))
            scaler = bundled_scaler or scaler
            feature_order = bundled_features or feature_order
        except Exception as e:
            st.sidebar.error(f"Failed to load uploaded model: {e}")
    elif model is None:
        try:
            model, bundled_scaler, bundled_features = store_loaded(load_model_from_file(model_path_input))
            scaler = bundled_scaler or scaler
            feature_order = bundled_features or feature_order
        except Exception as e:
            st.sidebar.error(f"Failed to load model at {model_path_input}: {e}")

    if uploaded_scaler is not None:
        temp_scaler_path = os.path.join(".", "streamlit_uploaded_scaler.joblib")
        with open(temp_scaler_path, "wb") as f:
            f.write(uploaded_scaler.getbuffer())
        try:
            scaler = load_scaler_from_file(temp_scaler_path)
            st.session_state["churn_scaler"] = scaler
        except Exception as e:
            st.sidebar.error(f"Failed to load uploaded scaler: {e}")
    elif scaler is None:
        try:
            scaler = load_scaler_from_file(scaler_path_input)
            if scaler is not None:
                st.session_state["churn_scaler"] = scaler
        except Exception as e:
            st.sidebar.error(f"Failed to load scaler at {scaler_path_input}: {e}")

    if feature_order is None:
        feature_order = load_feature_order(FEATURES_PATH) or EXPECTED_FEATURES
        st.session_state["churn_features"] = feature_order

    # Sidebar: training
    with st.sidebar.expander("Train model from dataset"):
        data_upload = st.file_uploader("Upload Customer-Churn-Records.csv", type=["csv"], key="train_csv")
        csv_path_input = st.text_input("Or local dataset path", value=DEFAULT_CSV_PATH)
        epochs = st.number_input("Epochs", min_value=1, max_value=300, value=60, step=10)
        train_button = st.button("Train Keras Sequential model")

    if train_button:
        source = data_upload if data_upload is not None else (csv_path_input if os.path.exists(csv_path_input) else None)
        if source is None:
            st.error("No dataset provided. Upload a CSV or give a valid local path.")
        else:
            try:
                df_raw = pd.read_csv(source)
                with st.spinner("Training the neural network — this takes a minute..."):
                    model, scaler, feature_order, metrics, holdout = train_model_from_dataframe(
                        df_raw, epochs=int(epochs)
                    )
                st.session_state["churn_model"] = model
                st.session_state["churn_scaler"] = scaler
                st.session_state["churn_features"] = feature_order
                st.session_state["churn_holdout"] = holdout
                st.success(f"Training finished. Model saved to {MODEL_PATH}")
                col_a, col_b = st.columns(2)
                col_a.metric(f"Recall @ {metrics['threshold']}", f"{metrics['recall']:.3f}")
                col_b.metric(f"Precision @ {metrics['threshold']}", f"{metrics['precision']:.3f}")
                st.text("Classification report (test set)")
                st.code(metrics["report"])
                st.text("Confusion matrix (test set)")
                st.write(
                    pd.DataFrame(
                        metrics["confusion_matrix"],
                        index=["Actual: stays", "Actual: churns"],
                        columns=["Predicted: stays", "Predicted: churns"],
                    )
                )
            except Exception as e:
                st.error(f"Training failed: {e}")

    if model is None:
        st.warning("No model loaded yet. Train one from the dataset, or upload a `.keras` model and its scaler.")
    elif scaler is None:
        st.warning(
            "A model is loaded but no fitted scaler was found. The network was trained on standardized "
            "inputs, so predictions will be wrong without the matching scaler."
        )

    st.subheader("Customer profile")
    with st.form("input_form"):
        col1, col2 = st.columns(2)
        with col1:
            credit_score = st.number_input("Credit Score", min_value=300, max_value=900, value=650, step=1)
            age = st.number_input("Age", min_value=18, max_value=100, value=40, step=1)
            tenure = st.number_input("Tenure (years with the bank)", min_value=0, max_value=10, value=5, step=1)
            balance = st.number_input("Balance", min_value=0.0, value=0.0, format="%.2f")
            estimated_salary = st.number_input("Estimated Salary", min_value=0.0, value=100000.0, format="%.2f")
            point_earned = st.number_input("Points Earned", min_value=0, max_value=1500, value=450, step=1)
        with col2:
            geography = st.selectbox("Geography", GEOGRAPHY_OPTIONS)
            gender = st.selectbox("Gender", GENDER_OPTIONS)
            card_type = st.selectbox("Card Type", CARD_TYPE_OPTIONS)
            num_products = st.selectbox("Number of Products", [1, 2, 3, 4])
            satisfaction = st.selectbox("Satisfaction Score", [1, 2, 3, 4, 5], index=2)
            has_cr_card = st.selectbox("Has Credit Card", ["Yes", "No"])
            is_active = st.selectbox("Is Active Member", ["Yes", "No"])

        threshold = st.slider(
            "Churn decision threshold",
            min_value=0.05,
            max_value=0.95,
            value=DEFAULT_THRESHOLD,
            step=0.05,
            help="The notebook uses 0.4 to favour recall — catching churners matters more than a few false alarms.",
        )

        submitted = st.form_submit_button("Predict churn")

    if submitted:
        if model is None:
            st.error("Please train or load a model before predicting.")
            return

        vals = {
            "CreditScore": credit_score,
            "Geography": geography,
            "Gender": gender,
            "Age": age,
            "Tenure": tenure,
            "Balance": balance,
            "NumOfProducts": num_products,
            "HasCrCard": 1 if has_cr_card == "Yes" else 0,
            "IsActiveMember": 1 if is_active == "Yes" else 0,
            "EstimatedSalary": estimated_salary,
            "Satisfaction Score": satisfaction,
            "Card Type": card_type,
            "Point Earned": point_earned,
        }

        X = build_input_dataframe(vals, feature_order)

        try:
            prob = predict_proba(model, scaler, X)
        except Exception as e:
            st.error(f"Prediction failed: {e}")
            return

        pred = int(prob > threshold)
        st.write("**Prediction**")
        if pred == 1:
            st.error(f"Likely to churn — churn probability: {prob:.3f} (threshold {threshold:.2f})")
        else:
            st.success(f"Likely to stay — churn probability: {prob:.3f} (threshold {threshold:.2f})")
        st.progress(min(max(prob, 0.0), 1.0))

        with st.expander("Encoded model input"):
            st.dataframe(X)

    # ROI analysis on the held-out test set, available once a model has been trained here.
    holdout = st.session_state.get("churn_holdout")
    if holdout is not None:
        st.subheader("Return on Investment analysis")
        st.caption(
            "Contacting every customer above a score threshold costs money; retaining an actual "
            "churner earns it back. The peak of the curve is the threshold to hand to marketing."
        )
        col_c, col_r = st.columns(2)
        contact_cost = col_c.number_input("Contact cost per customer ($)", min_value=0.0, value=float(DEFAULT_CONTACT_COST), step=1.0)
        revenue_profit = col_r.number_input("Profit per retained churner ($)", min_value=0.0, value=float(DEFAULT_REVENUE_PROFIT), step=1.0)

        agg = roi_table(holdout["y_test"], holdout["score"], contact_cost, revenue_profit)
        st.line_chart(agg["return_on_investment"])
        best_threshold = agg["return_on_investment"].idxmax()
        best_value = agg["return_on_investment"].max()
        st.info(f"Peak ROI ${best_value:,.0f} when targeting customers scored above {best_threshold:.2f}")
        with st.expander("ROI table"):
            st.dataframe(agg)


if __name__ == "__main__":
    main()
