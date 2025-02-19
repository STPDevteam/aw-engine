import re

def return_first_digit(s):
    return re.search(r'\d', s).group()
s = " I have an apple, it is 5 or 6 cents"
print(return_first_digit(s)) # 5