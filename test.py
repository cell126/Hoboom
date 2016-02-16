import re

text = "000160"
data = re.match(r'2\d{5}', text)
print(data)