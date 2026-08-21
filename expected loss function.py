import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

data = pd.read_csv("Customer_loan_data.csv")

X = data.drop(columns=["customer_id", "default"])
y = data["default"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict_proba(X_test)[:, 1]

print("ROC-AUC Score:", roc_auc_score(y_test, predictions))


def probability_of_default(
    credit_lines_outstanding,
    loan_amt_outstanding,
    total_debt_outstanding,
    income,
    years_employed,
    fico_score,
):
    borrower = pd.DataFrame(
        [{
            "credit_lines_outstanding": credit_lines_outstanding,
            "loan_amt_outstanding": loan_amt_outstanding,
            "total_debt_outstanding": total_debt_outstanding,
            "income": income,
            "years_employed": years_employed,
            "fico_score": fico_score
        }]
    )

    return model.predict_proba(borrower)[0][1]


def expected_loss(
    loan_amount,
    credit_lines_outstanding,
    loan_amt_outstanding,
    total_debt_outstanding,
    income,
    years_employed,
    fico_score,
    recovery_rate=0.10
):
    pd_value = probability_of_default(
        credit_lines_outstanding,
        loan_amt_outstanding,
        total_debt_outstanding,
        income,
        years_employed,
        fico_score
    )

    lgd = 1 - recovery_rate

    return pd_value * lgd * loan_amount


pd_estimate = probability_of_default(
    credit_lines_outstanding=3,
    loan_amt_outstanding=25000,
    total_debt_outstanding=40000,
    income=85000,
    years_employed=6,
    fico_score=720
)

loss = expected_loss(
    loan_amount=25000,
    credit_lines_outstanding=3,
    loan_amt_outstanding=25000,
    total_debt_outstanding=40000,
    income=85000,
    years_employed=6,
    fico_score=720
)

print(f"Probability of Default: {pd_estimate:.4f}")
print(f"Expected Loss: £{loss:,.2f}")