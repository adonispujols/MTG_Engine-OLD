from new_src import game as game_mod
from new_src import turn_parts as tp

# XXX try to make this share code with untap
def first_untap_of_game(game: game_mod.Game, first_player):
    print("Start of First Untap Step")
    game.step_or_phase = tp.TurnParts.UNTAP
    # at start, no one is active, so we must directly make 1st player active.
    self._players[first_player].make_active()
    print("Active Player:", self.active_index() + 1)
    print("TBA: Untap all")
    self.untap_all_of_active()
    self._upkeep()


def _untap(game: game_mod.Game):
    print("Start of Untap Step")
    game.step_or_phase = tp.TurnParts.UNTAP
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


def _upkeep(game: game_mod.Game):
    print("Start of Upkeep Step")
    game.step_or_phase = tp.TurnParts.UNTAP
    give_player_priority(active_index())


def _draw(game: game_mod.Game):
    # TODO must skip if 1st player's 1st draw (if 1v1 or 2-headed giant)
    print("Start of Draw Step")
    game.step_or_phase = tp.TurnParts.UNTAP
    print("TBA: Draw")
    active_player().draw()
    print_hand_and_decks()
    give_player_priority(active_index())


def _pre_combat(game: game_mod.Game):
    print("Start of Precombat Main Phase")
    game.step_or_phase = tp.TurnParts.UNTAP
    give_player_priority(active_index())


def _begin_combat(game: game_mod.Game):
    print("Start of Beginning of Combat Step")
    game.step_or_phase = tp.TurnParts.UNTAP
    give_player_priority(active_index())


def _declare_attackers(game: game_mod.Game):
    print("Start of Declare Attackers Step")
    # TODO need to skip to end if no attackers declared
    game.step_or_phase = tp.TurnParts.UNTAP
    give_player_priority(active_index())


def _declare_blockers(game: game_mod.Game):
    print("Start of Declare Blockers Step")
    game.step_or_phase = tp.TurnParts.UNTAP
    give_player_priority(active_index())


def _first_strike_damage(game: game_mod.Game):
    print("Start of First Strike Damage Step")
    # TODO need to skip to combat damage if no creatures wih first strike
    # ^ on either side of the field
    game.step_or_phase = tp.TurnParts.UNTAP
    give_player_priority(active_index())


def _combat_damage(game: game_mod.Game):
    print("Start of Combat Damage Step")
    game.step_or_phase = tp.TurnParts.UNTAP
    give_player_priority(active_index())


def _end_combat(game: game_mod.Game):
    print("Start of End of Combat Step")
    game.step_or_phase = tp.TurnParts.UNTAP
    give_player_priority(active_index())


def _post_combat(game: game_mod.Game):
    print("Start of Postcombat Main Phase")
    game.step_or_phase = tp.TurnParts.UNTAP
    print("Step or Phase:", step_or_phase.index)
    give_player_priority(active_index())


def _end(game: game_mod.Game):
    print("Start of End Step")
    game.step_or_phase = tp.TurnParts.UNTAP
    give_player_priority(active_index())


def _cleanup(game: game_mod.Game):
    print("Start of Cleanup Step")
    game.step_or_phase = tp.TurnParts.UNTAP
    untap()


_START_METHODS = (_untap, _upkeep, _draw, _pre_combat, _begin_combat,
                  _declare_attackers, _declare_blockers, _first_strike_damage,
                  _combat_damage, _end_combat, _post_combat, _end, _cleanup)


def start_next_step_or_phase(game, index):
    _START_METHODS[index + 1](game)
