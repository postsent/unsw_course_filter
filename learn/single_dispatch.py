"""https://stackoverflow.com/questions/24601722/how-can-i-use-functools-singledispatch-with-instance-methods
"""

from functools import singledispatch

class TestClass(object):

    def __init__(self):
        self.test_method = singledispatch(self.test_method)
        self.test_method.register(int, self._test_method_int)
        self.test_method.register(list, self._test_method_list)

    def test_method(self, arg, verbose=False):
        if verbose:
            print("Let me just say,", end=" ")

        print(arg)

    def _test_method_int(self, arg):
        print("Strength in numbers, eh?", end=" ")
        print(arg)

    def _test_method_list(self, arg):
        print("Enumerate this:")

        for i, elem in enumerate(arg):
            print(i, elem)


if __name__ == '__main__':
    test = TestClass()
    test.test_method(1.1, True)
    test.test_method(55555)
    test.test_method([33, 22, 11])
    