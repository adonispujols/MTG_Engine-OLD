# TODO
START_METHODS = ()


def start_next_step_or_phase(step_or_phase, game):
    # TODO
    pass


def special_untap(game, first_player):
    """

    :type first_player: player.Player
    """
    game.step_or_phase = 0
    # XXX ^evil set? (along with rest of step_or_phase = x)
    # first_player.

# store as tuple!!:

# # list holding method names as strings
# const start_methods = ["upkeep", "draw",
# 		"pre_combat_phase_start", "begin_combat", "begin_combat",
# 		"declare_attackers", "first_strike_damage",
# 		"combat_damage", "end_combat", "post_combat_phase_start",
# 		"end", "cleanup", "untap"]
#
# func start_next_step_or_phase(step_or_phase, game):
# 	call(start_methods[step_or_phase], game) # START ON UPKEEP, untap last
#
# func special_untap(game, first_player):
# 	game.step_or_phase = 0
# 	# XXX ^ evil set (along with rest of step_or_phase = x)
# 	first_player.make_active()
# 	game.get_active_player().untap
# 	upkeep(game)
#
# func untap(game):
# 	game.step_or_phase = 0
# 	game.change_active_player_to_next()
# 	game.untap_all_of_player(get_active_player().index())
# 	upkeep(game)
#
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
