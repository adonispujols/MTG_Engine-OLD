import abc
from src import restrictions
from src import player as player_mod
from src import game as game_mod
# Card
# Params:
# * Defined in script:
# - Name, Card Type,
# * Defined in game:
# - Owner, game


class Card(abc.ABC):
    def __init__(self, name, card_type, zone, player: player_mod.Player, game):
        # TODO
        super().__init__()
        self.name = name
        self.card_type = card_type
        self.super_type = None
        self.sub_type = None
        self.zone = zone
        self.owner = player
        self.game = game
        self.tapped = False
        # ALL cards + abilities have default sorcery speed restriction.
        self.restrictions = [restrictions.sorcery_speed]
        # XXX NEED TO FIGURE OUT CURRENT ZONE/RESTRICTING PLAY TO HAND (for now):

    def tapped(self):
        return self.tapped

    def tap(self):
        if not self.tapped:
            self.tapped = True
            return True
        else:
            return False

    def untap(self):
        if self.tapped:
            self.tapped = False
            return True
        else:
            return False

    @abc.abstractmethod
    def on_play(self):
        pass

    # XXX can't enforce params on abstract because they're overwritten!
    # ^ only remove until you remember!
    @abc.abstractmethod
    def resolve(self):
        pass

    def met_priority_or_special_restrictions(self):
        # overwritten by subclasses
        return self.owner.has_priority()

    def met_restrictions(self):
        for restriction in restrictions:
            if not restriction(self):
                return False
        return True

    def play(self):
        if self.met_priority_or_special_restrictions():
            self.owner.lose_priority()
            if self.on_play():
                self.game.passes = 0
                # XXX recall, don't get priority if mana ability
                # ^ or on cast if part of effect/resolution
                self.owner.gain_priority()
            else:
                raise RuntimeError("ERROR: Illegal play. Player: ", self.owner.index())
        else:
            # XXX avoiding to throw error in case we want to use play
            # ^ to probe/check legality of play (legally)
            return False

    def move_to(self, zone):
        # TODO
        pass

