# 🏢 Financial Health Prediction using Machine Learning

This project builds a full machine learning pipeline to evaluate the financial health of Slovak companies based on official accounting data. The pipeline includes data retrieval, metric calculation, preprocessing, modeling, and prediction storage into a PostgreSQL database with optional support for Qlik-based reporting.

---



## Summary

- **Goal**: Predict **Return on Assets (ROA)** and **Bankruptcy Risk** for Slovak companies
- **Domain**: Financial statements (SK NACE 27900 — Manufacture of electrical equipment)
- **Source**: Register účtovných závierok (Public Financial Statement Register)
- **Prediction Output**: Written to PostgreSQL DB, optionally connected to Qlik for dashboarding
- **Documentation**: Complete methodology with in depth analysis is explained in my Master’s Thesis which will be published at the end of april 2025. Link will be provided after official publication.

---

## Key features

1. **Extract Data**  
   Scrape financial statements from the Slovak RÚZ API based on company IČO(identification number) codes.

2. **Calculate Metrics**  
   Map rows of balance sheets and income statements into to calculate selected financial indicators:
   - Likvidita 1. stupňa / Liquidity Ratio (1st degree) – Cash Ratio
   - Likvidita 2. stupňa / Liquidity Ratio (2nd degree) – Quick Ratio
   - Likvidita 3. stupňa / Liquidity Ratio (3rd degree) – Current Ratio
   - ROA, ROE, ROI, ROS, ROC
   - Zisková marža / Profit Margin
   - Stupeň samofinancovania / Self-Financing Ratio
   - Stupeň zadĺženosti / Debt Ratio
   - Doba splácania záväzkov / Accounts Payable Repayment Period (in days)
   - Finančná páka / Financial Leverage
   - Obrat celkových aktív / Total Asset Turnover
   - Obrat dlhodobého majetku / Fixed Asset Turnover
   - Doba obratu zásob / Inventory Turnover Period (in days)

3. **Clean & Engineer Features**
   - Data exploration
   - Winsorization
   - Missing value imputation
   - Log + shift transformation
   - Feature selection

4. **Train Models**  
   - Regression (ROA): XGBoost, HistGradientBoosting, Random Forest
   Includes evaluation with RMSE, MSE, R2, Adjusted R2 
   - Classification (Bankruptcy): XGBoost, LightGBM, Random Forest  
   Includes evaluation with AUC, precision, recall, F1, SHAP explanations

5. **Run Predictions**  
   - Load an Excel file with metrics
   - Run predictions with selected model(s)
   - Store predictions in PostgreSQL DB

6. **Visualize in Qlik** *(Optional)*  
   - PostgreSQL tables are directly connected to Qlik dashboards

---

## **Technology Stack**
- **Python – scikit-learn, NumPy, Pandas, MatPlotLib**
- **Data Processing – Feature engineering, class balancing, log transformation, imputation and outliers removal techniques**
- **Model Training – Random Forest, XGBoost, Logistic Regression, LightGBM**
- **Explanation - SHAP summary**
- **CI/CD with Github Actions**
- **Docker support**

---

## Results
**Results of classification models can be found in folder \classification models results**
**Results of regression models can be found directly in file \notebooks\Regression models - Predicting ROA.**

## **Top Features Influencing Bankruptcy Predictions by Shap importance**
- **Obrat aktív/Asset turnover ratio**
- **Doba splácania záväzkov/Accounts Payable Repayment Period**
- **Finančná páka/Financial leverage**
- **ROE**

## **Top Features Influencing ROA Predictions by Shap importance**
- **ROS**
- **ROE**
- **ROC**
- **Profitability ratio**

---

## Running Predictions
python scripts/predict.py --file data/sample_input.xlsx --roa_model_name --bank_model_name

## Docker Support

# Run prediction inside container
docker run --rm -v ${PWD}:/app financial-predictor \
    python predict.py --file your_data.xlsx --roa_model_name --bank_model_name

---

# CI/CD with GitHub Actions
The repository includes a GitHub Actions workflow to:
- Lint code
- Check for correct model loading
- Run dummy predictions
- Keep pipeline robust

# PostgreSQL Output Schema
**roa_predictions**
→ ROA predictions by model, company, and year

**bankruptcy_predictions**
→ Binary class + probability of bankruptcy with timestamps

---

## Possible improvements
- Gather more instances of bankruptcy to balance the dataset (SMOTE and other techniques have been applied during test with low results)
- Implement MLflow or Weights & Biases to track models, metrics, and parameters over time
- Integrate notebooks to one unified pipeline
- Include other financial, domain or macroeconomic indicators as additional features to improve model performance
- Deploy as API for Realtime Scoring - wrap the prediction logic in a FastAPI or Flask service. This allows uploading financial Excel files via UI or API and returning instant results.

---

## Authors & Thesis
This work was developed as part and supplement of a Master’s thesis on a topic - Measurement and assessment of the financial health of the selected exporting company.

Do not hesitate to reach out or contribute to this project for further improvements.