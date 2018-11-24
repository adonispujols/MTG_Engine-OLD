from KISS import game as game_mod
from KISS import turn_parts as tp


def first_untap(game: "game_mod.Game", starting_player):
    game.step_or_phase = tp.TurnParts.UNTAP
    game.players[starting_player].make_active()
    game.reset_lands_played()
    # TBA = "Turn-Based Action", SBA = "State-Based Action"
    game.untap_all_of_active()
    game.empty_mana_pools()
    _upkeep(game)


def _untap(game: "game_mod.Game"):
    game.step_or_phase = tp.TurnParts.UNTAP
    prev_active = game.active_index()
    game.players[prev_active].make_inactive()
    new_active = (prev_active + 1) % len(game.players)
    game.players[new_active].make_active()
    game.reset_lands_played()
    game.untap_all_of_active()
    game.empty_mana_pools()
    _upkeep(game)


def _upkeep(game: "game_mod.Game"):
    game.step_or_phase = tp.TurnParts.UPKEEP
    game.give_player_priority(game.active_index())


def _draw(game: "game_mod.Game"):
    # TODO skip the very 1st draw step
    game.step_or_phase = tp.TurnParts.DRAW
    game.active_player().draw()
    game.give_player_priority(game.active_index())


def _pre_combat(game: "game_mod.Game"):
    game.step_or_phase = tp.TurnParts.PRECOMBAT_MAIN
    game.give_player_priority(game.active_index())


def _begin_combat(game: "game_mod.Game"):
    game.step_or_phase = tp.TurnParts.BEGIN_COMBAT
    game.give_player_priority(game.active_index())


def _declare_attackers(game: "game_mod.Game"):
    # TODO need to skip to end if no attackers declared
    game.step_or_phase = tp.TurnParts.DECLARE_ATTACKERS
    game.give_player_priority(game.active_index())


def _declare_blockers(game: "game_mod.Game"):
    game.step_or_phase = tp.TurnParts.DECLARE_BLOCKERS
    game.give_player_priority(game.active_index())


def _first_strike_damage(game: "game_mod.Game"):
    # TODO skip to combat damage if no creatures wih first strike
    game.step_or_phase = tp.TurnParts.FIRST_STRIKE_DAMAGE
    game.give_player_priority(game.active_index())


def _combat_damage(game: "game_mod.Game"):
    game.step_or_phase = tp.TurnParts.COMBAT_DAMAGE
    game.give_player_priority(game.active_index())


def _end_combat(game: "game_mod.Game"):
    game.step_or_phase = tp.TurnParts.END_COMBAT
    game.give_player_priority(game.active_index())


def _post_combat(game: "game_mod.Game"):
    game.step_or_phase = tp.TurnParts.POSTCOMBAT_MAIN
    game.give_player_priority(game.active_index())


def _end_step(game: "game_mod.Game"):
    game.step_or_phase = tp.TurnParts.END_STEP
    game.give_player_priority(game.active_index())


def _cleanup(game: "game_mod.Game"):
    game.step_or_phase = tp.TurnParts.CLEANUP
    _untap(game)


_START_METHODS = (_untap, _upkeep, _draw, _pre_combat, _begin_combat,
                  _declare_attackers, _declare_blockers, _first_strike_damage,
                  _combat_damage, _end_combat, _post_combat, _end_step, _cleanup)


def start_next_step_or_phase(game, step_or_phase: "tp.TurnParts"):
    _START_METHODS[step_or_phase.value + 1](game)
