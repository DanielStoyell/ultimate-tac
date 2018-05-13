class Game:
	def __init__(self, boards=None, board_to_move=None, turn="X"):
		if boards:
			self.boards = boards
			self.meta_board = Board([[row[0].winner, row[1].winner, row[2].winner] for row in self.boards])
		else:
			self.boards = [[Board(), Board(), Board()] for _ in range(3)]
			self.meta_board = Board()

		self.board_to_move = board_to_move
		self.turn = turn
		self.winner = self.meta_board.winner

	def is_valid_move(self, move):
		if self.board_to_move and self.board_to_move != move.board:	
			return False
		if self.get_board(move.board).winner is not None:
			return False
		if self.get_board(move.board).get_square(move.square) is None:
			return False
		if self.turn != move.symbol:
			return False

		return True

	def move(self, move):
		assert self.is_valid_move(move)

		board = self.get_board(move.board)
		board.set_square(move.square, move.symbol)
		if board.winner:
			self.meta_board.set_square(move.board, board.winner)
			if self.meta_board.is_cat():
				self.winner = "CAT"
			else:
				self.winner = self.meta_board.winner

		sent_board = self.get_board(move.square)
		if sent_board.winner or sent_board.is_full():
			self.board_to_move = None
		else:
			self.board_to_move = move.square

		if self.turn == "X":
			self.turn = "O"
		else:
			self.turn = "X"

	def undo_move(self, move, board_to_move):
		board = self.get_board(move.board)
		board.set_square(move.square, " ")
		if board.winner == None:
			self.meta_board.set_square(move.board, " ")
		else:
			self.meta_board.set_square(move.board, board.winner)

		if self.meta_board.is_cat():
			self.winner = "CAT"
		else:
			self.winner = self.meta_board.winner

		self.board_to_move = board_to_move

		if self.turn == "X":
			self.turn = "O"
		else:
			self.turn = "X"


	def get_board(self, t):
		return self.boards[t[0]][t[1]]

	def get_valid_moves(self):
		moves = []
		if self.board_to_move:
			open_squares = self.get_board(self.board_to_move).get_open_squares()
			for square in open_squares:
				moves.append(Move(self.board_to_move, square, self.turn))
		else:
			for row in range(len(self.boards)):
				for col in range(len(self.boards[row])):
					board = self.boards[row][col]
					if not board.winner:
						board_loc = (row, col)
						open_squares = board.get_open_squares()
						for square in open_squares:
							moves.append(Move(board_loc, square, self.turn))

		return moves


	def __str__(self):
		out = ["Meta:\n"]
		out.append(self.meta_board.__str__())
		out.append("\n\n")
		out.append("\n\nMain:\n")
		for row in range(3):
			for sub_row in range(3):
				for col in range(3):
					for sub_col in range(3):
						out.append(self.boards[row][col].squares[sub_row][sub_col])
						if sub_col == 0 or sub_col == 1:
							out.append("|")
					if col == 0 or col == 1:
						out.append(" | ")
				out.append("\n")
				if sub_row == 0 or sub_row == 1:
					out.append("-+-+- | -+-+- | -+-+-\n")
			if row == 0 or row == 1:
				out.append("      |       |\n------+-------+------\n      |       |\n")
		return "".join(out)


class Board:
	def __init__(self, squares=None):
		if squares:
			self.squares = squares
			self.winner = self.get_winner()
			self.filled_squares = 0
			for row in self.squares:
				for square in row:
					if square != " ":
						self.filled_squares += 1
		else:
			self.squares = [[" ", " ", " "],
						   [" ", " ", " "],
						   [" ", " ", " "],]
			self.winner = None
			self.filled_squares = 0

	def __str__(self):
		out = []
		for row in range(3):
			for col in range(3):
				out.append(self.squares[row][col])
				if col == 0 or col == 1:
					out.append("|")
			if row == 0 or row == 1:
				out.append("\n-+-+-\n")
		return "".join(out)

	def get_winner(self):
		#check rows and columns
		for i in range(3):
			if (self.squares[i][0] != " " and 
					self.squares[i][0] == self.squares[i][1] and 
					self.squares[i][1] == self.squares[i][2]):
				return self.squares[i][0]
			if (self.squares[0][i] != " " and 
					self.squares[0][i] == self.squares[1][i] and 
					self.squares[1][i] == self.squares[2][i]):
				return self.squares[0][i]
		#check diags
		if (self.squares[0][0] != " " and
				self.squares[0][0] == self.squares[1][1] and
				self.squares[1][1] == self.squares[2][2]):
			return self.squares[0][0]
		if (self.squares[0][2] != " " and
				self.squares[0][2] == self.squares[1][1] and
				self.squares[1][1] == self.squares[2][0]):
			return self.squares[0][2]

		return None

	def is_cat(self):
		#check rows and columns
		for i in range(3):
			row_vals = set([self.squares[i][0], self.squares[i][1], self.squares[i][2]])
			row_vals.discard(" ")
			col_vals = set([self.squares[0][i], self.squares[1][i], self.squares[2][i]])
			col_vals.discard(" ")
			if len(row_vals) < 2 or len(col_vals) < 2:
				return False

		#check diags
		diag1_vals = set([self.squares[2][0], self.squares[1][1], self.squares[0][2]])
		diag1_vals.discard(" ")
		diag2_vals = set([self.squares[0][0], self.squares[1][1], self.squares[2][2]])
		diag2_vals.discard(" ")
		if len(diag1_vals) < 2 or len(diag2_vals) < 2:
			return False

		return True

	def get_square(self, s):
		return self.squares[s[0]][s[1]]

	def set_square(self, s, symbol):
		self.squares[s[0]][s[1]] = symbol
		self.winner = self.get_winner()
		if symbol != " ":
			self.filled_squares += 1
		else:
			self.filled_squares -= 1

	def is_full(self):
		return self.filled_squares == 9

	def get_open_squares(self):
		squares = []
		for row in range(len(self.squares)):
			for square in range(len(self.squares[row])):
				if self.squares[row][square] == " ":
					squares.append((row, square))

		return squares

class Move:
	def __init__(self, board, square, symbol):
		self.board = board
		self.square = square
		self.symbol = symbol

	def __str__(self):
		return "Board: " + str(self.board) + " | Square: " + str(self.square) + " | Symbol: " + self.symbol