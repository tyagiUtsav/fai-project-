import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report
import json

SRC = "/root/.claude/uploads/e0edc0c6-eb30-56ed-ad48-c2d1ce79cd97/fe887add-Customer_Transactions.csv"
df = pd.read_csv(SRC)

print("Shape:", df.shape)
print("Churn rate:", df['churned'].mean())
print(df.dtypes)
print(df.isnull().sum())

num_cols = ['age','annual_income','spending_score','num_purchases','avg_purchase_value',
            'membership_years','website_visits_per_month','cart_abandon_rate']
cat_cols = ['gender','country']
target = 'churned'

X = df[num_cols + cat_cols]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

pre = ColumnTransformer([
    ('num', StandardScaler(), num_cols),
    ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
])

results = {}

for name, clf in [
    ('logistic_regression', LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42)),
    ('random_forest', RandomForestClassifier(n_estimators=300, max_depth=8, class_weight='balanced', random_state=42))
]:
    pipe = Pipeline([('pre', pre), ('clf', clf)])
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    y_proba = pipe.predict_proba(X_test)[:,1]
    results[name] = {
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1': f1_score(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, y_proba),
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
        'churn_rate_test': float(y_test.mean()),
        'n_test': len(y_test)
    }
    print(f"\n=== {name} ===")
    print(classification_report(y_test, y_pred, digits=3))
    print("ROC-AUC:", results[name]['roc_auc'])

# Feature importance from random forest
rf_pipe = Pipeline([('pre', pre), ('clf', RandomForestClassifier(n_estimators=300, max_depth=8, class_weight='balanced', random_state=42))])
rf_pipe.fit(X_train, y_train)
feat_names = num_cols + list(rf_pipe.named_steps['pre'].named_transformers_['cat'].get_feature_names_out(cat_cols))
importances = rf_pipe.named_steps['clf'].feature_importances_
feat_imp = sorted(zip(feat_names, importances), key=lambda x: -x[1])
print("\nTop feature importances (Random Forest):")
for f, i in feat_imp[:10]:
    print(f"  {f}: {i:.4f}")

results['feature_importance_top10'] = [[f, float(i)] for f, i in feat_imp[:10]]

# Correlation of churn with numeric features
corrs = df[num_cols + ['churned']].corr()['churned'].drop('churned').sort_values()
print("\nCorrelation with churn:")
print(corrs)
results['correlations'] = corrs.to_dict()

# Basic descriptive stats for dataset slide
desc = {
    'n_records': len(df),
    'n_features': df.shape[1],
    'churn_rate_overall': float(df['churned'].mean()),
    'countries': df['country'].value_counts().to_dict(),
    'gender_dist': df['gender'].value_counts().to_dict(),
    'age_range': [int(df['age'].min()), int(df['age'].max())],
    'age_mean': float(df['age'].mean()),
    'income_mean': float(df['annual_income'].mean()),
    'avg_purchase_value_mean': float(df['avg_purchase_value'].mean()),
    'cart_abandon_rate_mean': float(df['cart_abandon_rate'].mean()),
    'membership_years_mean': float(df['membership_years'].mean()),
}
results['dataset_description'] = desc

with open('/tmp/claude-0/-home-user/e0edc0c6-eb30-56ed-ad48-c2d1ce79cd97/scratchpad/analysis/results.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)

print("\nDONE")
