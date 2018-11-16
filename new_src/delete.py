# import enum
# import dis


def for_loop():
    lst = [7, 8, 9]
    for i in range(len(lst)):
        lst[i] = 5
    print(lst)


def list_comp():
    lst = [7, 8, 9]
    lst = [5 for _ in lst]
    print(lst)


for_loop()
list_comp()
# dis.dis(for_loop)
# print("LIST COMP")
# dis.dis(list_comp)


# class EnumTest(enum.Enum):
#     A = 1
#     B = 2
#
#
# x = "A"
# try:
#     choice = EnumTest["random"]
# except KeyError:
#     print("key not found")
# else:
#     print("key IS found")
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
