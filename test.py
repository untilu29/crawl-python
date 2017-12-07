import re
print(re.sub('([A-Z]{1})', r'\1','ABCD.EF.GH.BC').lower())