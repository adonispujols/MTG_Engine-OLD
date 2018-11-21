import collections


d = collections.deque()
d.append(["choose", 1])
d.append(["choose", 2])
d.append(["choose", 3])
d.append(["choose", 4])
print(d)
signal = d.popleft()
# could get an exception (nasty) <- means everything needs to be in []
# each signal could store a variety of information
# choose: plyer chosen. draw: player to draw
# give priority: player to give priority
# declre attacks: creature (mybe zone + card_index) and wht player
# don't wrp in object lest we'll haev lots of wasted attribtes that arent used
# rry will be good enough, for now
if signal[0] == "choose":
    # we can assume choose gives us this
    index = signal[1]
    print(index)

if signal[0] == "attck":
    card_in_gui = "zone.get(card"