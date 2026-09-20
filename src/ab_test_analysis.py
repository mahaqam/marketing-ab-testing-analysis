"""Statistical analysis of the public Marketing A/B Testing dataset."""
from pathlib import Path
import argparse, math
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm


def load_data(path):
    df = pd.read_csv(path)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    required = {"user_id", "test_group", "converted", "total_ads", "most_ads_day", "most_ads_hour"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing expected columns: {sorted(missing)}")

    if df["converted"].dtype != bool:
        df["converted"] = df["converted"].astype(str).str.lower().map(
            {"true": 1, "false": 0, "1": 1, "0": 0}
        )
    else:
        df["converted"] = df["converted"].astype(int)

    if df["converted"].isna().any():
        raise ValueError("Unexpected converted values")
    return df


def summary(df):
    return (
        df.groupby("test_group")["converted"]
        .agg(users="size", conversions="sum", conversion_rate="mean")
        .reset_index()
    )


def test(df):
    s = summary(df).set_index("test_group")
    if not {"ad", "psa"}.issubset(s.index):
        raise ValueError("Expected groups 'ad' and 'psa'")

    nt, nc = int(s.loc["ad", "users"]), int(s.loc["psa", "users"])
    xt, xc = int(s.loc["ad", "conversions"]), int(s.loc["psa", "conversions"])
    pt, pc = xt / nt, xc / nc
    diff = pt - pc

    pooled = (xt + xc) / (nt + nc)
    se0 = math.sqrt(pooled * (1 - pooled) * (1 / nt + 1 / nc))
    z = diff / se0 if se0 else 0
    p = 2 * norm.sf(abs(z))

    se = math.sqrt(pt * (1 - pt) / nt + pc * (1 - pc) / nc)
    return {
        "treatment_rate": pt,
        "control_rate": pc,
        "absolute_uplift": diff,
        "relative_uplift": diff / pc if pc else float("nan"),
        "z_statistic": z,
        "p_value": p,
        "ci_95_low": diff - 1.96 * se,
        "ci_95_high": diff + 1.96 * se,
    }


def segments(df, col):
    return (
        df.groupby([col, "test_group"])["converted"]
        .agg(users="size", conversions="sum", conversion_rate="mean")
        .reset_index()
    )


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", default="outputs")
    a = p.parse_args()

    out = Path(a.output)
    out.mkdir(parents=True, exist_ok=True)
    df = load_data(a.input)

    s = summary(df)
    s.to_csv(out / "group_summary.csv", index=False)
    result = pd.DataFrame([test(df)])
    result.to_csv(out / "test_results.csv", index=False)
    segments(df, "most_ads_day").to_csv(out / "conversion_by_day.csv", index=False)
    segments(df, "most_ads_hour").to_csv(out / "conversion_by_hour.csv", index=False)

    ax = s.plot.bar(
        x="test_group", y="conversion_rate", legend=False, title="Conversion rate by experiment group"
    )
    ax.set_ylabel("Conversion rate")
    plt.tight_layout()
    plt.savefig(out / "conversion_by_group.png", dpi=160)
    plt.close()

    print(s.to_string(index=False))
    print(result.to_string(index=False))


if __name__ == "__main__":
    main()
