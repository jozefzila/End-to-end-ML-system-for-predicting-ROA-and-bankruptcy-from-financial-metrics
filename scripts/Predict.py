# %% [markdown]
# # Predicting ROA and Bankruptcy for Companies
# 
# This script is a Python pipeline that allows users to  run predictions with desired model and save results to a PostgreSQL database. It is meant to be used outside of Jupyter, e.g. via VS Code or a CI/CD pipeline.
# 
# ## Input
# The script accepts an Excel file (`.xlsx`) with the following structure:
# - `firma` — company name
# - `rok` — year of the financial statement
# - Financial metrics — all relevant variables required by the trained models
# 
# 
# Models are expected to be located in the `models/` folder and saved in `.sav` format using `joblib`.
# 
# ## How to Run (example)
# 
# ```bash
# python predict.py --file input_data.xlsx --roa_model xgb --bank_model rf
# 

# %%
import pandas as pd
import joblib
from datetime import datetime
from sqlalchemy import create_engine
import argparse

# CONFIG: set paths and DB string

ROA_MODELS = {
    "xgb": "models/XGB.sav",
    "hgb": "models/HGB.sav",
    "rf" : "models/RF.sav"
}

BANKRUPTCY_MODELS = {
    "rf": "models/RF_class.sav",
    "xgb": "models/XGB_class.sav",
    "lgb": "models/LGB_class.sav"
}

from dotenv import load_dotenv
import os

load_dotenv()

DB_CONN_STR = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"


# UTILITY: Load model safely

def load_model(path):
    try:
        return joblib.load(path)
    except Exception as e:
        print(f"Error loading model from {path}: {e}")
        exit()

# MAIN FUNCTION

def run_prediction(input_file, roa_model_key, bank_model_key):
    # Load financial data
    df = pd.read_excel(input_file)
    print("Loaded input data.")

    df_meta = df[["firma", "rok"]].copy() #Company and year info
    df_meta.columns = ["company_name", "year"]

    # Drop ID columns if needed
    features = df.drop(columns=["firma", "rok"])

    # DB connection
    engine = create_engine(DB_CONN_STR)

    # ROA Prediction
    if roa_model_key:
        model_path = ROA_MODELS.get(roa_model_key.lower())
        if not model_path:
            print(f"Unknown ROA model '{roa_model_key}'. Available: {list(ROA_MODELS.keys())}")
        else:
            model = load_model(model_path)
            y_pred = model.predict(features)

            df_roa = df_meta.copy()
            df_roa["model_name"] = roa_model_key.upper()
            df_roa["predicted_roa"] = y_pred
            df_roa["prediction_date"] = datetime.now()

            df_roa.to_sql("roa_predictions", engine, if_exists="append", index=False)
            print("ROA predictions inserted into DB.")

    # Bankruptcy Prediction
    if bank_model_key:
        model_path = BANKRUPTCY_MODELS.get(bank_model_key.lower())
        if not model_path:
            print(f"Unknown bankruptcy model '{bank_model_key}'. Available: {list(BANKRUPTCY_MODELS.keys())}")
        else:
            model = load_model(model_path)
            probs = model.predict_proba(features)[:, 1]
            preds = (probs >= 0.5).astype(int)

            df_bank = df_meta.copy()
            df_bank["model_name"] = bank_model_key.upper()
            df_bank["predicted_class"] = preds
            df_bank["probability"] = probs
            df_bank["prediction_date"] = datetime.now()

            df_bank.to_sql("bankruptcy_predictions", engine, if_exists="append", index=False)
            print("Bankruptcy predictions inserted into DB.")

# CLI: Run from terminal
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run ROA/Bankruptcy predictions and insert into PostgreSQL.")

    parser.add_argument("--file", required=True, help="Path to input Excel file")
    parser.add_argument("--roa_model", help="ROA model to use: XGB, HGB, RF")
    parser.add_argument("--bank_model", help="Bankruptcy model to use: RF, XGB, LGB")

    args = parser.parse_args()

    run_prediction(args.file, args.roa_model, args.bank_model)


# %% [markdown]
# ###  Qlik Connection
# 
# To allow non-technical stakeholders to interactively view model predictions, we connected Qlik Sense to the PostgreSQL database containing results.
# 
# Steps taken:
# 1. Created a new app in Qlik
# 2. Add a new **PostgreSQL data connection** with correct host, user, and password
# 3. Load the `roa_predictions` and `bankruptcy_predictions` tables from database
# 4. Build visualizations and filters for company, year, model, and prediction score
# 


