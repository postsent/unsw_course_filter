class Old_data:

    def __init__(self, year):
        self.result = []
        with open(f"courses_data/y{year}.txt", "r") as f:
            lines = f.readlines()
            for l in lines:
                tmp = l.split()
                tmp = tmp[:5] + [" ".join(tmp[5:])]
                self.result.append(tmp)
           
    def get_result(self):
        return self.result
    @staticmethod
    def get_popular_degree(year):
        with open(f"courses_data/y{year}.txt", "r") as f:
            lines = f.readlines()[1:-1]
            res = []
            for l in lines:
                c = l.split()[1][:4]
                if c not in res:
                    res.append(c)
        for r in res:
            print(r, end=" ")
# tmp = Old_data(2020).get_result()
# print(tmp[1])
# Old_data.get_popular_degree(2020)