def is_duplicate_lec(lec_bag, t, cur_enrol, cur_total):
    cur_enrol_stats = str(cur_enrol) + "/" + str(cur_total)
    cur_name = {"LEC" in t:"LEC", "WEB" in t:"WEB"}.get(True, None) # lec/web
    
    if ("LEC" in list(*zip(*lec_bag)) and cur_name == "WEB") or ("WEB" in list(*zip(*lec_bag)) and cur_name == "LEC"):
        lec_sum = "0/0"
        for lec in lec_bag:
            for k, v in lec.items():
                if k == "LEC":
                    c_enrol = int(v[:v.index("/")]) 
                    c_total = int(v[v.index("/") + 1:]) 
                    prev_enrol = int(lec_sum[:lec_sum.index("/")]) 
                    prev_total = int(lec_sum[lec_sum.index("/") + 1:]) 
                    lec_sum = str(prev_enrol + c_enrol) + "/" + str(c_total + prev_total)
                
                if k == "LEC" and cur_name == "WEB" and v == cur_enrol_stats:
                    return  True # ignore the result
                if k == "WEB" and cur_name == "LEC" and v == cur_enrol_stats:
                    return  True
        if cur_name == "WEB" and lec_sum == cur_enrol_stats:
            return True
    return False

lec_bag = [{"LEC":"5/10"}, {"LEC":"4/10"}] # {"LEC":"1/1"}, {"LEC":"1/1"}
t = "WEB ..."
cur_enrol = "9"
cur_total = "19"
print(is_duplicate_lec(lec_bag, t, cur_enrol, cur_total))