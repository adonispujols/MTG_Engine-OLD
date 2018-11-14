import typing
from new_src import passes
from new_src import turn_actions
from new_src import turn_parts as tp
from new_src import player as player_mod
from new_src import stack
from new_src import card as card_mod
# XXX Always forward reference types (wrap in string) to avoid import errors!
# ^ STILL NEED TO IMPORT FOR THIS TO WORK <- key misunderstanding


class Game:
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

    def _print_hand(self, index):
        print("P" + str(index + 1), "HAND:\n", self.players[index].hand)

    def _player_prompt(self, index):
        return "P{:d} {}: ".format(index + 1, ("A" if self.players[index].active else "N"))

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
        if self._passes.count != len(self.players):
            # ask the user for input
            def user_has_priority():
                while True:
                    # a_n = "A" if self.players[index].active else "N"
                    choice = input(self._player_prompt(index)).split()
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
                            # XXX maybe we should push this player def. up?
                            # Should we keep direct access to players or so?
                            # ^ Is that even possible (if not using array)?
                            p = self.players[index]
                            if 0 <= card_index < p.hand.size():
                                self.play(p.hand, card_index, p.active, p.under_land_limit(), index)
                    elif self.debug:
                        # XXX Our code ignores extra input after what is understood
                        # ^ I.e., "hand 0 asdf" is translated as "hand 0"
                        if choice[0] == "hand":
                            # XXX make a general "valid player index" method?
                            try:
                                # "p_index" means player index/index param
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
                                    self._print_hand(p_index)
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
        # TODO need to take into account actions taken in between passes!
        # "passed in succession"
        else:
            # MUST RESET PASSES (else we're stuck in infinite loop)
            self._passes.reset()
            turn_actions.start_next_step_or_phase(self, self.step_or_phase)

    # Playing around with play

    # the USER/AI plays cards, NOT the player object!
    # ^ It's something the actual player DOES on the CARD
    # TODO start with playing a land!
    # ^ literally just straight up think about how, you would go about playing a land.
    # ^ DO NOT WORRY about efficiency/super abstract design.
    # ^ we'll refactor/apply proper OOP principles once we're done!
    def play(self, zone, card_index, is_active, under_land_limit, player_index):
        # with zone and index we can find the card
        # FIRST, just look at it. THEN pop once confirmed legal
        card = zone.get(card_index)
        # ELSE, IT, OR AT LEAST, CAST, WON'T KNOW WHAT TO DO
        if card.type == "Land":
            # check if at sorcery speed (priority is implied since play can only be
            # ^ be called if had priority)
            in_main_phase = (self.step_or_phase == tp.TurnParts.PRECOMBAT_MAIN
                    or self.step_or_phase == tp.TurnParts.POSTCOMBAT_MAIN)
            sorcery_speed = in_main_phase and self._stack.is_empty() and is_active
            # 1st is timing restriction, second is a specific restriction
            if sorcery_speed and under_land_limit:
                # put on battlefield (typically from hand)
                # need to move it from previous zone to battlefield
                zone.remove(card_index)
                self.battlefield[player_index].append(card)

    # to play a land
    # check if card is a land:
    # ^ this is a special action that requires:
    # - sorcery speed (priority (given), stack is empty, is their turn (is active))
    # & - lands played < lands limit
    # ^ then, you put it onto battlefield (usually from hand)
    # ^ no need for stack resolving or passing priority
    # !!!!    regain priorirty afterwards
    # "losing" priority just means game is doing stuff and you can't interact
    # with it (not accepting input)
    # "gaining" priority means the game is taking input again

