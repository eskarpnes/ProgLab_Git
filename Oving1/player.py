import random

class Player:
	def __init__(self, name='Default'):
		self.actions = ['rock', 'paper', 'scissors']
		self.events = {
			1: self.random_act,
			2: self.seq_act,
			3: self.common_act,
			4: self.history_act
		}
		self.name = name
		self.previous_plays = []
		self.last_played = None
		self.opponent = None
		self.remember = 2
		
	def valid_action(self, act):
		return True if act in self.actions else False
		
	def play(self, act):
		if self.valid_action(act):
			self.previous_plays.append(act)
			print self.get_name(), 'played', act
			self.update_last_play()
		else:
			print 'Invalid action!'
		print ''
			
	def auto_play(self, intel):
		if intel > 0 and intel < 5:
			act = self.events[intel]()
			self.play(act)
		else:
			print 'Invalid intelligence level!'
	
	def get_plays(self):
		print self.get_name(),':\t',
		return ', '.join(self.previous_plays)
		
	def get_result(self, n):
		return self.previous_plays[n]
		
	def get_name(self):
		return self.name
		
	def set_opponent(self, opponent):
		if opponent != self.opponent:
			self.opponent = opponent
		
	# TYPES OF PLAYING
	def update_last_play(self):
		#will simply extract the last item in the previous plays list
		self.last_played = self.previous_plays[len(self.previous_plays)-1]
		
	#start and end to later specify intervals
	def random_act(self, start=0,step=1,stop=2):
		rand_act = random.randrange(start,stop+1,step)
		#rand_act = random.choice(numbers)
		print 'RANDOM! Got',rand_act
		return self.actions[rand_act]

	def seq_act(self):
		print 'SEQUENCE! Previously played:',self.last_played,', now playing:',
		if self.last_played is None:
			print self.actions[0]
			return self.actions[0]
		else:
			ind = self.actions.index(self.last_played)
			if ind+1 >= len(self.actions):
				ind = -1
			print self.actions[ind+1]
			return self.actions[ind+1]
	
	def common_act(self):
		print 'COMMON!',
		if len(self.previous_plays)==0:
			print '...but no previous plays were found. Playing a random number.'
			return self.random_act()
		r,p,s=0,0,0
		for item in self.previous_plays:
			if item == 'rock': r+=1
			elif item == 'paper': p+=1
			else: s+=1
		# in case duplicates shouldn't return rock
		# if r==p: return self.random_act(0,1,1)
		# elif r==s: return self.random_act(0,2,2)
		# elif s==p: return self.random_act(1,1,2)
		typical = list((r,p,s))
		ind = typical.index(max(typical))
		print self.get_plays(),'\t',typical
		return self.actions[ind]
		
	def history_act(self):
		print 'HISTORY! ('+self.get_name()+')'
		print self.get_plays()

		def get_opponent_play(ind):
			return self.opponent.get_result(ind)
		
		r,p,s = 0,0,0
		def counter_next_play(ind, seq):
			valid_plays = list((r,p,s))
			print 'Found these valid plays for (R/P/S):',valid_plays
			most_played = self.actions[valid_plays.index(max(valid_plays))]
			print 'Opponent usually played',most_played,'after your',' and '.join(seq)			
			play = None
			if most_played == 'rock': play = 'paper'
			elif most_played == 'paper': play = 'scissors'
			else: play = 'rock'
			return play
					
		sub_sequence = []
		similar_plays = 0
		for i in range(len(self.previous_plays)-self.remember, len(self.previous_plays)):
			sub_sequence.append(self.previous_plays[i])			
		print '-->Subsequence for "husk='+str(self.remember),'" =',sub_sequence
		print self.opponent.get_plays()
		valid_sequence = True
		found_play = False
		k = 0
		for k in range(len(self.previous_plays)-self.remember): #don't check the (AMOUNT) last items
			#find the first match:
			if self.get_result(k)==sub_sequence[0]:
				valid_sequence = True
				for j in range(1,len(sub_sequence)):
					if self.get_result(k+j)!=sub_sequence[j]:
						valid_sequence = False
				if valid_sequence:
					found_play = True
					print 'valid sequence at pos:',k
					tmp = self.opponent.get_result(k+self.remember)
					if tmp=='rock': r+=1
					elif tmp=='paper': p+=1
					else: s+=1
			
		if found_play:
			return counter_next_play(k+self.remember, sub_sequence)
		else:
			print "Invalid sequence. Giving up, going random."
			return random_act()