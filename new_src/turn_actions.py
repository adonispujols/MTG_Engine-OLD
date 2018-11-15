from new_src import game as game_mod
from new_src import turn_parts as tp
# XXX Always forward reference types (wrap in string) to avoid import errors!
# ^ STILL NEED TO IMPORT FOR THIS TO WORK <- key misunderstanding


def first_untap_of_game(game: "game_mod.Game", first_player):
    game.step_or_phase = tp.TurnParts.UNTAP
    print("Start: First Untap step")
    game.players[first_player].make_active()
    print("Active Player:", first_player + 1)
    # TBA = "Turn-Based Action", SBA = "State-Based Action"
    print("TBA: Active untaps all")
    # XXX should game be doing this, or should we get the active player,
    # ^ then untap all their stuff (since it makes sense here)?
    game.untap_all_of_active()
    game.empty_mana_pools()
    _upkeep(game)


def _untap(game: "game_mod.Game"):
    print("Start: Untap step")
    game.step_or_phase = tp.TurnParts.UNTAP
    prev_active = game.active_index()
    game.players[prev_active].make_inactive()
    new_active = (prev_active + 1) % len(game.players)
    game.players[new_active].make_active()
    print("Active Player:", new_active + 1)
    game.untap_all_of_active()
    print("TBA: Active untaps all")
    game.empty_mana_pools()
    _upkeep(game)


def _upkeep(game: "game_mod.Game"):
    print("Start: Upkeep")
    game.step_or_phase = tp.TurnParts.UPKEEP
    game.give_player_priority(game.active_index())


def _draw(game: "game_mod.Game"):
    # TODO must skip if 1st player's 1st draw (if 1v1 or 2-headed giant)
    print("Start: Draw")
    game.step_or_phase = tp.TurnParts.DRAW
    print("TBA: Active draws")
    game.active_player().draw()
    game.give_player_priority(game.active_index())


def _pre_combat(game: "game_mod.Game"):
    print("Start: Precombat Main")
    game.step_or_phase = tp.TurnParts.PRECOMBAT_MAIN
    game.give_player_priority(game.active_index())


def _begin_combat(game: "game_mod.Game"):
    print("Start: Begin Combat")
    game.step_or_phase = tp.TurnParts.BEGIN_COMBAT
    game.give_player_priority(game.active_index())


def _declare_attackers(game: "game_mod.Game"):
    print("Start: Declare Attackers")
    # TODO need to skip to end if no attackers declared
    game.step_or_phase = tp.TurnParts.DECLARE_ATTACKERS
    game.give_player_priority(game.active_index())


def _declare_blockers(game: "game_mod.Game"):
    print("Start: Declare Blockers")
    game.step_or_phase = tp.TurnParts.DECLARE_BLOCKERS
    game.give_player_priority(game.active_index())


def _first_strike_damage(game: "game_mod.Game"):
    print("Start: First Strike Damage")
    # TODO need to skip to combat damage if no creatures wih first strike
    # ^ on either side of the field
    game.step_or_phase = tp.TurnParts.FIRST_STRIKE_DAMAGE
    game.give_player_priority(game.active_index())


def _combat_damage(game: "game_mod.Game"):
    print("Start: Combat Damage")
    game.step_or_phase = tp.TurnParts.COMBAT_DAMAGE
    game.give_player_priority(game.active_index())


def _end_combat(game: "game_mod.Game"):
    print("Start: End of Combat")
    game.step_or_phase = tp.TurnParts.END_COMBAT
    game.give_player_priority(game.active_index())


def _post_combat(game: "game_mod.Game"):
    print("Start: Postcombat Main")
    game.step_or_phase = tp.TurnParts.POSTCOMBAT_MAIN
    game.give_player_priority(game.active_index())


def _end_step(game: "game_mod.Game"):
    print("Start: End Step")
    game.step_or_phase = tp.TurnParts.END_STEP
    game.give_player_priority(game.active_index())


def _cleanup(game: "game_mod.Game"):
    print("Start: Cleanup")
    game.step_or_phase = tp.TurnParts.CLEANUP
    _untap(game)


_START_METHODS = (_untap, _upkeep, _draw, _pre_combat, _begin_combat,
                  _declare_attackers, _declare_blockers, _first_strike_damage,
                  _combat_damage, _end_combat, _post_combat, _end_step, _cleanup)


def start_next_step_or_phase(game, index: "tp.TurnParts"):
    # XXX this might fail if turn_parts' constants change (in type or meaning)
    _START_METHODS[index.value + 1](game)
