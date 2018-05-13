import random
import game as game_classes

class Player:
	def __init__(self, symbol):
		self.symbol = symbol

	def get_move(self, game):
		return None

class Human(Player):
	def get_move(self, game):
		print(game)
		move = None
		while not move or not game.is_valid_move(move):
			if move:
				print("Invalid move! Try again")
			try:
				board = int(input("Choose a board, 1-9: "))-1
				square = int(input("Choose a square, 1-9: "))-1
				move = game_classes.Move((board//3, board%3), (square//3, square%3), self.symbol)
				print(move)
			except:
				print("Invalid input! Try again")
				move = None
		return move


class Dumbo(Player):
	def get_move(self, game):
		moves = game.get_valid_moves()
		if len(moves) > 0:
			return random.choice(moves)
		else:
			return None

class Maximinian(Player):
	def __init__(self, symbol, evaluator, depth):
		Player.__init__(self, symbol)
		self.depth = depth
		self.evaluator = evaluator

	def get_move(self, game):
		moves = game.get_valid_moves()

		bestVal = -float('inf')
		bestMoves = [None]
		board_to_move = game.board_to_move

		for move in moves:
			game.move(move)
			val = self.minimax(game, self.depth, -float("inf"), float("inf"), True)
			if val > bestVal:
				bestVal = val
				bestMoves = [move]
			if val == bestVal:
				bestMoves.append(move)
			game.undo_move(move, board_to_move)

		return random.choice(bestMoves)

	def minimax(self, game, depth, a, b, maximize):
		if depth == 0 or game.winner:
			return self.evaluator(game, self.symbol)

		moves = game.get_valid_moves()
		board_to_move = game.board_to_move

		if maximize:
			bestVal = -float("inf")
			for move in moves:
				game.move(move)
				v = self.minimax(game, depth-1, a, b, False)
				bestVal = max(bestVal, v)
				a = max(a, bestVal)
				game.undo_move(move, board_to_move)
				if b <= a:
					break
		else:
			bestVal = float("inf")
			for move in moves:
				game.move(move)
				v = self.minimax(game, depth-1, a, b, True)
				bestVal = min(bestVal, v)
				b = min(b, bestVal)
				game.undo_move(move, board_to_move)
				if b <= a:
					break

		return bestVal

def hval_bad(game, symbol):
	return 0

def hval_winloss(game, symbol):
	if game.winner == symbol:
		return 1
	elif game.winner:
		return -1
	else:
		return 0

def hval_boardwins(game, symbol):
	if game.winner == symbol:
		return 1
	elif game.winner:
		return -1

	won_board_differential = 0
	for row in game.meta_board.squares:
		for square in row:
			if square == symbol:
				won_board_differential += .1
			elif square != " ":
				won_board_differential -= .1

	return won_board_differential