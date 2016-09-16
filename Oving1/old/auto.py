import random

class AutoPlay:
	def __init__(self, player):
		self.player = player
		self.actions = ['rock', 'paper', 'scissors']

	def random_act(self, start=0,step=1,stop=2):
		rand_act = random.randrange(start,stop+1,step)
		#print 'RANDOM! -->',rand_act
		return self.actions[rand_act]
		
	def seq_act(self):
		#print 'SEQUENCE! Previously played:',self.player.last_played,', now playing:',
		if self.player.last_played is None:
			#print self.actions[0]
			return self.actions[0]
		else:
			ind = self.actions.index(self.player.last_played)
			if ind+1 >= len(self.actions):
				ind = -1
			#print self.actions[ind+1]
			return self.actions[ind+1]
		
	def common_act(self):
		#print 'COMMON!',
		if len(self.player.previous_plays)==0:
			#print '...No previous plays were found. Playing a random number.'
			return self.random_act()
		r,p,s=0,0,0
		for item in self.player.opponent.previous_plays:
			if item == 'rock': r+=1
			elif item == 'paper': p+=1
			else: s+=1
		# in case duplicates shouldn't return rock
		# if r==p: return self.random_act(0,1,1)
		# elif r==s: return self.random_act(0,2,2)
		# elif s==p: return self.random_act(1,1,2)
		#typical = list((r,p,s))
		#ind = typical.index(max(typical))
		return self.counter_next_play(list((r,p,s)))
		#return self.actions[ind]
		
	def counter_next_play(self, plays): #,seq
		#print 'R/P/S:',plays
		most_played = self.actions[plays.index(max(plays))]
		##print 'Opponent usually played',most_played,'after your',' and '.join(seq)			
		play = None
		if most_played == 'rock': play = 'paper'
		elif most_played == 'paper': play = 'scissors'
		else: play = 'rock'
		return play
		
	def history_act(self):
		#print 'HISTORY! ('+self.player.get_name()+')'
		
		def get_opponent_play(ind):
			return self.player.opponent.get_result(ind)
		
		r,p,s = 0,0,0
		sub_sequence = []
		if self.player.get_size()<self.player.remember+1:
			#print 'Cannot instantiate a history-based intelligence...\n...not enough plays have been made for a lookback-size of',self.player.remember
			return self.random_act()
		##print self.player.get_plays()
		for i in range(len(self.player.previous_plays)-self.player.remember, len(self.player.previous_plays)):
			sub_sequence.append(self.player.previous_plays[i])			
		##print '-->Subsequence of size',self.player.remember,':',sub_sequence
		##print self.player.opponent.get_plays()
		
		valid_sequence = True
		found_play = False
		k = 0
		# don't check the (AMOUNT) last items
		for k in range(len(self.player.previous_plays)-self.player.remember):
			# find the first match:
			if self.player.get_result(k)==sub_sequence[0]:
				valid_sequence = True
				# find the remaining matches in the sequence list
				for j in range(1,len(sub_sequence)):
					if self.player.get_result(k+j)!=sub_sequence[j]:
						valid_sequence = False
				if valid_sequence:
					found_play = True
					##print '...valid sequence at index ',k
					# increases each play by one, later compare which one was most common
					tmp = self.player.opponent.get_result(k+self.player.remember)
					if tmp=='rock': r+=1
					elif tmp=='paper': p+=1
					else: s+=1
			
		if found_play:
			return self.counter_next_play(list((r,p,s)))
		else:
			#print "Invalid sequence. Giving up, going random."
			return self.random_act()