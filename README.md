# J.P.-Morgan-Chase-Co-Quantitative-Research

A collection of quantitative finance projects developed around key problems in **credit risk, natural gas price modelling, financial forecasting, and quantitative pricing**.

This repository contains Python implementations and supporting datasets covering several areas of quantitative research, including **expected loss estimation, credit rating optimisation, commodity price analysis, and prototype pricing models**.

## 📌 Projects

### 1. Expected Loss Function

**File:** `expected loss function.py`

Implements an expected-loss framework for credit risk analysis.

The model is based on the fundamental relationship:

[
\text{Expected Loss} = PD \times LGD \times EAD
]

where:

* **PD** — Probability of Default
* **LGD** — Loss Given Default
* **EAD** — Exposure at Default

The implementation demonstrates how these parameters can be used to estimate potential credit losses.

---

### 2. Rating Map

**File:** `rating map.py`

Explores the mapping between credit ratings and quantitative risk characteristics.

Credit ratings provide an important mechanism for categorising borrowers according to their estimated probability of default. This project provides a programmatic representation of rating categories that can be incorporated into quantitative credit models.

---

### 3. Optimised Rating Map

**File:** `optimised rating map.py`

Extends the rating-mapping approach by introducing an optimisation component.

The objective is to create a more systematic relationship between quantitative risk measures and rating categories, providing a foundation for improved credit-risk classification.

---

### 4. Prototype Pricing Model

**File:** `prototype pricing model.py`

Contains a prototype quantitative pricing model.

The project demonstrates how financial inputs can be transformed into a model-driven pricing framework and serves as a starting point for more sophisticated financial modelling techniques.

---

### 5. Natural Gas Data Analysis

**File:** `Data_Analysis_of_Natural_Gases_data.py`

**Dataset:** `Nat_Gas.csv`

Analyses historical natural gas data to identify trends and patterns in commodity prices.

The analysis provides a foundation for understanding:

* Historical price behaviour
* Time-series trends
* Seasonal effects
* Price movements
* Forecasting and modelling opportunities

The dataset is used directly by the Python analysis script.

---

### 6. Customer Loan Data

**Dataset:** `Customer_loan_data.csv`

Contains customer-level loan information intended for quantitative credit-risk analysis.

The dataset can be used to investigate relationships between customer characteristics, lending decisions, and potential credit losses.

## 🗂️ Repository Structure

```text
J.P.-Morgan-Chase-Co-Quantitative-Research/
│
├── Customer_loan_data.csv
├── Data_Analysis_of_Natural_Gases_data.py
├── Nat_Gas.csv
├── expected loss function.py
├── optimised rating map.py
├── prototype pricing model.py
├── rating map.py
├── info
└── README.md
```

## 🛠️ Technologies

* **Python 3**
* **Pandas** — data manipulation and analysis
* **NumPy** — numerical computation
* **Matplotlib** — data visualisation
* **Statistical / quantitative modelling**
* **Financial mathematics**
* **Credit risk modelling**
* **Time-series analysis**

## 🚀 Getting Started

### Clone the repository

```bash
git clone https://github.com/inikaprakash/J.P.-Morgan-Chase-Co-Quantitative-Research.git
cd J.P.-Morgan-Chase-Co-Quantitative-Research
```

### Install dependencies

If a `requirements.txt` file is not provided, install the commonly used Python packages:

```bash
pip install numpy pandas matplotlib
```

### Run the projects

For example:

```bash
python "Data_Analysis_of_Natural_Gases_data.py"
```

Other models can be executed using:

```bash
python "expected loss function.py"
python "rating map.py"
python "optimised rating map.py"
python "prototype pricing model.py"
```

## 📊 Quantitative Finance Concepts

The repository brings together several important quantitative-finance concepts:

| Area                | Concepts                                           |
| ------------------- | -------------------------------------------------- |
| Credit Risk         | PD, LGD, EAD, Expected Loss                        |
| Credit Ratings      | Risk classification, rating mapping                |
| Commodity Markets   | Natural gas prices, time-series analysis           |
| Financial Modelling | Quantitative pricing, model prototyping            |
| Data Analysis       | Data cleaning, statistical analysis, visualisation |
| Risk Management     | Credit exposure and loss estimation                |

## 🎯 Objectives

The main objectives of this repository are to:

1. Apply quantitative methods to financial datasets.
2. Develop practical credit-risk modelling techniques.
3. Analyse commodity-market data.
4. Explore relationships between credit ratings and financial risk.
5. Build prototype financial pricing models.
6. Demonstrate the application of Python to quantitative finance.

## 📚 Disclaimer

This repository is intended for **educational, research, and portfolio purposes**.

The models are prototypes and should not be considered production-ready financial, investment, credit, or risk-management systems. Real-world financial models require rigorous validation, calibration, stress testing, governance, and appropriate market and institutional data.

## 👤 Author

**Nik Prakash**

GitHub: [@nik251](https://github.com/nik251)

## ⭐ Contributing

Contributions, suggestions, and improvements are welcome. Feel free to fork the repository, experiment with the models, and submit a pull request.

## 📄 License

No specific license is currently provided. Unless otherwise stated, the contents of this repository should be treated as **all rights reserved** by the repository owner.
