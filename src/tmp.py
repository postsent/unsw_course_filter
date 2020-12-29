# import re
# # http://regex.inginf.units.it/
# txt = "ABCc100/100"
# txt = "this\\test"
# txt = "1111/test"
# tmp = "^[a-zA-Z0-9]+\\\\[a-zA-Z0-9]+$"
# tmp = "/^[\d]+/[a-zA-Z0-9]+$/"
# print(tmp)

# p = re.compile(tmp)

# print(p.match(txt).group(0))

t = "\nTLB"
if not any(i in t[1:4] for i in ["LEC", "WEB", "THE", "PRJ"]):
    print("111")