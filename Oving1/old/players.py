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
import numpy as np
import matplotlib.pyplot as plt
from player import Player
from game import GameController
class PlayerController:
	def __init__(self, amount_players=2):
		# default instance has 2 players
		self.players = []
		self.rounds_completed = 0
		self.active_player = 0 #holds the current player
		self.print_enabled = True
		self.winner = None
		
		game = GameController(self)
		self.end()
		self.update_plot()
		
	def _print(self, txt):
		if self.print_enabled:
			print txt
		
	def update_plot(self):
		fig = plt.figure()
		x_ = np.arange(self.rounds_completed)
		plt.plot(x_,self.players[0].score_table)
		plt.plot(x_,self.players[1].score_table)
		
		plt.xlabel('Rounds played')
		plt.ylabel('Points')
		plt.title('Rock-Paper-Scissors. '+self.winner)
		plt.legend([self.players[0].get_name()+' = '+self.players[0].get_intel(),
					self.players[1].get_name()+' = '+self.players[1].get_intel()],
					loc = 'upper left')
		
		plt.show()
		# self.p1_scores.set_xdata(numpy.append(self.p1_scores.get_xdata(), self.players[0].points))
		# self.p2_scores.set_xdata(numpy.append(self.p2_scores.get_xdata(), self.players[1].points))
		
		# y_height = self.players[0].points + self.players[1].points
		# self.p1_scores.set_ydata(numpy.append(self.p1_scores.get_ydata(), y_height))
		# self.p2_scores.set_ydata(numpy.append(self.p2_scores.get_ydata(), y_height))
		
		# self.p1_scores.ax.relim()
		# self.p2_scores.ax.relim()
		# self.p1_scores.draw()
		# self.p2_scores.draw()
		
	def add_player(self,player):
		self.players.append(Player(player))
				
	def play(self, act):
		self.players[self.active_player].play(act)
		self.next_player()
			
	def auto_play(self, difficulty):
		self.set_player_opponent()
		self.players[self.active_player].auto_play(difficulty)
		self.next_player()
		
	def set_player_opponent(self):
		opponent = self.players[1] if self.active_player == 0 else self.players[0]
		self.players[self.active_player].set_opponent(opponent)
	
	def next_player(self):
		if self.active_player >= len(self.players)-1:
			self.round_finished()
			self.active_player = 0
		else:
			self.active_player+=1

	def round_finished(self):
		self._print( '### ROUND'+str(self.rounds_completed+1)+'OVER! ####' )
		self.compare(self.get_result(0), self.get_result(1))
		self.rounds_completed += 1
		self._print( 'Points:' )
		for pl in self.players:
			self._print( pl.get_name()+':'+str(pl.points ))
		self._print(' ')
		
	def get_result(self, player):
		return self.players[player].get_result(self.rounds_completed)
		
	def get_names(self):
		self._print( '\nCurrent players below\n' )
		for i in range(len(self.players)):
			if i==self.active_player:
				self._print( 'Active:\t',)
			else:
				self._print( '\t', )
			self._print( self.players[i].get_name())
		self._print( '\n' )
	
	def give_points(self, player, points):
		self.players[player].points+=points
	
	def get_points(self, player):
		return self.players[player].points
			
	def compare(self, r1,r2): #true if r1 wins over r2
		self.players[0].score_table.append(self.players[0].points)
		self.players[1].score_table.append(self.players[1].points)
		if r1==r2:
			self._print( '>> Same hands!\n')
			self.give_points(0,0.5)
			self.give_points(1,0.5)
		elif (r1=='rock' and r2=='scissors') or (r1=='paper' and r2=='rock') or (r1=='scissors' and r2=='paper'):
			self._print( '>>'+self.players[0].get_name()+' wins the round! <<\n')
			self.give_points(0,1)
		else:
			self._print( '>>'+self.players[1].get_name()+' wins the round! <<\n')
			self.give_points(1,1)
			
	def end(self):
		print '*** Game over! ***'
		player = self.get_points(0)
		p2 = self.get_points(1)
		if player==p2:
			self.winner = 'Equal scores!'
		elif player>p2:
			self.winner = self.players[0].get_name()+' won!'
		else:
			self.winner = self.players[1].get_name()+' won!'
		print self.winner