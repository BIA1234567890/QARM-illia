from engine import PortfolioConfig, load_all_data, run_backtest, run_today_optimization
import pandas as pd

data = load_all_data()

config = PortfolioConfig(
    today_date=pd.Timestamp("2025-10-01"),
    investment_horizon_years=1,
    est_months=12,
    rebalancing=12,
    gamma=2.0,
    universe_choice="SP500",
    keep_sectors=None,
    keep_esg=None,
    selected_asset_classes_other=None,
    keep_ids_by_class=None,
    max_weight_per_asset=0.05,
    sector_constraints=None
    # {
    #     "Technology": {"max": 0.1},
    #     "Utilities": {"min": 0.1, "max": 0.25},
    # }
    ,
    esg_constraints={
        "H": {"min": 0.20},
        "L": {"max": 0.10},
    },
    asset_class_constraints={
        "Equity": {"min": 0.7},
        "Commodities": {"max": 0.20},
        "Fixed Income": {"max": 0.20},
    },
)

perf, summary_df, debug_weights_df = run_backtest(config, data)

# Backtest results
perf, summary_df, debug_weights_df = run_backtest(config, data)

# Today's portfolio
today_res = run_today_optimization(config, data)
print(today_res)

today_df = today_res["weights"]
top5_today = today_res["top5"]
alloc_by_ac = today_res["alloc_by_asset_class"]

print("Top 5 positions:\n", top5_today)
print("\nAllocation by asset class:\n", alloc_by_ac)

# If you want, you can still write to Excel:
today_df.to_excel("today_portfolio_weights.xlsx", index=False)
