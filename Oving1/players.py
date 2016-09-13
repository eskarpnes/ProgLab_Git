'''
Rock paper scissors
2 players each play between 3 actions

First phase (starting):
each player will have
determined their choice without disclosure.

Second phase:
both players reveal their choice
calculate score and decide the winner
'''

from player import Player

class PlayerController:
	def __init__(self, amount_players=2):
		#instance with 2 players
		#self.rpc = RockPaperScissors()
		self.players = []
		self.rounds_completed = 0		
		for i in range(amount_players):
			p_name = 'Player '+str(1+i)
			self.players.append(Player(p_name))
		self.active_player = 0 #holds the current player
		#self.get_names()
		
		
	def play(self, act):
		self.players[self.active_player].play(act)
		self.next_player()
			
	def auto_play(self, difficulty):
		self.set_player_opponent()
		self.players[self.active_player].auto_play(difficulty)
		self.next_player()
		
	def set_player_opponent(self):
		opponent = self.players[1] if self.active_player == 0 else self.players[0]
		#print 'Player =',self.active_player,'-> Opponent =',opponent
		self.players[self.active_player].set_opponent(opponent)
	
	def next_player(self):
		if self.active_player >= len(self.players)-1:
			self.round_finished()
			self.active_player = 0
		else:
			self.active_player+=1

	def round_finished(self):
		print '### ROUND',self.rounds_completed,'OVER! ####'
		self.compare(self.get_result(0), self.get_result(1))
		self.rounds_completed += 1
		print ''
		
	def get_result(self, player):
		return self.players[player].get_result(self.rounds_completed)
		
	def get_names(self):
		print '\nCurrent players below\n'
		for i in range(len(self.players)):
			if i==self.active_player:
				print 'Active:\t',
			else:
				print '\t',
			print self.players[i].get_name()
		print '\n'
		
	#compare results
	def eq(self,r1,r2):
		return True if r1==r2 else False
		
	def compare(self, r1,r2): #true if r1 wins over r2
		if self.eq(r1,r2):
			print '>> Same hands!\n'
			return False
		elif (r1=='rock' and r2=='scissors') or (r1=='paper' and r2=='rock') or (r1=='scissors' and r2=='paper'):
			print '>> Player 1 wins the round!\n'
			return True
		else:
			print '>> Player 2 wins the round!\n'
			return False