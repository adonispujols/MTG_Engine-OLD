class Card:
    def __init__(self):
        self.tapped = False

    def tapped(self):
        return self.tapped

    def tap(self):
        if not self.tapped():
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

    def resolve(self):
        # TODO
        pass

# Card
# Params:
# * Defined in script:
# - Name, Card Type,
# * Defined in game:
# - Owner, game
# Props:
# * Name
# * Supertype(s) (Basic, Legendary,...)
# * Cardtype(s) (Creature, Land, ...)
# ^- some cards may not even have a card type
# * Subtype(s) (Tribe/class for creatures, aura for enchantments, ...)
# ^- Not every card NEEDS super or subtypes, but may gain them.
# ^- Should we keep as null fields here, or only add if relevant?
# * Restrictions = [restrictions.sorcery_speed()]
# ^- actually [funcref(restrictions, "sorcery_speed")] for godot.
# ^- restrictions to cast spell or play land (well, not sure if there's any play land resitrcitons)
# ^ ALL cards + abilities inherit default sorcery speed restriction.
# NEED TO FIGURE OUT CURRENT ZONE/RESTRICTING PLAY TO HAND (for now):
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
# * resolve():
# ^- The effects of playing lands and other special actions are
# technically NOT referred to as “resolving,” but we’ll
# refer to it in our code
# ^^- same effect, but do mark in code this potential
# inconsistency with rules.
# - must implement
# WHY IS THIS FORCE TO IMPLEMENT? oh. they just resolve immediately
#
# * met_restrictions
# - checks if all restrictions of the object have been meet.
# - for restriction in restrictions:
# -- if !restriction(this card):
# ^-- return false
# - return true
# ^- if we failed to meet any, it'll return false.
# ^- else, we'll reach this return true.
# ^- all restrictions are boolean methods that check for
# satisfaction upon call.
#
# * on_play(card_index)
# - must implement
#
# * met_priority_or_special_restrictions():
# - basic, hands-down virtually no exceptions restriction to play/cast something.
# - not to be confused with timing or void or null rod or etc restrictions!
# - Either meet priority restriction, or some special restriction
# (mostly just for mana abilities).
# ^- could even share with Ability, too! (though they'll always require priority)
# - return owner.has_priority()
#