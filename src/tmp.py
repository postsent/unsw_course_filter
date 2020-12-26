def str_sum(a, b):
        c_enrol = int(a[:a.index("/")]) 
        c_total = int(a[a.index("/") + 1:]) 
        prev_enrol = int(b[:b.index("/")]) 
        prev_total = int(b[b.index("/") + 1:]) 
        enrol = c_enrol  + prev_enrol
        total = prev_total + c_total
        return str(enrol) + "/" + str(total)

def sort_by_key(l):
    tmp = sorted(l, key=lambda k: k["c"]) 
    res = []
    res.append(tmp[0])
    for t in tmp[1:]:
        if t["c"]  == res[-1]["c"]:
            res[-1]["e"] = str_sum(res[-1]["e"], t["e"])
            res[-1]["l"] = str_sum(res[-1]["l"], t["l"])
            continue
        res.append(t)
    return res
a = [{"c": "comp1511", "e":"1/1", "l":"2/2"}, {"c":"comp1511", "e":"1/1", "l":"2/2"}, {"c":"math1131","e":"1/1", "l":"2/2"}, 
        {"c":"math1231", "e":"1/1", "l":"2/2"}]
res = sort_by_key(a)
print(res)
