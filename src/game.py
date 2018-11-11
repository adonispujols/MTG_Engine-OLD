import typing
from src import stack
from src import turn_actions
from src import player as player_mod
from src import card as card_mod
# XXX ^ should NOT import just for type checking (risks cyclic importing)
# ^ we can't get around it atm, but beware!

class Game:
    def __init__(self, players: typing.List[player_mod.Player], index):
        self.players = players
        self.first_player_index = index
        # XXX ^ should NOT hold 1st player index in memory (wasteful).
        self.step_or_phase = 0
        self.passes = 0
        self.battlefield: typing.List[typing.List[card_mod.Card]] = []
        for player in range(len(players)):
            self.battlefield.append([])
        self.stack = stack.Stack()

    def start_game(self):
        turn_actions.special_untap(self, self.get_player(self.first_player_index))

    def get_player(self, index):
        return self.players[index]

    def next_player(self, curr_index):
        return self.get_player((curr_index + 1) % len(self.players))

    def active_player(self):
        for player in self.players:
            if player.active():
                return player

    def player_due_priority(self):
        for player in self.players:
            if player.due_priority():
                return player

    def pass_priority(self, player):
        if not player.has_priority():
            raise RuntimeError("ERROR: Passed without priority. Player: ", player.index())
        player.lose_priority()
        if self.all_passed_no_actions(player.index()) and self.stack.empty():
            self.empty_mana_pools()
            turn_actions.start_next_step_or_phase(self.step_or_phase, self)
        else:
            if not self.stack.empty():
                self.stack.resolve()
            self.next_player(player.index()).gain_priority()

    def all_passed_no_actions(self, index):
        passed = False
        if self.next_player(index).active():
            if self.passes == len(self.players):
                passed = True
            self.passes = 0
        else:
            self.passes += 1
        return passed

    def empty_mana_pools(self):
        for player in self.players:
            player.mana_pool.clear()

    def step_or_phase(self):
        return self.step_or_phase

    def change_active_player_to_next(self):
        prev_active_index = self.active_player().index()
        self.active_player().make_nonactive()
        self.next_player(prev_active_index).make_active()

    def permanents_of_player(self, index):
        return self.battlefield[index]

    def put_on_battlefield(self, card, player):
        self.battlefield[player.index()].append(card)
        player.hand.remove(card.index())

    def untap_all_of_player(self, index):
        for card in self.permanents_of_player(index):
            card.untap()
