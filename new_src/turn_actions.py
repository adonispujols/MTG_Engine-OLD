from new_src import game as game_mod
from new_src import turn_parts as tp
# XXX avoid importing just for type checking (risks cyclic importing)


def first_untap_of_game(game: "game_mod.Game", first_player):
    game.g
    print("Start of First Untap Step")
    game.step_or_phase = tp.TurnParts.UNTAP
    # at start, no one is active, so we must directly make 1st player active.
    game.players[first_player].make_active()
    print("Active Player:", first_player)
    # TBA = "Turn-Based Action", SBA = "State-Based Action"
    print("TBA: Untap all")
    # XXX should game be doing this, or should we get the active player,
    # ^ then untap all their stuff (since it makes sense here)?
    game.untap_all_of_active()
    _upkeep(game)


def _untap(game: game_mod.Game):
    print("Start of Untap Step")
    game.step_or_phase = tp.TurnParts.UNTAP
    # change active player to the next
    prev_active = game.active_index()
    game.players[prev_active].make_inactive()
    new_active = (prev_active + 1) % len(game.players)
    game.players[new_active].make_active()
    print("Active Player:", new_active + 1)
    print("TBA: Untap all")
    game.untap_all_of_active()
    _upkeep(game)


def _upkeep(game: game_mod.Game):
    print("Start of Upkeep Step")
    game.step_or_phase = tp.TurnParts.UPKEEP
    # give the active player priority
    game.give_player_priority(game.active_index())


def _draw(game: game_mod.Game):
    # TODO must skip if 1st player's 1st draw (if 1v1 or 2-headed giant)
    print("Start of Draw Step")
    game.step_or_phase = tp.TurnParts.DRAW
    print("TBA: Draw")
    game.active_player().draw()
    game.give_player_priority(game.active_index())


def _pre_combat(game: game_mod.Game):
    print("Start of Precombat Main Phase")
    game.step_or_phase = tp.TurnParts.PRE_COMBAT
    game.give_player_priority(game.active_index())


def _begin_combat(game: game_mod.Game):
    print("Start of Beginning of Combat Step")
    game.step_or_phase = tp.TurnParts.BEGIN_COMBAT
    game.give_player_priority(game.active_index())


def _declare_attackers(game: game_mod.Game):
    print("Start of Declare Attackers Step")
    # TODO need to skip to end if no attackers declared
    game.step_or_phase = tp.TurnParts.DECLARE_ATTACKERS
    game.give_player_priority(game.active_index())


def _declare_blockers(game: game_mod.Game):
    print("Start of Declare Blockers Step")
    game.step_or_phase = tp.TurnParts.DECLARE_BLOCKERS
    game.give_player_priority(game.active_index())


def _first_strike_damage(game: game_mod.Game):
    print("Start of First Strike Damage Step")
    # TODO need to skip to combat damage if no creatures wih first strike
    # ^ on either side of the field
    game.step_or_phase = tp.TurnParts.FIRST_STRIKE_DAMAGE
    game.give_player_priority(game.active_index())


def _combat_damage(game: game_mod.Game):
    print("Start of Combat Damage Step")
    game.step_or_phase = tp.TurnParts.COMBAT_DAMAGE
    game.give_player_priority(game.active_index())


def _end_combat(game: game_mod.Game):
    print("Start of End of Combat Step")
    game.step_or_phase = tp.TurnParts.END_COMBAT
    game.give_player_priority(game.active_index())


def _post_combat(game: game_mod.Game):
    print("Start of Postcombat Main Phase")
    game.step_or_phase = tp.TurnParts.POST_COMBAT
    game.give_player_priority(game.active_index())


def _end(game: game_mod.Game):
    print("Start of End Step")
    game.step_or_phase = tp.TurnParts.END_COMBAT
    game.give_player_priority(game.active_index())


def _cleanup(game: game_mod.Game):
    print("Start of Cleanup Step")
    game.step_or_phase = tp.TurnParts.CLEANUP
    _untap(game)


_START_METHODS = (_untap, _upkeep, _draw, _pre_combat, _begin_combat,
                  _declare_attackers, _declare_blockers, _first_strike_damage,
                  _combat_damage, _end_combat, _post_combat, _end, _cleanup)


def start_next_step_or_phase(game, index):
    _START_METHODS[index + 1](game)
