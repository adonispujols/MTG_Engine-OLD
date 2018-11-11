from src import game as game_mod
from src import player as player_mod


def special_untap(game: game_mod.Game, first_player: player_mod.Player):
    game.step_or_phase = 0
    # XXX ^ evil set? (along with rest of step_or_phase = x)
    # at start, no one is active, so we must directly make first player active.
    first_player.make_active()
    game.untap_all_of_player(first_player.index())
    upkeep(game)


def untap(game: game_mod.Game):
    game.step_or_phase = 0
    game.change_active_player_to_next()
    game.untap_all_of_player(game.active_player().index())
    upkeep(game)


def upkeep(game):
    game.step_or_phase = 1
    game.active_player().gain_priority()


def draw(game: game_mod.Game):
    game.step_or_phase = 2
    game.active_player().draw(1)
    game.active_player().gain_priority()


def pre_combat(game):
    game.step_or_phase = 3
    game.active_player().gain_priority()


def begin_combat(game):
    game.step_or_phase = 4
    game.active_player().gain_priority()


def declare_attackers(game):
    game.step_or_phase = 5
    game.active_player().gain_priority()


def declare_blockers(game):
    game.step_or_phase = 6
    game.active_player().gain_priority()


def first_strike_damage(game):
    game.step_or_phase = 7
    game.active_player().gain_priority()


def combat_damage(game):
    game.step_or_phase = 8
    game.active_player().gain_priority()


def end_combat(game):
    game.step_or_phase = 9
    game.active_player().gain_priority()


def post_combat(game):
    game.step_or_phase = 10
    game.active_player().gain_priority()


def end(game):
    game.step_or_phase = 11
    game.active_player().gain_priority()


def cleanup(game):
    game.step_or_phase = 12
    untap(game)


START_METHODS = (upkeep, draw, pre_combat, begin_combat, declare_attackers,
                 declare_blockers, first_strike_damage, combat_damage,
                 end_combat, post_combat, end, cleanup, untap)


def start_next_step_or_phase(step_or_phase, game):
    START_METHODS[step_or_phase](game)
