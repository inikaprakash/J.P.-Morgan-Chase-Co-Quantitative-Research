import pandas as pd
import numpy as np
import math

df = pd.read_csv("Customer_loan_data.csv")

df = df.sort_values("fico_score").reset_index(drop=True)

fico = df["fico_score"].values
defaults = df["default"].values

n = len(df)


def bucket_log_likelihood(start, end):
    bucket_defaults = defaults[start:end + 1]
    count = len(bucket_defaults)

    default_count = bucket_defaults.sum()

    p = default_count / count

    if p == 0:
        p = 1e-10

    if p == 1:
        p = 1 - 1e-10

    return (
        default_count * math.log(p)
        + (count - default_count) * math.log(1 - p)
    )


def optimal_buckets(num_buckets):

    dp = np.full((num_buckets + 1, n), -np.inf)
    boundaries = np.zeros(
        (num_buckets + 1, n),
        dtype=int
    )

    for i in range(n):
        dp[1][i] = bucket_log_likelihood(0, i)


    for b in range(2, num_buckets + 1):

        for i in range(b - 1, n):

            best_score = -np.inf
            best_split = 0

            for j in range(b - 2, i):

                score = (
                    dp[b-1][j]
                    + bucket_log_likelihood(j+1, i)
                )

                if score > best_score:
                    best_score = score
                    best_split = j

            dp[b][i] = best_score
            boundaries[b][i] = best_split


    splits = []

    index = n - 1

    for b in range(num_buckets, 1, -1):

        split = boundaries[b][index]

        splits.append(split)

        index = split


    splits.reverse()

    return splits


num_buckets = 10

splits = optimal_buckets(num_buckets)


bucket_ranges = []

start = 0

for split in splits:

    bucket_ranges.append(
        (
            fico[start],
            fico[split]
        )
    )

    start = split + 1


bucket_ranges.append(
    (
        fico[start],
        fico[-1]
    )
)


rating_map = []

for rating, (low, high) in enumerate(bucket_ranges, 1):

    bucket = df[
        (df["fico_score"] >= low)
        &
        (df["fico_score"] <= high)
    ]

    rating_map.append(
        {
            "rating": rating,
            "min_fico": low,
            "max_fico": high,
            "borrowers": len(bucket),
            "defaults": bucket["default"].sum(),
            "PD": bucket["default"].mean()
        }
    )


rating_map = pd.DataFrame(rating_map)


print(rating_map)


def fico_rating(fico_score):

    row = rating_map[
        (rating_map["min_fico"] <= fico_score)
        &
        (rating_map["max_fico"] >= fico_score)
    ]

    if len(row) == 0:
        return None

    return {
        "rating": int(row.iloc[0]["rating"]),
        "PD": round(row.iloc[0]["PD"], 4)
    }


print(fico_rating(720))
print(fico_rating(580))