import pandas as pd
df = pd.read_csv("/root/.claude/uploads/e0edc0c6-eb30-56ed-ad48-c2d1ce79cd97/fe887add-Customer_Transactions.csv")
print("Date range:", df['last_purchase_date'].min(), df['last_purchase_date'].max())

# High-risk segment real baseline: high cart abandon + low spending score (top real drivers)
seg = df[(df['cart_abandon_rate'] >= 0.7) & (df['spending_score'] <= 25)]
print("High-risk segment size:", len(seg), "churn rate:", seg['churned'].mean())

low_risk = df[(df['cart_abandon_rate'] < 0.3) & (df['spending_score'] > 50)]
print("Low-risk segment size:", len(low_risk), "churn rate:", low_risk['churned'].mean())

print("Overall churn:", df['churned'].mean())
print("n churned total:", df['churned'].sum())

# quartiles of cart_abandon_rate and spending score
print(df['cart_abandon_rate'].describe())
print(df['spending_score'].describe())
