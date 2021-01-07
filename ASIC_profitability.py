import math

def user_input_function(text):
    while True:
        user_input = input(f'Enter {text}: ')
        try:
            user_input = float(user_input)
        except:
            print('Error: Only numbers (integers and floats) are allowed as input')
            continue
        return user_input

ASIC_price = user_input_function('ASIC price in €')
ASIC_yearly_cost = 12 * user_input_function('monthly cost of ASIC in €/month')
ASIC_yearly_revenue = 12 * user_input_function('ASIC revenue in €/month')

j = round(-math.log(2) / 2, 3)
k = -j
a,b = 0,1

while a < b:
    k = round(k, 3) - 0.001
    end_of_miner_profitability = ( math.log(ASIC_yearly_revenue) - math.log(ASIC_yearly_cost) ) / (-j - k)
    end_of_miner_profitability = round(end_of_miner_profitability, 3)
    a = ( 1 - math.exp(j * end_of_miner_profitability) ) * ASIC_yearly_revenue / -j
    b = ( ASIC_yearly_cost * end_of_miner_profitability ) + ASIC_price 

print(f'Bitcoin\'s growth coefficient may be no lower than {k:.3f}')

current_price = user_input_function('Bitcoin Price in USD/BTC') # The script should get the price online.
estimated_price = current_price * math.exp(k)
estimated_price = float(estimated_price)

print(f'The Bitcoin price in 1 year is estimated to be at least {estimated_price:.2f} USD.')