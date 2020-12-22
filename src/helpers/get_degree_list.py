with open("degrees", "r") as f:
    lines = f.readlines()
    print("[", end="")
    for l in lines:
        t = l.split(" ")[0]
        print("\""+t+"\"", end="")
        if l != lines[-1]:
            print(",", end=" ")
    print("]")