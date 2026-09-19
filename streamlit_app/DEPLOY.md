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

Live: https://my-data-science-project-2ccfjojzs2vz353tfaxyqk.streamlit.app/

1. Deploy
   - Go to https://share.streamlit.io/ → "New app" → repo `SighanoCel/My-data-science-project`.
   - Branch `main`, file path `streamlit_app/bank_churn_app.py`.
   - Click "Deploy". The build only needs `streamlit`, `numpy` and `pandas` for this app,
     so it is quick — see "No TensorFlow on the server" below.

2. No TensorFlow on the server
   The app does NOT import TensorFlow to make predictions, and `tensorflow-cpu` is
   deliberately absent from `requirements.txt`.

   The network is three dense layers (16 → 64 → 32 → 1) and dropout is inactive at
   inference, so a prediction is three matrix multiplies and a sigmoid. Importing
   TensorFlow to do that costs roughly 500 MB of resident memory in a container that
   also holds langchain, chromadb, catboost and pymupdf from the shared requirements
   file — which is what made the first deployment crash with "Oh no. Error running app."

   `NumpyChurnModel` in `bank_churn_app.py` runs the same forward pass from the weights
   in `churn_weights.npz`. It was checked against Keras over all 10,000 rows:
   max absolute difference 2e-7, identical decisions at every threshold. `NumpyScaler`
   does the same for StandardScaler, so scikit-learn is not needed at serving either.

   TensorFlow, scikit-learn and imbalanced-learn remain optional imports, used only by
   the in-app training section. Where they are missing that section is disabled and
   everything else works.

3. The model — already committed, no action needed
   `streamlit_app/models/` holds a trained network ready to serve:

   | File | Contents |
   |---|---|
   | `churn_weights.npz`       | layer weights + scaler stats (16 KB) — **what the app serves** |
   | `churn_keras_model.keras` | the original Keras model (67 KB) |
   | `churn_scaler.joblib`     | the fitted StandardScaler |
   | `churn_features.json`     | the training column order |
   | `churn_model_bundle.joblib` | model + scaler + features in one joblib file |

   Trained with the notebook pipeline on the full 10,000-row Customer-Churn-Records.csv,
   seeded for reproducibility. Test-set scores at threshold 0.4: recall 0.576,
   precision 0.598, accuracy 0.83 — in line with the notebook's own run
   (recall 0.63, precision 0.57), the difference being unseeded weight initialization.

   The app loads these at startup. To replace them, use either route below.

   a) Train inside the app (local only — needs tensorflow-cpu, scikit-learn,
      imbalanced-learn installed; the button is disabled when they are missing)
      - Sidebar → "Train model from dataset" → upload `Customer-Churn-Records.csv`
        (Kaggle: "Bank Customer Churn" records, the same file used by the notebook).
      - Click "Train Keras Sequential model". Training reproduces the notebook pipeline
        (drop leaking `Complain`, one-hot encode, StandardScaler, SMOTE 0.4, 60 epochs)
        and reports recall/precision/confusion matrix on the held-out test set.
      - Artifacts are written to `streamlit_app/models/` for the rest of the session.

   b) Ship a pre-trained model (durable — recommended)
      - The notebook `banking_churn_with_deep_learning.ipynb` now ends with a
        "Saving the trained model for deployment" section. Run those cells after training;
        they write four files and download them out of Colab:

        | File | Contents |
        |---|---|
        | `churn_keras_model.keras` | the network |
        | `churn_scaler.joblib`     | the fitted StandardScaler |
        | `churn_features.json`     | the training column order |
        | `churn_model_bundle.joblib` | all three in one joblib file |

      - Commit them to `streamlit_app/models/`. The app prefers `churn_weights.npz`,
        then `churn_keras_model.keras`, then the bundle; you can also upload any of
        them in the sidebar. Training inside the app refreshes the .npz automatically,
        so a retrained model stays deployable without TensorFlow.
      - The bundle needs Keras 3 (TensorFlow ≥ 2.16) to pickle the model; verified on
        TF 2.21 / Keras 3.15. On older Keras the notebook skips the bundle and the three
        separate files still work.

4. Notes
   - Retraining is a local workflow, not a deployed one: the server has no TensorFlow,
     and Streamlit Cloud's filesystem is ephemeral, so anything trained in a session is
     lost on restart. Commit the artifacts (route b) to change what the app serves.
   - Decision threshold defaults to 0.4, the value the notebook chose to favour recall.
   - The ROI panel appears after training, using the held-out test set
     (contact cost $3, retained-churner profit $40 by default).
