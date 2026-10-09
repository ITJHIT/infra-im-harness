"""1MW ground-mount solar — independent re-computation for model-audit.

Reads nothing but the assumption block below (mirrors assumptions.md).
The Excel model is built by hand; this script exists only to check it.

    python model_check.py
"""

BASE = dict(
    capacity_kw=1_000,
    capacity_factor=0.154,      # KEEI 24-22, Table 5-1
    degradation=0.0045,         # KEEI 24-22, Table 5-1
    price_krw_kwh=140.0,        # assumption (2026 round-1 cap 147.686)
    capex_krw_kw=1_281_000,     # KEEI 24-22, Table 5-1 (2024)
    om_krw_kw_yr=21_198,        # KEEI 24-22, Table 5-1
    land_krw_kw_yr=13_261,      # KEEI 24-22, Table 5-1
    cost_inflation=0.0185,      # KEEI 24-22, Table 5-1
    debt_ratio=0.80,            # KEEI 24-22, Table 5-1
    rate=0.05,                  # KEEI 24-22, Table 5-1
    tenor=15,                   # bank product: up to 15y
    amortization="principal",   # bank product: equal principal only
    tax_rate=0.099,             # 9% bracket + local income tax
    life=20,                    # KEEI 24-22, Table 5-1
    curtailment=0.0,
)


def irr(cashflows, lo=-0.9, hi=1.0):
    for _ in range(200):
        mid = (lo + hi) / 2
        npv = sum(cf / (1 + mid) ** t for t, cf in enumerate(cashflows))
        lo, hi = (mid, hi) if npv > 0 else (lo, mid)
    return mid


def run(**overrides):
    a = {**BASE, **overrides}
    kw = a["capacity_kw"]
    capex = a["capex_krw_kw"] * kw
    debt = capex * a["debt_ratio"]
    equity = capex - debt
    depreciation = capex / a["life"]
    annuity = debt * a["rate"] / (1 - (1 + a["rate"]) ** -a["tenor"])

    balance = debt
    project_cf, equity_cf, dscr = [-capex], [-equity], []
    for t in range(1, a["life"] + 1):
        gen_kwh = kw * 8_760 * a["capacity_factor"] * (1 - a["degradation"]) ** (t - 1) * (1 - a["curtailment"])
        opex = (a["om_krw_kw_yr"] + a["land_krw_kw_yr"]) * kw * (1 + a["cost_inflation"]) ** (t - 1)
        ebitda = gen_kwh * a["price_krw_kwh"] - opex

        if t <= a["tenor"]:
            interest = balance * a["rate"]  # opening balance
            principal = debt / a["tenor"] if a["amortization"] == "principal" else annuity - interest
        else:
            interest = principal = 0.0
        balance -= principal

        tax_levered = max(0.0, (ebitda - depreciation - interest) * a["tax_rate"])
        tax_unlevered = max(0.0, (ebitda - depreciation) * a["tax_rate"])
        cfads = ebitda - tax_levered

        project_cf.append(ebitda - tax_unlevered)
        equity_cf.append(cfads - interest - principal)
        if t <= a["tenor"] and debt > 0:
            dscr.append(cfads / (interest + principal))

    worst = min(dscr) if dscr else float("nan")
    return {
        "project_irr": irr(project_cf),
        "equity_irr": irr(equity_cf),
        "min_dscr": worst,
        "min_dscr_year": dscr.index(worst) + 1 if dscr else 0,
        "avg_dscr": sum(dscr) / len(dscr) if dscr else float("nan"),
    }


CASES = [
    ("base (15y equal principal)", {}),
    ("15y annuity", {"amortization": "annuity"}),
    ("20y equal principal", {"tenor": 20}),
    ("capacity factor 14.4%", {"capacity_factor": 0.144}),
    ("capacity factor 14.0%", {"capacity_factor": 0.140}),
    ("curtailment 5%", {"curtailment": 0.05}),
    ("curtailment 10%", {"curtailment": 0.10}),
    ("price 133", {"price_krw_kwh": 133.0}),
    ("rate 6%", {"rate": 0.06}),
    ("rate 7.088% (product cap)", {"rate": 0.07088}),
    ("capex 2023 (1,416)", {"capex_krw_kw": 1_416_000}),
    ("no land lease", {"land_krw_kw_yr": 0}),
    ("downside: rate 6% + curtail 5% + CF 14.9%", {"rate": 0.06, "curtailment": 0.05, "capacity_factor": 0.149}),
    ("sanity: no debt (equity IRR == project IRR)", {"debt_ratio": 0.0}),
]

if __name__ == "__main__":
    print(f"{'case':46s} {'proj IRR':>9s} {'eq IRR':>8s} {'min DSCR':>9s} {'yr':>3s} {'avg':>5s}")
    for name, kw in CASES:
        r = run(**kw)
        dscr = f"{r['min_dscr']:9.2f} {r['min_dscr_year']:3d} {r['avg_dscr']:5.2f}" if kw.get("debt_ratio", 1) else f"{'-':>9s} {'-':>3s} {'-':>5s}"
        print(f"{name:46s} {r['project_irr']*100:8.1f}% {r['equity_irr']*100:7.1f}% {dscr}")
