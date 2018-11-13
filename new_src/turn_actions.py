# Helper methods for game
# methods/classes related to (specifically) turn based actions

# we have parts of turn class holding constants
# turn based makes step or phase = parts of turn.STEP_OR_PHASE
# game can check if current step or phase is parts_of_turn.STEP_OR_PHASE
# now, if it's an index, or string, or whatever, we only change it in two places!
# ^ make untap = 0 then turn based list/dic shifts appropriately!




# SET INITIAL TO NONE (will be set later <- mkaes much more sense
# ^ since tech. we aren't at untap yet (game hasn't started)

# XXX try to make this share code with untap
def first_untap_of_game(self, first_player):
    print("Start of First Untap Step")
    step_or_phase.index = 0
    # ^ XXX evil sets? (along with rest of step_or_phase.index = x)
    # at start, no one is active, so we must directly make 1st player active.
    self._players[first_player].make_active()
    print("Active Player:", self.active_index() + 1)
    print("TBA: Untap all")
    self.untap_all_of_active()
    self._upkeep()


def _untap(self):
    print("Start of Untap Step")
    step_or_phase.index = 0
    # change active player to the next
    prev_active_index = self.active_index()
    self.active_player().make_inactive()
    self._players[(prev_active_index + 1) % len(self._players)].make_active()
    # XXX calling active_index again is slightly inefficient, but HEY,
    # ^ there might be a corner case we need to cover
    # ALWAYS FAVOR SECURITY/CLARITY OVER EFFICIENCY (to reasonable limits)
    print("Active Player:", self.active_index() + 1)
    # TBA = "Turn-Based Action", SBA = "State-Based Action"
    print("TBA: Untap all")
    self.untap_all_of_active()
    self._upkeep()


def _upkeep(self):
    print("Start of Upkeep Step")
    step_or_phase.index = 1
    give_player_priority(active_index())


def _draw(self):
    # TODO must skip if 1st player's 1st draw (if 1v1 or 2-headed giant)
    print("Start of Draw Step")
    step_or_phase.index = 2
    print("TBA: Draw")
    active_player().draw()
    print_hand_and_decks()
    give_player_priority(active_index())


def _pre_combat(self):
    print("Start of Precombat Main Phase")
    step_or_phase.index = 3
    give_player_priority(active_index())


def _begin_combat(self):
    print("Start of Beginning of Combat Step")
    step_or_phase.index = 4
    give_player_priority(active_index())


def _declare_attackers(self):
    print("Start of Declare Attackers Step")
    # TODO need to skip to end if no attackers declared
    step_or_phase.index = 5
    give_player_priority(active_index())


def _declare_blockers(self):
    print("Start of Declare Blockers Step")
    step_or_phase.index = 6
    give_player_priority(active_index())


def _first_strike_damage(self):
    print("Start of First Strike Damage Step")
    # TODO need to skip to combat damage if no creatures wih first strike
    # ^ on either side of the field
    step_or_phase.index = 7
    give_player_priority(active_index())


def _combat_damage(self):
    print("Start of Combat Damage Step")
    step_or_phase.index = 8
    give_player_priority(active_index())


def _end_combat(self):
    print("Start of End of Combat Step")
    step_or_phase.index = 9
    give_player_priority(active_index())


def _post_combat(self):
    print("Start of Postcombat Main Phase")
    step_or_phase.index = 10
    print("Step or Phase:", step_or_phase.index)
    give_player_priority(active_index())


def _end(self):
    print("Start of End Step")
    step_or_phase.index = 11
    give_player_priority(active_index())


def _cleanup(self):
    print("Start of Cleanup Step")
    step_or_phase.index = 12
    untap()


_START_METHODS = (_untap, _upkeep, _draw, _pre_combat, _begin_combat,
                  _declare_attackers, _declare_blockers, _first_strike_damage,
                  _combat_damage, _end_combat, _post_combat, _end, _cleanup)


def start_next_step_or_phase(game, index):
    _START_METHODS[index + 1](game)
