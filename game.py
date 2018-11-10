class Game:
    def __init__(self, players, first_player):
        self.players = players
        self.first_player = first_player
        # XXX should NOT hold first_player in memory (wasteful). how to get around it?
        self.step_or_phase = 0
        self.passes_count = 0
        self.battlefield = []
        for player in players:
            self.battlefield.append([])

"""
const TurnBasedActions = preload("turn_based_actions.gd")

# Initializing member vars on object creation
func _init(_players, _first_player):
	var Stack = load("stack.gd")
	# XXX ^ make class calls into constants?
	# XXX ^ preload class calls?
	stack = Stack.new()

func start_game():
	TurnBasedActions.special_untap_step_start(self, get_player(first_player))

func get_player(player_index):
	return players[player_index]

func get_active_player():
	for player in players:
		if player.is_active_player():
			return player

func get_player_due_priority():
	for player in players:
		if player.is_due_priority():
			return player

func pass_priority(player):
	if !player.has_priority():
		print("ERROR: Passed without priority. Player: ", player.index())
		get_tree().quit()
	player.lose_priority()
	if all_players_passed_no_actions(player.index()) and stack.empty():
		empty_mana_pools()
		TurnBasedActions.start_next_step_or_phase(step_or_phase, this)
	else:
		if !stack.empty():
			stack.resolve_next()
		get_player((player.get_index + 1) % players.size()).gain_priority()

func all_players_passed_no_actions(player_index):
	var passed = false
	if (get_player((player.get_index + 1) % players.size()).is_active_player()):
		if passes_count == players.size():
			passed = true
		passes_count = 0
	else:
		passes_count += 1

func step_or_phase():
	return step_or_phase

func change_active_player_to_next():
	previous_active_player_index = get_active_player.get_index()
	get_active_player.make_nonactive()
	get_player((player.get_index + 1) % players.size()).make_active()

func empty_mana_pools():
	for player in players:
		player.mana_pool.clear()

func get_permanents_of_player(player_index):
	return battefield[player_index]

func put_on_battlefield(card, player):
	battefield[player.index()].append(card_object)
	player.hand.remove(card.index())

"""