import enum
import dis

#
# class Test:
#     def __init__(self):
#         self.name = "test test"
#
#
# t = Test()
#
#
# class EnumTest(enum.Enum):
#     A = 1
#     B = 2
x = []
if not x:
    print("false")
# print(EnumTest.v)

# x = "A"
# print(x == EnumTest.A.name)
#
# x = {"G": 2}
# print(x)
#
# y = 4
# if y == 3 or 1:
#     print("df")
#
# b = 0
# if not b:
#     print("b is seen as False")
#
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
#
# payed_costs = False
# # XXX make mana types more verbose "Green" and simpler?
# generic_cost = 1
# specific_types = {"G": 1}
# while not payed_costs:
#     mana_payed = input("Pay Mana: ")
#     # for key, value in inputdict.items():
#     #     # do something with value
#     #     inputdict[key] = newvalue
#     if (mana_payed in specific_types) and (specific_types[mana_payed] > 0):
#         specific_types[mana_payed] -= 1
#     elif generic_cost > 0:
#         generic_cost -= 1
#     else:
#         print("ERROR: Generic costs payed. Missing specific type.")
#     if all(i == 0 for i in specific_types.values()) and (generic_cost == 0):
#         break
