import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, precision_score, classification_report
import xgboost as xgb
import shap
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def train_churn_model(rfm_df: pd.DataFrame):
    """
    Trains an XGBoost classifier to predict churn and generates SHAP explainability.
    
    Args:
        rfm_df (pd.DataFrame): RFM table with 'Churn' target variable.
        
    Returns:
        xgb.XGBClassifier: Trained XGBoost model.
    """
    logger.info("Training XGBoost Churn Prediction Model...")
    
    # Features and Target
    X = rfm_df[['Recency', 'Frequency', 'Monetary']]
    y = rfm_df['Churn']
    
    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Initialize and Train XGBoost
    model = xgb.XGBClassifier(
        objective='binary:logistic',
        eval_metric='auc',
        use_label_encoder=False,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    y_pred = model.predict(X_test)
    
    auc_roc = roc_auc_score(y_test, y_pred_proba)
    
    logger.info(f"Model Evaluation - AUC-ROC: {auc_roc:.4f}")
    logger.info(f"\n{classification_report(y_test, y_pred)}")
    
    # SHAP Explainability (F-04 Requirement)
    generate_shap_explanations(model, X_train)
    
    return model

def generate_shap_explanations(model: xgb.XGBClassifier, X_train: pd.DataFrame):
    """
    Generates SHAP (SHapley Additive exPlanations) summary plots 
    to interpret the churn model's decisions.
    """
    logger.info("Generating SHAP explainability plots...")
    
    # Create SHAP explainer
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_train)
    
    # Save a summary plot
    import matplotlib.pyplot as plt
    plt.figure()
    shap.summary_plot(shap_values, X_train, show=False)
    plt.savefig("reports/figures/shap_churn_summary.png", bbox_inches='tight')
    logger.info("Saved SHAP summary plot to reports/figures/shap_churn_summary.png")
    plt.close()