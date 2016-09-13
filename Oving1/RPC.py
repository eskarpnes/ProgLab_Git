import random
class RockPaperScissors:
	def __init__(self):
		self.actions = ['rock', 'paper', 'scissors']
		
	def valid_action(self, act):
		return True if (act in self.actions) or (act in self.difficulties) else False
		
	# def random_act(self):
		# rand_act = random.randint(0,2)
		# self.update_last_played(rand_act)
		# return self.actions[rand_act]
		
	# def seq_act(self):
		# if self.last_played is None:
			# return self.actions[0]
		# else:
			# if self.last_played+1 >= len(self.actions):
				# self.last_played = 0
			# return self.actions[self.last_played+1]
		
	# def common_act(self):
		# pass
		
	# def history_act(self):
		# pass
	
	# def eq(self,r1,r2):
		# return True if r1==r2 else False
		
	# def compare(self, r1,r2): #true if r1 wins over r2
		# if self.eq(r1,r2):
			# print '>> Same hands!\n'
			# return False
		# elif (r1=='rock' and r2=='scissors') or (r1=='paper' and r2=='rock') or (r1=='scissors' and r2=='paper'):
			# print '>> Player 1 wins the round!\n'
			# return True
		# else:
			# print '>> Player 2 wins the round!\n'
			# return False