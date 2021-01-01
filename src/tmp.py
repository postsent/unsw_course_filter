from itertools import product
names = ['Brown', 'Wilson', 'Bartlett', 'Rivera', 'Molloy', 'Opie']
addres = ["a", "b", "c"]
tmp = zip(names, addres)
print([i for i in tmp])