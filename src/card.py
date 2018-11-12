import abc
from src import restrictions
from src import player as player_mod
# Card
# Params:
# * Defined in script:
# - Name, Card Type,
# * Defined in game:
# - Owner, game


class Card(abc.ABC):
    def __init__(self, name, card_type, player: player_mod.Player):
        # TODO
        super().__init__()
        self.name = name
        self.card_type = card_type
        self.super_type = None
        self.owner = player
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

# Props:
# * Name
# * Supertype(s) (Basic, Legendary,...)
# * Cardtype(s) (Creature, Land, ...)
# * Subtype(s) (Tribe/class for creatures, aura for enchantments, ...)
# ^- Not every card NEEDS super or subtypes, but may gain them.
# ^- Should we keep as null fields here, or only add if relevant?
# * Tapped?
# ^- tech not relevant in non-permanent spells. Should we still keep?
# ^- does manifesting force us to care about this for sorceries/instants, still?
# * Game (game object)
# ^- SHOULD WE FIND ANOTHER WAY/add abstractions?
# ^^- (Keeps things more isolated)
# * Owner (player object)
# ^- need to keep track of control shifts OR when opponent casts the spell
# * zone  = "Library" (library at start)
# - its current zone
# ^ Changes for edh (commander in command zone), etc...
# ^ REGARDLESS, CARDS NEED TO HAVE THEIR ZONE/OWNER INFO
# CHANGED WHENEVER THE CHANGE HAPPENS (esp. for play/cast/etc).
# Funcs:
# * Play(card_index) <- get index from input call to play (the same index
# you used to select the card in the first place)
# - Needed GUI Improvement:
# ^- Check in advance if possible to cast as instant (to avoid illegal casts)!
# ^- For now, check card type. In future, check if any additional restrictions
# on cast/ability ("act. only as sorcery" or "only cast before X") AND if ANY
# part of proposal could change legal timing (like the additional costs in "Rout").
# - if met_priority_or_special_restrictions():
# ^- this just checks for priority, timing restrictions + etc are checked during casting.
# -- owner.lose_priority()
# ^-- can't take actions during playing/resolving something
# -- if on_play(card_index):
# ^--- if on_play was successful
# ^--- game.passes_count = 0
# ^--- reset passes count since a player took an action
# ^--- game.give_player_priority(owner)
# ^--- After ANY action (cast/act or special action), if the player had priority before
# doing it, they regain priority (and thus an SBA check and triggers). [CR 116.3c]
# -- else:
# ^--- will there already debug message/error from on_play/cast()?
# ^--- need to turn back state to before play!
# - else (did not have priority):
# -- debug message saying you can't play it?
# ^-- shouldn't just throw error if we didn't even begin the process
#


