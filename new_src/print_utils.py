def print_hand(index, player):
    print("P" + str(index + 1), "HAND:\n", player.hand)


def print_field(battlefield):
    print(battlefield)


def player_prompt(index, player):
    return "{} P{:d}: ".format(("A" if player.active else "N"), index + 1)
