import enum
# import dis


class EnumTest(enum.Enum):
    A = 1
    B = 2


x = "A"
try:
    choice = EnumTest[x]
except KeyError:
    print("key not found")
else:
    print("key IS found")
# print(type(EnumTest[x]))

# def foo():
#   t.name
#   t.name
#   t.name
#   t.name
#
# def bar():
#   x = t.name
#   x
#   x
#   x
#
# x = t
# x.name = "123123123"
# print(t.name)
# dis.dis(foo)
# print("bar")
# dis.dis(bar)

# accessing members ALSO takes work!
