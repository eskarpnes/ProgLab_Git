import random
from auto import AutoPlay
class Player:
	def __init__(self, name='Default'):
		self.auto = AutoPlay(self)
		self.actions = ['rock', 'paper', 'scissors']
		self.events = {
			1: self.auto.random_act,
			2: self.auto.seq_act,
			3: self.auto.common_act,
			4: self.auto.history_act
		}
		self.intelligence = {
			0: 'None',
			1: 'Random',
			2: 'Sequential',
			3: 'Most common',
			4: 'Historical (AI)'
		}
		self.name = name
		self.previous_plays = []
		self.last_played = None
		self.opponent = None
		self.remember = 2
		self.points = 0.0
		self.intel = 0
		self.score_table = []
		
	def valid_action(self, act):
		return True if act in self.actions else False
		
	def play(self, act):
		if self.valid_action(act):
			self.previous_plays.append(act)
			#print self.get_name(), 'played', act
			self.update_last_play()
		else:
			print 'Invalid action!'
		#print ''
			
	def auto_play(self, level):
		if level > 0 and level < 5:
			self.play(self.events[level]())
		else:
			print 'Invalid levelligence level!'

	def set_opponent(self, opponent):
		if opponent != self.opponent:
			self.opponent = opponent
		
	def get_result(self, n):
		return self.previous_plays[n]
	
	def get_name(self):
		return self.name
		
	def get_plays(self):
		print self.get_name(),':\t',
		return ', '.join(self.previous_plays)
		
	def get_size(self):
		return len(self.previous_plays)
		
	def get_intel(self):
		return self.intelligence[self.intel]
		
	def update_last_play(self):
		self.last_played = self.previous_plays[len(self.previous_plays)-1]
