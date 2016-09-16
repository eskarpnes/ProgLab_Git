from players import PlayerController as Game
from PySide.QtGui import *
from mainview import MainView
import sys

def main():
	print 'Starting Rock-Paper-Scissors\n'
	game = Game()
	# game.play('rock')
	# game.play('paper')
	# game.auto_play(1)
	# game.auto_play(1)
	# game.end()
	
	# app = QApplication(sys.argv)
	# win = MainView()
	# sys.exit(app.exec_())
	
if __name__=='__main__':
	main()
	