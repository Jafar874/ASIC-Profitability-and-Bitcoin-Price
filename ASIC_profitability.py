import math


def get_user_input(text):
    while True:
        try:
            user_input = float(input(f"Enter {text}: "))
        except ValueError as e:
            print(f"{e}: Only numbers (integers and floats) are allowed as input")
            continue
        return user_input


ASIC_price = get_user_input("ASIC price in €")
ASIC_yearly_cost = 12 * get_user_input("monthly cost of ASIC in €/month")
ASIC_yearly_revenue = 12 * get_user_input("ASIC revenue in €/month")

j = round(-math.log(2) / 2, 3)
k = -j
a, b = 0, 1

# TODO: find more expressive names for variables
while a < b:
    k = round(k, 3) - 0.001
    end_of_miner_profitability = (
        math.log(ASIC_yearly_revenue) - math.log(ASIC_yearly_cost)
    ) / (-j - k)
    end_of_miner_profitability = round(end_of_miner_profitability, 3)
    a = (1 - math.exp(j * end_of_miner_profitability)) * ASIC_yearly_revenue / -j
    b = (ASIC_yearly_cost * end_of_miner_profitability) + ASIC_price

print(f"Bitcoin's growth coefficient may be no lower than {k:.3f}")

current_price = get_user_input("Bitcoin Price in USD/BTC")
# TODO: The script should get the price online.
estimated_price = current_price * math.exp(k)
estimated_price = float(estimated_price)

print(
    f"The Bitcoin price in 1 year is estimated to be at least {estimated_price:.2f} USD."
)

# TODO: fix overflow error!!!
