import math


def get_user_input(text):
    while True:
        try:
            user_input = float(input(f"Enter {text}: "))
        except ValueError as e:
            print(f"{e}: Only numbers (integers and floats) are allowed as input.")
            continue
        if text != 'ASIC price in €' and user_input <= 0:
            print('ASIC operational cost and revenue cannot be zero or negative.')
            continue
        if text == 'ASIC price in €' and user_input < 0:
            print('ASIC price cannot be less than zero.')
            continue
        return user_input


ASIC_price = get_user_input('ASIC price in €')
ASIC_yearly_cost = 12 * get_user_input('monthly cost of ASIC in €/month')
ASIC_yearly_revenue = 12 * get_user_input('ASIC revenue in €/month')


current_price = get_user_input('Bitcoin Price in USD/BTC')
# TODO: The script should get the price online.

if ASIC_yearly_cost >= ASIC_yearly_revenue:
    print('This ASIC may never be profitable')
    exit()

j = round(-math.log(2)/2, 3)

k = 100*j  # This defines the range of the brute force loop (line 43)
# TODO: Find better way then brute forcing the calculation.

a, b = 0, 1

while a < b:
    k = round(k, 3) + 0.001

    if k == -j:
        print('This miner is only profitable if the bitcoin price rises faster than the hashrate')
        exit()
    # TODO: Better error handling.

    end_of_miner_profitability = round(
        (math.log(ASIC_yearly_revenue) - math.log(ASIC_yearly_cost))
        / (-j - k), 3)

    a = math.expm1(j * end_of_miner_profitability) * ASIC_yearly_revenue / j

    b = (ASIC_yearly_cost * end_of_miner_profitability) + ASIC_price


growth_ratio = round(math.exp(-j-k), 2)
estimated_price = current_price * math.exp(k)
estimated_price = float(estimated_price)
bitcoin_mined = a/current_price

print(
    f'For this ASIC, the hashrate may rise no more then {growth_ratio} as fast as the bitcoin price.')
print(
    f"Mining with this ASIC would still be profitable if the Bitcoin price would equal to {estimated_price:.2f} USD in 1 year."
)
print(
    f'This ASIC would run for {end_of_miner_profitability:.1f} years and would generate ~ {bitcoin_mined:.3f} bitcoin worth at least {a:.2f} €.')
