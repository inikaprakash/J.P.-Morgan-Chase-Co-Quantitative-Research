# J.P. Morgan Chase & Co. — Quantitative Research

A practical quantitative-finance portfolio covering **credit risk modelling, credit-rating segmentation, natural-gas price forecasting, and commodity storage-contract valuation**.

The repository combines Python models with supporting datasets to demonstrate how statistical learning, optimisation, time-series modelling, and financial mathematics can be applied to problems encountered in quantitative finance.

> **Status:** Educational / research prototype. The models are intentionally lightweight and are not production-grade risk, pricing, investment, or trading systems.

## Contents

- [Overview](#overview)
- [Projects](#projects)
- [Methodology](#methodology)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Key Quantitative Concepts](#key-quantitative-concepts)
- [Limitations](#limitations)
- [Author](#author)
- [Contributing](#contributing)
- [License](#license)

## Overview

This repository contains several related quantitative-research exercises:

1. **Credit risk / probability of default:** trains a Random Forest classifier on customer loan data and exposes a reusable probability-of-default function.
2. **Expected loss:** combines estimated probability of default with loss given default and exposure to estimate credit loss.
3. **Credit-rating optimisation:** partitions FICO scores into rating buckets using dynamic programming and log-likelihood maximisation.
4. **Monotonic rating map:** post-processes the optimised buckets so estimated probability of default is non-increasing across the rating scale.
5. **Natural-gas modelling:** fits a trend-plus-seasonality model to historical natural-gas prices and produces a one-year forecast.
6. **Storage-contract valuation:** uses the natural-gas price model to value a simplified gas storage contract subject to inventory, injection, withdrawal, transaction-cost, and storage constraints.

## Projects

### 1. Credit Risk and Expected Loss

**File:** `expected loss function.py`  
**Dataset:** `Customer_loan_data.csv`

The model trains a `RandomForestClassifier` using customer-level loan and credit variables. The test-set probability estimates are evaluated with **ROC-AUC**.

The script then exposes:

```text
Probability of Default = model-predicted default probability

Expected Loss = PD × LGD × EAD
```

where:

- **PD** — Probability of Default
- **LGD** — Loss Given Default, calculated as `1 - recovery_rate`
- **EAD** — Exposure at Default, represented here by the loan amount

This provides a simple bridge between supervised machine learning and a conventional credit-risk expected-loss framework.

### 2. Credit Rating Map

**File:** `rating map.py`

Customers are sorted by FICO score and divided into a specified number of contiguous buckets. A dynamic-programming procedure maximises the sum of bucket-level Bernoulli log-likelihoods.

For each resulting bucket, the script reports:

- Rating number
- Minimum and maximum FICO score
- Number of borrowers
- Number of defaults
- Estimated probability of default

The `fico_rating()` function then maps an individual FICO score to its corresponding rating and estimated PD.

### 3. Optimised Rating Map

**File:** `optimised rating map.py`

This extends the rating-map approach with two important constraints:

- A minimum bucket size of **5% of the sample**.
- A monotonicity pass that merges adjacent buckets whenever the estimated PD ordering is violated.

The result is a more practical rating structure in which risk estimates are ordered consistently across the FICO-score bands.

### 4. Natural-Gas Price Analysis and Forecasting

**File:** `Data_Analysis_of_Natural_Gases_data.py`  
**Dataset:** `Nat_Gas.csv`

The natural-gas model:

1. Loads and sorts historical observations by date.
2. Fits a regression-style function containing a linear trend and annual seasonality:

```text
Price(t) = a + b·t + c·sin(2πt/12) + d·cos(2πt/12)
```

3. Evaluates the fitted model using **R²** and **RMSE**.
4. Generates a 12-month forecast.
5. Provides `estimate_price(date)` for estimating the model price at a requested date.

The seasonal terms capture recurring annual effects while the linear component captures the underlying trend.

### 5. Natural-Gas Storage Contract Pricing

**File:** `prototype pricing model.py`

The pricing model imports `estimate_price()` from the natural-gas analysis module and simulates a simplified storage strategy.

The contract valuation accounts for:

- Injection dates and withdrawal dates
- Gas volume per transaction
- Maximum storage capacity
- Injection and withdrawal-rate limits
- Injection/withdrawal transaction costs
- Monthly storage costs
- Modelled natural-gas prices

The implementation tracks inventory through time and raises validation errors when storage capacity, injection/withdrawal rates, or available inventory constraints are breached.

## Methodology

### Credit risk

The credit-risk workflow is:

```text
Customer loan data
        ↓
Train/test split
        ↓
Random Forest classifier
        ↓
Probability of Default (PD)
        ↓
LGD from recovery assumption
        ↓
Expected Loss = PD × LGD × EAD
```

### Rating segmentation

```text
FICO scores + default observations
              ↓
       Sort by FICO score
              ↓
 Dynamic-programming optimisation
              ↓
       Initial score bands
              ↓
 Minimum-size / monotonicity controls
              ↓
       Final rating map
```

### Commodity modelling and valuation

```text
Historical natural-gas prices
              ↓
 Trend + seasonal curve fitting
              ↓
       Price estimates
              ↓
 Storage injection / withdrawal events
              ↓
 Inventory and capacity constraints
              ↓
        Contract value
```

## Repository Structure

```text
J.P.-Morgan-Chase-Co-Quantitative-Research/
│
├── Customer_loan_data.csv
├── Nat_Gas.csv
│
├── expected loss function.py
├── rating map.py
├── optimised rating map.py
├── Data_Analysis_of_Natural_Gases_data.py
├── prototype pricing model.py
│
├── info
└── README.md
```

## Installation

### Requirements

The scripts use Python 3 and the following packages:

- `pandas`
- `numpy`
- `scikit-learn`
- `scipy`
- `matplotlib`

Install them with:

```bash
pip install pandas numpy scikit-learn scipy matplotlib
```

## Usage

Clone the repository:

```bash
git clone https://github.com/inikaprakash/J.P.-Morgan-Chase-Co-Quantitative-Research.git
cd J.P.-Morgan-Chase-Co-Quantitative-Research
```

Run the individual models from the repository root:

```bash
python "expected loss function.py"
python "rating map.py"
python "optimised rating map.py"
python "Data_Analysis_of_Natural_Gases_data.py"
python "prototype pricing model.py"
```

The natural-gas analysis script should be run before the prototype pricing model when working interactively, because the pricing model imports the `estimate_price()` function from that module.

## Key Quantitative Concepts

| Area | Techniques / Concepts |
|---|---|
| Credit Risk | Probability of Default, LGD, EAD, Expected Loss |
| Machine Learning | Random Forest, train/test split, ROC-AUC, probability estimation |
| Credit Ratings | FICO segmentation, dynamic programming, likelihood maximisation, monotonicity |
| Commodity Markets | Natural-gas price modelling, seasonality, forecasting |
| Time Series | Trend estimation, periodic components, out-of-sample projection |
| Derivatives / Valuation | Storage economics, inventory constraints, transaction costs |
| Numerical Methods | Curve fitting, optimisation, statistical error metrics |

## Limitations

These implementations are designed to demonstrate quantitative techniques rather than provide production-ready financial models. In particular:

- The credit model uses a single train/test split and does not include calibration, cross-validation, feature engineering, or model governance.
- Expected loss uses a simplified recovery-rate assumption and treats loan amount as EAD.
- The rating optimisation is based on observed FICO/default relationships and does not address scorecard calibration or regulatory rating requirements.
- The natural-gas model uses a simple deterministic trend-plus-seasonality specification; it does not model stochastic volatility, regime changes, convenience yield, or the full forward curve.
- The storage valuation is a simplified event-driven model rather than a complete stochastic real-options framework.

Real-world financial models require robust data, calibration, validation, sensitivity analysis, stress testing, documentation, governance, and independent model review.

## Author

**Nik Prakash**  
GitHub: [@nik251](https://github.com/nik251)

## Contributing

Suggestions and improvements are welcome. Fork the repository, make your changes, and submit a pull request with a clear description of the methodology and validation performed.

## License

No specific open-source license is currently provided. Unless a license is added to the repository, the contents should be treated as **all rights reserved** by the repository owner.
