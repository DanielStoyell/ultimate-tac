import random

class AI:
	def __init__(self, symbol):
		self.symbol = symbol

	def get_move(self, game):
		return None

	def get_heuristic_value(self, game):
		return 0

class Dumbo(AI):
	def get_move(self, game):
		moves = game.get_valid_moves()
		if len(moves) > 0:
			return random.choice(moves)
		else:
			return None

class Maximinian(AI):
	def __init__(self, symbol, evaluator, depth):
		AI.__init__(self, symbol)
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

	def get_heuristic_value(self, game):
		if game.winner == self.symbol:
			return 1
		elif game.winner:
			return -1
		else:
			return 

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