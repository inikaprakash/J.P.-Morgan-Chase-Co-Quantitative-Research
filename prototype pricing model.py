import pandas as pd
from Data_Analysis_of_Natural_Gases_data import estimate_price


def price_storage_contract(
    injection_dates,
    withdrawal_dates,
    injection_withdrawal_cost_rate,
    volume_per_transaction,
    max_storage_volume,
    injection_rate,
    withdrawal_rate,
    storage_cost_per_month
):
    inventory = 0
    contract_value = 0

    events = []

    for date in injection_dates:
        events.append((pd.to_datetime(date), "inject"))

    for date in withdrawal_dates:
        events.append((pd.to_datetime(date), "withdraw"))

    events.sort(key=lambda x: x[0])

    first_injection = min(pd.to_datetime(d) for d in injection_dates)
    last_withdrawal = max(pd.to_datetime(d) for d in withdrawal_dates)

    for date, action in events:
        if action == "inject":
            if volume_per_transaction > injection_rate:
                raise ValueError(f"Injection rate exceeded on {date.date()}")

            if inventory + volume_per_transaction > max_storage_volume:
                raise ValueError("Maximum storage capacity exceeded.")

            purchase_price = estimate_price(date.strftime("%Y-%m-%d"))

            contract_value -= (
                purchase_price * volume_per_transaction
                + volume_per_transaction * injection_withdrawal_cost_rate
            )

            inventory += volume_per_transaction

            print(
                f"{date.date()} | Injected {volume_per_transaction:,} MMBtu "
                f"@ ${purchase_price:.2f}"
            )

        else:
            if volume_per_transaction > withdrawal_rate:
                raise ValueError(f"Withdrawal rate exceeded on {date.date()}")

            if inventory < volume_per_transaction:
                raise ValueError("Insufficient gas in storage.")

            sale_price = estimate_price(date.strftime("%Y-%m-%d"))

            contract_value += (
                sale_price * volume_per_transaction
                - volume_per_transaction * injection_withdrawal_cost_rate
            )

            inventory -= volume_per_transaction

            print(
                f"{date.date()} | Withdrew {volume_per_transaction:,} MMBtu "
                f"@ ${sale_price:.2f}"
            )

    storage_months = (
        (last_withdrawal.year - first_injection.year) * 12
        + (last_withdrawal.month - first_injection.month)
    )

    contract_value -= storage_months * storage_cost_per_month

    return round(contract_value, 2)


value = price_storage_contract(
    injection_dates=[
        "2024-05-31",
        "2024-06-30"
    ],
    withdrawal_dates=[
        "2024-12-31",
        "2025-01-31"
    ],
    injection_withdrawal_cost_rate=0.02,
    volume_per_transaction=100000,
    max_storage_volume=500000,
    injection_rate=150000,
    withdrawal_rate=150000,
    storage_cost_per_month=10000
)

print(f"Contract Value: ${value:,.2f}")