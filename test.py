import math 

CF = [0, -1670000, -3664000, -378000, 6475000]


initial_capital_raise = 7000000
initial_investment = 400000

share = initial_investment/initial_capital_raise


DCF = 0

risk_free_interest = 0.034

for i in range(0,5):
     DCF += (CF[i] * share)/ math.pow((1+0.034), i)


print("\n\nAlternative one :")     
print("DCF is {}".format(DCF))
print("NPV is {}".format(DCF - initial_investment))
print("--------------\n")  

sd = 0.40

current_investment = 450000

NPVq =  initial_investment/(current_investment/math.pow(1+risk_free_interest, 4))
cumulative_variation = sd * 2

print("Alternative two :")     
print("NPVq is {}".format(NPVq))
print("cumulative variation is {}".format(cumulative_variation))


final_alt2 = 31.8
print("real option value : {}".format(final_alt2))
print("--------------\n") 
