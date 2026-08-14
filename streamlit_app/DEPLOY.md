Streamlit Cloud deployment instructions

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
   - If CatBoost isn't in `requirements.txt`, add `catboost` and push; Streamlit will rebuild.

4. After deploy
   - Copy the deployed app URL (it will look like `https://<name>.streamlit.app/` or `https://share.streamlit.io/...`).
   - Send me that URL and I'll update the portfolio (`index.html`) to point to the live app.
