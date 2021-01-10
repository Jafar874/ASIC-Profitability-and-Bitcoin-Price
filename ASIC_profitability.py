import math


def get_user_input(text):
    while True:
        try:
            user_input = float(input(f"Enter {text}: "))
        except ValueError as e:
            print(f"{e}: Only numbers are allowed as input.")
            continue
        if text == 'ASIC price in €' and user_input < 0:
            print('ASIC prices cannot be negative.')
            continue
        if text != 'ASIC price in €' and user_input <= 0:
            print(
                'ASIC operational costs, ASIC revenues and Bitcoin Prices cannot be zero or negative.')
            continue
        return user_input


def get_time_interval(bitcoin_price_growth):
    time_interval = round(
        (math.log(ASIC_yearly_revenue) - math.log(ASIC_yearly_cost))
        / (network_hashrate_growth - bitcoin_price_growth), 3)
    return time_interval


def get_mining_reward(time_interval):
    mining_reward = math.expm1(
        - network_hashrate_growth * time_interval) * ASIC_yearly_revenue / - network_hashrate_growth
    return mining_reward


def get_buying_btc(time_interval):
    buying_btc = (
        ASIC_yearly_cost * time_interval) + ASIC_price
    return buying_btc


def get_fair_price():
    print()
    current_price = get_user_input('Bitcoin Price in USD/BTC')
    # TODO: The script should get the price online.

    time_interval = 2  # Assuming 2 years of ASIC operation
    mining_reward = get_mining_reward(time_interval)
    buying_btc = get_buying_btc(time_interval)
    fair_price = buying_btc / mining_reward * current_price
    print(
        f'The fair bitcoin price is estimated to be {fair_price:.2f} USD/BTC')
    exit()


ASIC_price = get_user_input('ASIC price in €')
ASIC_yearly_cost = 12 * get_user_input('monthly cost of ASIC in €/month')
ASIC_yearly_revenue = 12 * get_user_input('ASIC revenue in €/month')
print()


if ASIC_yearly_cost >= ASIC_yearly_revenue:
    print('This ASIC is not profitable')
    exit()


network_hashrate_growth = - round(-math.log(2)/2, 3)  # Assuming Moore's Law
n, mining_reward, buying_btc = 0, 0, 1
# TODO: Find a better way than brute forcing the calculation.
bitcoin_price_growth = -100 * network_hashrate_growth


while mining_reward < buying_btc:
    bitcoin_price_growth = round(bitcoin_price_growth, 3) + 0.001

    if bitcoin_price_growth == network_hashrate_growth:
        print('This ASIC is only profitable if the bitcoin price rises faster than the network-hashrate')
        get_fair_price()

    mining_reward = get_mining_reward(
        get_time_interval(bitcoin_price_growth))

    buying_btc = ASIC_yearly_cost * \
        get_time_interval(bitcoin_price_growth) + ASIC_price

    n += 1


if n == 1:
    print('Error: Check input parameters and run code again.')
    exit()


print(
    f"This ASIC is profitable if the network-hashrate rises no faster than {math.exp(network_hashrate_growth - bitcoin_price_growth):.1f}-fold the bitcoin price."
)
print(
    f"Assuming Moore's Law, this ASIC is profitable after {get_time_interval(bitcoin_price_growth):.1f} years.")

get_fair_price()
