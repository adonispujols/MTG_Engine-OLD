from src import card
from src import player as player_mod


class Spell(card.Card):
    def __init__(self, costs, name, card_type, zone, player: player_mod.Player, game):
        super().__init__(name, card_type, zone, player, game)
        self.costs = costs

    def resolve(self):
        # TODO
        pass

    def on_play(self):
        self.cast()

    def cast(self):
        # TODO
        # [CR 601.2a]
        # move card
        pass

# * Cast():
# - 601.2a:
# ^- move card from where it is to the stack:
# - game.stack.push(self)
# -- zone.remove(card_index) <- removes this card from relevant zone
# ^- for now we're simply pushing to stack, then removing from hand
# ^- how to deal with copies? <- where do they come from?
# ^- how to move from any where to the stack?
# ^- RECALL ALLLL MOVEMENTS SHOULD BE MONITORED!
# ^- CARDS CARE IF GONE FROM BATTLEFIELD TO GRAVE, OR LIB TO GRAVE, OR ETC
# ^- Godot should be referencing this same object from the Stack, without making a separate copy of it or whatnot, and thus see whatever changes we make here.
# ^- CONFIRM THIS IS THE CASE. Otherwise, only send the complete spell to stack.
# - 601.2e:
# - Check if met restrictions (mostly just if sorcery speed). if true, continue to next step (paying costs, or 601.2f):
# - if !met_restrictions():
# -- throw error, for now
# ^- should just return false.
#
# - 601.2f:
# -  determine final costs.
# ^ For now, there is no determining. We just set to original cost. Although this is where alt costs, additional costs, cost modifies, etc are determined.
# - costs[0]
# ^- REQUIRED to make copy of mana costs if there are any modifcations (the COPY is modifed).
# ^- Need to distuingish between mana costs and others! (this is super hard coded)
# - final_costs[] = costs[]
# -601.2h:
# - if !owner.play_costs(costs):
# -- throw error
# ^- tech should just return false (since we will reverse state if cast returns false).
# ^-- again, we don't know how to reverse the state.
# [The player pays the total cost in any order. Partial payments are not allowed. Unpayable costs can’t be paid.]
# - 601.2i:
# - again, this part isn't fully implemented (no spell modification), but mostly there.
# - return true
#
# </ Cast >
#
# * Resolve:
# - must implement