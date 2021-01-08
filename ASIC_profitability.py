import math
from typing import List

from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
import numpy as np


def get_user_input(text: str) -> float:
    while True:
        try:
            user_input = float(input(f"Enter {text}: "))
        except ValueError as e:
            print(f"{e}: Only numbers (integers and floats) are allowed as input")
            continue
        return user_input


def calculate_stuff(
    ASIC_price: float,
    ASIC_yearly_cost: float,
    ASIC_yearly_revenue: float,
    num_iters: int = 1000,
) -> List[float]:
    # TODO: find more expressive names for variables
    j = round(-math.log(2) / 2, 3)
    k = -j
    a, b = 0, 1
    eom_profitability = list()

    for i in range(num_iters):
        k = round(k, 3) - 0.001
        end_of_miner_profitability = (
            math.log(ASIC_yearly_revenue) - math.log(ASIC_yearly_cost)
        ) / (-j - k)
        end_of_miner_profitability = round(end_of_miner_profitability, 3)
        a = (1 - math.exp(j * end_of_miner_profitability)) * ASIC_yearly_revenue / -j
        b = (ASIC_yearly_cost * end_of_miner_profitability) + ASIC_price
        eom_profitability.append(end_of_miner_profitability)
        if a >= b:
            break
    return eom_profitability, k


ASIC_price = get_user_input("ASIC price in €")
ASIC_yearly_cost = 12 * get_user_input("monthly cost of ASIC in €/month")
ASIC_yearly_revenue = 12 * get_user_input("ASIC revenue in €/month")
current_price = get_user_input("Bitcoin Price in USD/BTC")

num_iters = 1000

# plotting preliminaries
fig = plt.figure(figsize=(6, 8.5))
ax = fig.add_subplot(111)
ax.set_xlim([-1, num_iters])
ax.set_ylim([-50, 50])
fig.subplots_adjust(bottom=0.1, top=0.80)

# Create axes for sliders
ax_asic_price = fig.add_axes([0.3, 0.89, 0.4, 0.02])
ax_asic_price.spines["top"].set_visible(True)
ax_asic_price.spines["right"].set_visible(True)

ax_asic_yearly_cost = fig.add_axes([0.3, 0.92, 0.4, 0.02])
ax_asic_yearly_cost.spines["top"].set_visible(True)
ax_asic_yearly_cost.spines["right"].set_visible(True)

ax_asic_yearly_revenue = fig.add_axes([0.3, 0.95, 0.4, 0.02])
ax_asic_yearly_revenue.spines["top"].set_visible(True)
ax_asic_yearly_revenue.spines["right"].set_visible(True)

# Create sliders
s_ap = Slider(
    ax=ax_asic_price,
    label="ASIC price",
    valmin=0.0,
    valmax=10000.0,
    valinit=ASIC_price,
    valfmt=" %1.2f USD",
    facecolor="#00a1c6",
)
s_ayc = Slider(
    ax=ax_asic_yearly_cost,
    label="ASIC yearly cost ",
    valmin=1.0,
    valmax=5000.0,
    valinit=ASIC_yearly_cost,
    valfmt=" %1.2f USD",
    facecolor="#00a1c6",
)
s_ayr = Slider(
    ax=ax_asic_yearly_revenue,
    label="ASIC yearly revenue ",
    valmin=1.0,
    valmax=5000.0,
    valinit=ASIC_yearly_revenue,
    valfmt=" %1.2f USD",
    facecolor="#00a1c6",
)


def update(_):
    eom_profitability, k = calculate_stuff(s_ap.val, s_ayc.val, s_ayr.val)
    f_d.set_data(list(range(len(eom_profitability))), eom_profitability)
    fig.canvas.draw_idle()
    estimated_price = current_price * math.exp(k)
    text.set_text(f"Estimated BTC price: {estimated_price:.2f}")


# Plot default data
x = np.arange(num_iters)
eom_profitability, k = calculate_stuff(
    ASIC_price, ASIC_yearly_cost, ASIC_yearly_revenue
)
(f_d,) = ax.plot(list(range(len(eom_profitability))), eom_profitability, linewidth=2.5)
estimated_price = current_price * math.exp(k)
text = ax.text(0.1, -2, f"Estimated BTC price: {estimated_price:.2f}", fontsize=12)


s_ap.on_changed(update)
s_ayc.on_changed(update)
s_ayr.on_changed(update)

ax.set_xlabel("Iteration")
ax.set_ylabel("End of mining profitability")
plt.show()
