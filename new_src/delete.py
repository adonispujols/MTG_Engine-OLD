import enum
import dis


class Test:
    def __init__(self):
        self.name = "test test"


t = Test()


class EnumTest(enum.Enum):
    A = 1
    B = 2


x = "A"
print(x == EnumTest.A.name)

x = {"G": 2}
print(x)

y = 4
if y == 3 or 1:
    print("df")

b = 0
if not b:
    print("b is seen as False")

def foo():
  t.name
  t.name
  t.name
  t.name

def bar():
  x = t.name
  x
  x
  x

x = t
x.name = "123123123"
print(t.name)
dis.dis(foo)
print("bar")
dis.dis(bar)

# accessing members ALSO takes work! <- So a var works here, too.
# BUT, if you want to do work on the member, you need the object wrapping it
# ^ i.e., can only affect player's attributes if you have the player object
# ^- (unless you're using an object within player)
