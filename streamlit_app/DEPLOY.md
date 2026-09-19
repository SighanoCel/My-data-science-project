Streamlit Cloud deployment instructions

This repository hosts two Streamlit apps. Each one is deployed separately from the same repo.

---

## App 1 — Bank Transaction Fraud Detection (`streamlit_app/bank_fraud_app.py`)

Live: https://my-data-science-project-vhld898jdnzjnqgu3vcvmr.streamlit.app/

1. Requirements
   - Ensure this repository is pushed to GitHub: https://github.com/SighanoCel/My-data-science-project
   - Confirm `requirements.txt` lists needed packages (e.g., streamlit, catboost, pandas)

2. Quick deploy (recommended)
   - Go to https://share.streamlit.io/ and sign in with your GitHub account.
   - Click "New app" → select the `SighanoCel/My-data-science-project` repository.
   - For the branch choose `main` and for the file path enter `streamlit_app/bank_fraud_app.py`.
   - Click "Deploy". Streamlit will build the environment using `requirements.txt`.

3. Notes
   - The app expects a model file. Upload a model in the app sidebar or place it in `streamlit_app/models/` and push to the repo.
   - The trained model `Fraud_catboost_classifier.joblib` is already at the repo root and is the default path.

---

## App 2 — Customer Banking Churn Prediction (`streamlit_app/bank_churn_app.py`)

Planned URL: https://sighanocel-bank-churn.streamlit.app/
(the portfolio already links to this address — set exactly this custom subdomain when deploying)

1. Deploy
   - Go to https://share.streamlit.io/ → "New app" → repo `SighanoCel/My-data-science-project`.
   - Branch `main`, file path `streamlit_app/bank_churn_app.py`.
   - In "Advanced settings" / the app URL field, set the custom subdomain to **`sighanocel-bank-churn`**
     so the deployed address matches the link in `index.html`.
   - Click "Deploy". The build installs `tensorflow-cpu` and `imbalanced-learn`, so the first
     build takes several minutes.

2. Getting a model into the app — the churn model is NOT stored in the repo
   The Keras network only makes sense together with the `StandardScaler` it was trained with,
   so the app supports two routes:

   a) Train inside the app (simplest)
      - Sidebar → "Train model from dataset" → upload `Customer-Churn-Records.csv`
        (Kaggle: "Bank Customer Churn" records, the same file used by the notebook).
      - Click "Train Keras Sequential model". Training reproduces the notebook pipeline
        (drop leaking `Complain`, one-hot encode, StandardScaler, SMOTE 0.4, 60 epochs)
        and reports recall/precision/confusion matrix on the held-out test set.
      - Artifacts are written to `streamlit_app/models/` for the rest of the session.

   b) Ship a pre-trained model
      - In the notebook, after `model.fit(...)`, save both objects:

        ```python
        import joblib, json
        model.save('churn_keras_model.keras')
        joblib.dump(scaler, 'churn_scaler.joblib')
        json.dump(list(X.columns), open('churn_features.json', 'w'))
        ```

      - Commit all three to `streamlit_app/models/`. The app picks them up automatically
        (they are the default paths in the sidebar), or upload them in the sidebar.

   To make the deployed app self-training on first run, commit the dataset to
   `streamlit_app/data/Customer-Churn-Records.csv` and train once from the sidebar.

3. Notes
   - Streamlit Cloud's filesystem is ephemeral: a model trained in the app survives the
     session but is lost when the app restarts. Route (b) is the durable option.
   - Decision threshold defaults to 0.4, the value the notebook chose to favour recall.
   - The ROI panel appears after training, using the held-out test set
     (contact cost $3, retained-churner profit $40 by default).
