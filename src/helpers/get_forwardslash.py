def find_idxs(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def substr_digit(s, forward=True):
    sub = ""
    if forward:
        
        for l in s[::-1]:
            if not l.isdigit(): break
            sub += l
        sub = sub[::-1]
    else:
        for l in s:
            if not l.isdigit(): break
            sub += l
    return sub

def get_substr_by_letter(s, ch):
    ch_list = find_idxs(s, ch)
    res = []
    for idx in ch_list:
        forward_str = substr_digit(s[:idx], True)
        backward_str = substr_digit(s[idx + 1:], False)
        if forward_str and backward_str:
            res.append(forward_str + "/" + backward_str)
    return res[0]


a = "asdsdasdas1212323/123acv"
b = "1"
print(get_substr_by_letter(a, "/"))
