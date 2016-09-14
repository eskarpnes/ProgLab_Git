class GameController:
	def __init__(self, pc):
		print 'Game modes:\n1) Player vs Computer\n2) Computer vs Computer'
		game_mode = None
		while True:
			game_mode = input('>')
			if (game_mode == 1 or game_mode == 2):
				break
			else:
				print 'Invalid mode. Try again...'
		if game_mode == 1:
			player = raw_input('Enter your name: ')
			player = player.title()
			pc.add_player(player)
			pc.add_player('Computer')
			print "\nSelect the computer's intelligence:\n1) Random\n2) Sequential\n3) Most common\n4) History (AI)"
			difficulty = input('>')
			print '...'+player+', prepare to play vs the Computer!'
			
			while True:
				act = raw_input('Your play is... ')
				if pc.players[0].valid_action(act):
					pc.play(act)
					pc.auto_play(difficulty)
				elif act == 'quit':
					break
				else:
					print 'Invalid action. Try again:'
		elif game_mode == 2:
			pc.add_player('John')
			pc.add_player('Anna')

			print 'Initializing robots John and Anna...'
			print "\nIntelligence levels:\n1) Random\n2) Sequential\n3) Most common\n4) History (AI)"
			r1, r2 = 0,0
			r1_smart, r2_smart = 0,0
			r1 = input("Select John's intelligence level: ")
			if r1==4:
				print 'On a scale from 1 to 4...'
				r1_smart = input ('...How smart is '+pc.players[0].get_name()+'? ')
				pc.players[0].remember=r1_smart
			r2 = input("Select Anna's intelligence level: ")
			if r2==4:
				print 'On a scale from 1 to 4...'
				r2_smart = input ('...How smart is '+pc.players[1].get_name()+'? ')
				pc.players[1].remember=r2_smart
			if r1_smart == r2_smart:
				print pc.players[0].get_name(),'is just as smart as',pc.players[1].get_name()
			elif r1_smart > r2_smart:
				print pc.players[0].get_name(),'outsmarts',pc.players[1].get_name()
			else:
				print pc.players[1].get_name(),'outsmarts',pc.players[0].get_name()
			
			pc.players[0].intel = r1
			pc.players[1].intel = r2
			
			time_test = input('Run for an amount of rounds (enter as number), or control it manually? (Leave blank for manual) ')
			if time_test!='' and isinstance(time_test, (int, long)):
				pc.print_enabled = False
				for i in range(time_test):
					pc.auto_play(r1)
					pc.auto_play(r2)
			else:
				print '...Ready! (Type "end" to quit the game)\n'
				while True:
					act = raw_input('Press enter for next round ')
					pc.auto_play(r1)
					pc.auto_play(r2)
					if act == 'end':
						break
						