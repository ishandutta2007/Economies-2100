import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. Baseline 2026 Data (IMF WEO Oct 2026) & Structural Solow Parameters
# Steady_GDP_pc = Structural frontier (2026 USD)
# Conv_Rate = Annual convergence speed (lambda)
countries_data = [
    {"Country": "United States", "GDP_pc_2026": 95210, "Steady_GDP_pc": 380000, "Conv_Rate": 0.018},
    {"Country": "Japan", "GDP_pc_2026": 35400, "Steady_GDP_pc": 310000, "Conv_Rate": 0.016},
    {"Country": "Russia", "GDP_pc_2026": 19950, "Steady_GDP_pc": 210000, "Conv_Rate": 0.014},
    {"Country": "Mexico", "GDP_pc_2026": 16190, "Steady_GDP_pc": 220000, "Conv_Rate": 0.016},
    {"Country": "China", "GDP_pc_2026": 15370, "Steady_GDP_pc": 265000, "Conv_Rate": 0.022},
    {"Country": "Brazil", "GDP_pc_2026": 12400, "Steady_GDP_pc": 205000, "Conv_Rate": 0.015},
    {"Country": "Vietnam", "GDP_pc_2026": 5260, "Steady_GDP_pc": 225000, "Conv_Rate": 0.024},
    {"Country": "Indonesia", "GDP_pc_2026": 5150, "Steady_GDP_pc": 215000, "Conv_Rate": 0.022},
    {"Country": "Philippines", "GDP_pc_2026": 4360, "Steady_GDP_pc": 195000, "Conv_Rate": 0.021},
    {"Country": "Egypt", "GDP_pc_2026": 4020, "Steady_GDP_pc": 175000, "Conv_Rate": 0.019},
    {"Country": "Bangladesh", "GDP_pc_2026": 2890, "Steady_GDP_pc": 170000, "Conv_Rate": 0.021},
    {"Country": "India", "GDP_pc_2026": 2750, "Steady_GDP_pc": 210000, "Conv_Rate": 0.025},
    {"Country": "Pakistan", "GDP_pc_2026": 1840, "Steady_GDP_pc": 140000, "Conv_Rate": 0.016},
    {"Country": "Nigeria", "GDP_pc_2026": 1590, "Steady_GDP_pc": 145000, "Conv_Rate": 0.018},
    {"Country": "Ethiopia", "GDP_pc_2026": 1130, "Steady_GDP_pc": 135000, "Conv_Rate": 0.020},
    {"Country": "DR Congo", "GDP_pc_2026": 1110, "Steady_GDP_pc": 125000, "Conv_Rate": 0.017},
]

df = pd.DataFrame(countries_data)
years = np.arange(2026, 2101)
t = years - 2026

# 2. Simulate Conditional Solow Convergence
projections = pd.DataFrame({"Year": years})
for _, row in df.iterrows():
    y0 = row["GDP_pc_2026"]
    ystar = row["Steady_GDP_pc"]
    lam = row["Conv_Rate"]
    ln_yt = (1 - np.exp(-lam * t)) * np.log(ystar) + np.exp(-lam * t) * np.log(y0)
    projections[row["Country"]] = np.exp(ln_yt)

# 3. Plot Trajectories with Critical Year Annotations
fig, ax = plt.subplots(figsize=(14, 8.5))
colors = plt.cm.tab20(np.linspace(0, 1, len(df)))

# Sort legend by 2100 projected GDP per capita
sorted_countries = projections.iloc[-1, 1:].sort_values(ascending=False).index
highlight_countries = ["United States", "Japan", "China", "India", "DR Congo"]

for idx, country in enumerate(sorted_countries):
    val_2100 = projections[country].iloc[-1]
    is_highlighted = country in highlight_countries
    ax.plot(
        projections["Year"],
        projections[country] / 1000,
        label=f"{country} (${val_2100/1000:,.1f}k)",
        linewidth=2.5 if is_highlighted else 1.3,
        alpha=1.0 if is_highlighted else 0.75,
        color=colors[idx],
    )

# 4. Annotate Critical Years (2026 Baseline, 2050 Mid-Century, 2075 Third-Quarter, 2100 Horizon)
critical_years = [2026, 2050, 2075, 2100]
for yr in critical_years:
    ax.axvline(x=yr, color="gray", linestyle=":", linewidth=1.2, alpha=0.8)
    ax.text(
        yr,
        272,
        f"{yr}\nMilestone",
        ha="center",
        va="bottom",
        fontsize=9,
        fontweight="bold",
        color="#333333",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="#f4f4f4", edgecolor="#cccccc", alpha=0.9),
    )

# Highlight specific data points at critical years for key economies
annotations = [
    ("United States", 2026, (8, -4)),
    ("United States", 2050, (-12, 10)),
    ("United States", 2075, (-12, 10)),
    ("United States", 2100, (-45, 8)),
    ("Japan", 2100, (-45, 6)),
    ("China", 2050, (-10, 10)),
    ("China", 2100, (-45, -14)),
    ("India", 2050, (6, -12)),
    ("India", 2075, (6, -10)),
    ("India", 2100, (-45, -12)),
    ("DR Congo", 2100, (-45, -12)),
]

for country, yr, offset in annotations:
    val_k = projections.loc[projections["Year"] == yr, country].values[0] / 1000
    ax.scatter(yr, val_k, color="black", zorder=5, s=28)
    ax.annotate(
        f"{country.split()[0]} ${val_k:,.1f}k",
        xy=(yr, val_k),
        xytext=offset,
        textcoords="offset points",
        fontsize=8.5,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="gray", alpha=0.85),
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.1", color="gray", lw=0.8),
    )

ax.set_title(
    "Projected GDP per Capita (2026–2100): Economies with >100M Population",
    fontsize=14,
    fontweight="bold",
    pad=28,
)
ax.set_xlabel("Year", fontsize=12, fontweight="bold")
ax.set_ylabel("GDP per Capita (Thousands of Constant 2026 USD)", fontsize=12, fontweight="bold")
ax.set_xlim(2024, 2103)
ax.set_ylim(0, 290)
ax.grid(True, linestyle="--", alpha=0.45)
ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=9.5, title="2100 Projected Ranking")

plt.tight_layout()
plt.savefig("gdp_per_capita_2100_annotated.png", dpi=300)
plt.show()
