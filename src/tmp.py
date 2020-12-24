def sum(a, b):
    c_enrol = int(a[:a.index("/")]) 
    c_total = int(a[a.index("/") + 1:]) 
    prev_enrol = int(b[:b.index("/")]) 
    prev_total = int(b[b.index("/") + 1:]) 
    enrol = c_enrol  + prev_enrol
    total = prev_total + c_total
    return str(enrol) + "/" + str(total)

print(sum("3/3", "1/1"))