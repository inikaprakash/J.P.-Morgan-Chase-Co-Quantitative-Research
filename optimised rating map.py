import pandas as pd
import numpy as np
import math
import time

start_time = time.time()

df = pd.read_csv("Customer_loan_data.csv")

df = df.sort_values("fico_score").reset_index(drop=True)

fico = df["fico_score"].values
defaults = df["default"].values

n = len(df)

minimum_bucket_size = int(n * 0.05)


def calculate_log_likelihood(start, end):

    count = end - start + 1

    if count < minimum_bucket_size:
        return -np.inf

    default_count = defaults[start:end + 1].sum()

    p = default_count / count
    p = min(max(p, 1e-10), 1 - 1e-10)

    return (
        default_count * math.log(p)
        + (count - default_count) * math.log(1 - p)
    )


likelihood = np.full((n, n), -np.inf)

for i in range(n):
    for j in range(i, n):
        likelihood[i][j] = calculate_log_likelihood(i, j)


def optimise_buckets(number_of_buckets):

    dp = np.full(
        (number_of_buckets + 1, n),
        -np.inf
    )

    split_points = np.zeros(
        (number_of_buckets + 1, n),
        dtype=int
    )

    for i in range(n):
        dp[1][i] = likelihood[0][i]

    for bucket in range(2, number_of_buckets + 1):

        for end in range(n):

            if end < bucket - 1:
                continue

            best_score = -np.inf
            best_split = 0

            for split in range(bucket - 2, end):

                score = (
                    dp[bucket - 1][split]
                    +
                    likelihood[split + 1][end]
                )

                if score > best_score:
                    best_score = score
                    best_split = split

            dp[bucket][end] = best_score
            split_points[bucket][end] = best_split

    boundaries = []

    index = n - 1

    for bucket in range(number_of_buckets, 1, -1):

        index = split_points[bucket][index]
        boundaries.append(index)

    return sorted(boundaries)


number_of_buckets = 10

boundaries = optimise_buckets(number_of_buckets)


ratings = []

start = 0

for rating, end in enumerate(boundaries + [n - 1], 1):

    bucket = df.iloc[start:end + 1]

    ratings.append(
        {
            "rating": rating,
            "min_fico": int(bucket.fico_score.min()),
            "max_fico": int(bucket.fico_score.max()),
            "customers": len(bucket),
            "defaults": int(bucket.default.sum()),
            "PD": bucket.default.mean()
        }
    )

    start = end + 1


rating_map = pd.DataFrame(ratings)


while True:

    changed = False

    for i in range(len(rating_map) - 1):

        if rating_map.loc[i, "PD"] < rating_map.loc[i + 1, "PD"]:

            rating_map.loc[i, "max_fico"] = (
                rating_map.loc[i + 1, "max_fico"]
            )

            rating_map.loc[i, "customers"] += (
                rating_map.loc[i + 1, "customers"]
            )

            rating_map.loc[i, "defaults"] += (
                rating_map.loc[i + 1, "defaults"]
            )

            rating_map.loc[i, "PD"] = (
                rating_map.loc[i, "defaults"]
                /
                rating_map.loc[i, "customers"]
            )

            rating_map = (
                rating_map
                .drop(i + 1)
                .reset_index(drop=True)
            )

            changed = True
            break

    if not changed:
        break


rating_map["rating"] = range(1, len(rating_map) + 1)

rating_map["PD"] = rating_map["PD"].round(6)

print("FICO Rating Map\n")
print(rating_map)


def fico_to_rating(fico_score):

    result = rating_map[
        (rating_map["min_fico"] <= fico_score)
        &
        (rating_map["max_fico"] >= fico_score)
    ]

    if result.empty:
        return None

    return {
        "rating": int(result.iloc[0]["rating"]),
        "PD": float(result.iloc[0]["PD"])
    }


print("\nExamples")
print("FICO 720:", fico_to_rating(720))
print("FICO 580:", fico_to_rating(580))
print("FICO 800:", fico_to_rating(800))

print(
    "\nRuntime:",
    round(time.time() - start_time, 2),
    "seconds"
)