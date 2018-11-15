import typing
from new_src import passes
from new_src import turn_actions
from new_src import turn_parts as tp
from new_src import player as player_mod
from new_src import stack
from new_src import card as card_mod
from new_src import print_utils as print_u
from new_src import mana_types as mt
# XXX Always forward reference types (wrap in string) to avoid import errors!
# ^ STILL NEED TO IMPORT FOR THIS TO WORK <- key misunderstanding


class Game:
    step_or_phase: "tp.TurnParts"
    battlefield: typing.List[typing.List["card_mod.Card"]]
    players: typing.List["player_mod.Player"]

    def __init__(self):
        self.debug = False
        self.ai_only = False
        self.players = None
        self.battlefield = None
        self._stack = stack.Stack()
        self._passes = passes.Passes()
        # Initially none since game isn't at untap yet (officially)
        self.step_or_phase = None

    def _print_hand_and_decks(self):
        # XXX Use ID when comparing objects (as you should)
        for i, player in enumerate(self.players):
            print("P" + str(i + 1), "HAND:\n", player.hand,
                  "\nP" + str(i + 1), "DECK:\n", player.deck)

    def _in_main_phase(self):
        return (self.step_or_phase == tp.TurnParts.PRECOMBAT_MAIN
                or self.step_or_phase == tp.TurnParts.POSTCOMBAT_MAIN)

    def _sorcery_speed(self, is_active):
        return is_active and self._in_main_phase() and self._stack.is_empty()

    def _met_land_restrictions(self, player):
        # 115.2a Playing a land is a special action. To play a land, a player puts that land onto the battlefield from the zone it was in (usually that player’s hand). By default, a player can take this action only once during each of their turns. A player can take this action any time they have priority and the stack is empty during a main phase of their turn. See rule 305, “Lands.”
        return self._sorcery_speed(player.active) and player.under_land_limit()

    # TODO Refactor: don't pass index if you need the player (for api)
    # ^ TODO BUT, you ONLY need an object to use its api
    # ^ YOU NEVER (except in rare cases, like init) modify a field directly!
    # ^ YOU MAY "get" a field, but as a PARAM. You may NOT do object.foo ... etc
    # TODO Make index a player property? <- Need to track deaths, then
    # ^ likely yes (much simpler, esp since it's static)
    # ^ for deaths: either del player & update all indices,
    # ^ or make empty & skip over, or...
    # TODO confirm if CARD index (in zone) should be a property, too!
    # ^ most likely not
    def active_index(self):
        # XXX could definitely optimize this AND SIMILAR (however, clarity is key atm)
        for i, player in enumerate(self.players):
            if player.active:
                return i

    def active_player(self):
        return self.players[self.active_index()]

    def untap_all_of_active(self):
        for card in self.battlefield[self.active_index()]:
            card.untap()

    def give_player_priority(self, index):
        if int(self._passes) == len(self.players):
            # TODO need to take into account actions taken in between passes!
            # MUST RESET PASSES (else we're stuck in infinite loop)
            self._passes.reset()
            turn_actions.start_next_step_or_phase(self, self.step_or_phase.value)
        else:
            def user_has_priority():
                # TODO is it okay to just ignore superfluous/extra input?
                # ^ i.e., hand 2 asdfasdfasdf will just have asdf... ignored
                # ^ is this okay behavior?
                while True:
                    choice = input(print_u.player_prompt(index, self.players[index])).split()
                    # TODO here is where we add more choices for player
                    # ^ either actions requiring priority (play, activate, pass, etc)
                    # ^ OR ability to look at game state
                    # ^^ XXX could organize ALL input asks such that:
                    # ^^ user may always look at the board state before a choice
                    if not choice:
                        self._passes.inc()
                        self.give_player_priority((index + 1) % len(self.players))
                        break
                    # TODO implement user-limited commands (no debug)
                    # ^ normally, user's knowledge of game is limited
                    # ^ he can't just randomly search through hands, decks, etc
                    # ^ EX: "hand-self" prints own hand of player
                    # TODO play(card)
                    elif choice[0] == "play":
                        # TODO allow for playing from other zones
                        # player chooses a card from a zone (just hand for now)
                        try:
                            # enter card # in hand (counting left to right)
                            card_index = int(choice[1]) - 1
                        except ValueError:
                            print("ERROR: Invalid integer")
                        except IndexError:
                            print("ERROR: Need 1 player # parameter, given 0")
                        else:
                            # TODO VARIABLES FOR LIST[] DO SAVE COMPUTATION!
                            # ^- A list[i] takes more work than just reading var
                            # ^ So go ahead and have player = players[index]!
                            p = self.players[index]
                            if 0 <= card_index < p.hand.size():
                                self._play(p.hand, card_index, index, p)
                            else:
                                print("ERROR: Invalid card #")
                    # TODO activate ability
                    # ^ what to name for pseudo activations, like morph and
                    # ^ other special actions?
                    elif choice[0] == "act":
                        # TODO allow for activating from other zones
                        # player chooses a card from a zone (just battlefield for now)
                        try:
                            # enter card # on field (counting left to right)
                            card_index = int(choice[1]) - 1
                        except ValueError:
                            print("ERROR: Invalid integer")
                        except IndexError:
                            print("ERROR: Need 1 player # parameter, given 0")
                        else:
                            # TODO VARIABLES FOR LIST[] DO SAVE COMPUTATION!
                            # ^- A list[i] takes more work than just reading var
                            # ^ So go ahead and have player = players[index]!
                            # TODO sometimes you CAN activate stuff on another
                            # ! person's side of the field!
                            # Right now you can only activate from YOUR side!
                            p_field = self.battlefield[index]
                            if 0 <= card_index < len(p_field):
                                self._activate(p_field, card_index, self.players[index].mana_pool)
                            else:
                                print("ERROR: Invalid card #")
                    elif choice[0] == "field":
                        print_u.print_field(self.battlefield)
                    elif self.debug:
                        # XXX Our code ignores extra input after what is understood
                        # ^ I.e., "hand 0 asdf" is translated as "hand 0"
                        if choice[0] == "hand":
                            # XXX make a general "valid player index" method?
                            try:
                                p_index = int(choice[1]) - 1
                            except ValueError:
                                print("ERROR: Invalid integer")
                            except IndexError:
                                print("ERROR: Need 1 player # parameter, given 0")
                            else:
                                # XXX Apply EAFP ONLY when validating input, NOT LOGIC!
                                # ^ I.e., checking for int/params is FINE! BUT we
                                # ^ can't allow for irreversible game states by allowing
                                # ^ invalid actions to run until error is caught!!!
                                # - Essentially: Preemptively stop illegal game states
                                # - from existing!
                                if 0 <= p_index < len(self.players):
                                    print_u.print_hand(p_index, self.players[p_index])
                                else:
                                    print("ERROR: Invalid player #")
                        # could we combine this error message w/ final else?
                        else:
                            print("ERROR: Invalid input")
                    else:
                        print("ERROR: Invalid input")
            if index == 0:
                if not self.ai_only:
                    user_has_priority()
                else:
                    # TODO continue adding AI options in future!
                    # ai is making choice
                    pass
            else:
                if self.debug:
                    user_has_priority()
                else:
                    pass

    # TODO Rafactor params to represent ALL info needed (even redundant object)
    # ^ I.e., even if you need both player.index AND player, those are TWO
    # ^ SEPARATE params (that we may later then refactor to remove player from)
    # XXX Only pass the EXACT object you need! Not an object containing it!
    # ^ i.e, what's the closest possible object you need to do your work?
    # ^ e.g., if you need a hand, just get the hand, NOT player (for player.hand)
    # XXX WARNING: You can ONLY edit stuff by accessing it's wrapper!
    # ^ Thus, any operation on "class.foo" has to be done via class.foo = ...
    # ^ NOT passed as a param! Direct param loses class context, so can't edit
    # XXX IT IS *PLAY'S* JOB TO PARSE THE INFO NEEDED FROM PLAYER
    # ^ *NOT* THE THING SIMPLY CALLING IT FROM INPUT
    # ^ Give play the minimum it should expect from input,
    # ^ and let PLAY sort out the rest!
    def _play(self, zone, card_index, p_index, p):
        card: "card_mod.Card" = zone.get(card_index)
        if card.type == "Land":
            self._play_land(card, zone, card_index, p_index, p, p.lands_played)
        # elif card.type == "Creature"

    # XXX since met land restrictions requires player, play_land, TOO, requires
    # ^ it! Just passing it as an index so we can call players[index] is both
    # ^ deceptive, clunky, AND inefficient!
    def _play_land(self, card, zone, card_index, player_index, player, lands_played):
        if self._met_land_restrictions(player):
            zone.remove(card_index)
            self.battlefield[player_index].append(card)
            # XXX Always increment afterwards (if you can) so it's only
            # ^ done on success
            lands_played.inc()

    def _activate(self, zone, card_index, mana_pool):
        # XXX this only works with primitive array zones unlike above,
        # ^ which uses an actual object
        card: "card_mod.Card" = zone[card_index]
        if card.ability == "{T}: Add G":
            # [CR 601.2e]: See if legal.
            # At instant speed, so priority (or call/act. by effect) is implied.
            #
            if card.
            # try to tap, if true, do the thing
            mana_pool.add(mt.ManaTypes.G.value)
