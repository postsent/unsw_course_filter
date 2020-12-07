# https://stackoverflow.com/questions/51114481/singledispatch-decorator-doesnt-work-as-advertised
from functools import singledispatch

"""
# works since 3.4
@foo.register(str)
def foo_str(a: str):
    pass

# works since 3.7
@foo.register
def foo_str(a: str)
    pass
"""

# Block A
@singledispatch
def divider(a, b=1):
    print(a, b)

@divider.register
def _(a: int, b=1):
    print(a/b)

@divider.register
def _(a: str, b=1):
    print(a[:len(a)//b])

divider(25, 2)
divider('single dispatch practice', 2)


# Block B
@singledispatch
def div(a, b=1):
    print(a, b)


@div.register(int)
def _(a: int, b=1):
    print(a/b)


@div.register(str)
def _(a: str, b=1):
    print(a[:len(a)//b])

div(25 , 2)
div('single dispatch practice', 2)