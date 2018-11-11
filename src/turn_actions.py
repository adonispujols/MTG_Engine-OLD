from src import game as game_mod
from src import player as player_mod


def special_untap(game: game_mod.Game, first_player: player_mod.Player):
    game.step_or_phase = 0
    # XXX ^evil set? (along with rest of step_or_phase = x)
    # at start, no one is active, so we must directly make first player active.
    first_player.make_active()
    game.untap_all_of_player(first_player.index())
    upkeep(game)

# func upkeep(game):
# 	game.step_or_phase = 1
# 	game.get_active_player.gain_priority()
#
# func draw(game):
# 	game.step_or_phase = 2
# 	game.get_active_player().draw(1)
# 	game.get_active_player.gain_priority()
#
# func pre_combat_phase_start(game):
#     game.step_or_phase = 3
#     game.get_active_player.gain_priority()
#
# func begin_combat(game):
#     game.step_or_phase = 4
#     game.get_active_player.gain_priority()
#
# func declare_attackers(game):
#     game.step_or_phase = 5
#     game.get_active_player.gain_priority()
#
# func declare_blockers(game):
#     game.step_or_phase = 6
#     game.get_active_player.gain_priority()
#
# func first_strike_damage(game):
#     game.step_or_phase = 7
#     game.get_active_player.gain_priority()
#
# func combat_damage(game):
#     game.step_or_phase = 8
#     game.get_active_player.gain_priority()
#
# func end_combat(game):
#     game.step_or_phase = 9
#     game.get_active_player.gain_priority()
#
# func post_combat_phase_start(game):
#     game.step_or_phase = 10
#     game.get_active_player.gain_priority()
#
# func end(game):
#     game.step_or_phase = 11
#     game.get_active_player.gain_priority()
#
# func cleanup(game):
#     game.step_or_phase = 12
#     untap(game)
# func untap(game):
# 	game.step_or_phase = 0
# 	game.change_active_player_to_next()
# 	game.untap_all_of_player(get_active_player().index())
# 	upkeep(game)

def untap(game):
    # TODO
    game.step_or_phase = 0
    game.change_active_player_to_next()
    game.untap_all_of_player(game.active_player().)

def upkeep(game):
    # TODO
    pass

def draw(game):
    # TODO
    pass

def pre_combat(game):
    # TODO
    pass

def begin_combat():
    # TODO
    pass

def declare_attackers(game):
    # TODO
    pass

def declare_blockers(game):
    # TODO
    pass

def first_strike_damage(game):
    # TODO
    pass

def combat_damage(game):
    # TODO
    pass

def end_combat(game):
    # TODO
    pass

def post_combat(game):
    # TODO
    pass

def end(game):
    # TODO
    pass

def cleanup(game):
    # TODO
    pass


START_METHODS = (upkeep(), draw(), pre_combat(), begin_combat(),
                 declare_attackers(), declare_blockers(), first_strike_damage(),
                 combat_damage(), end_combat(), post_combat(), end(), cleanup(),
                 untap())


def start_next_step_or_phase(step_or_phase, game):
    START_METHODS[step_or_phase](game)
