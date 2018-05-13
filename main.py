import game
import ai
import random
import time
import progressbar

def gen_random_square():
	r = random.randint(1,3)
	if r == 1:
		return " "
	elif r == 2:
		return "X"
	else:
		return "O"

def gen_random_board():
	return game.Board([[gen_random_square(), gen_random_square(), gen_random_square()] for _ in range(3)])

def gen_random_game():
	return game.Game([[gen_random_board(), gen_random_board(), gen_random_board()] for _ in range(3)])

def get_stats(p1, p2, num_games):
	bar = progressbar.bar.ProgressBar(max_value=num_games)
	start = time.time()
	wins = {}
	for c in range(num_games):
		bar.update(c)
		g = game.Game()
		while g.winner == None:
			if g.turn == "X":
				move = p1.get_move(g)
			else:
				move = p2.get_move(g)
			if move:
				g.move(move)
			else:
				g.winner = "CAT"
		wins[g.winner] = wins.get(g.winner, 0) + 1
	elapsed = time.time() - start
	games_per_second = round(num_games / elapsed, 3)
	bar.finish()

	print("games/second: " + str(games_per_second))
	print("Win distribution: ")
	for key in wins:
		print(key + ": " + str(wins[key]))

def test_game(p1, p2, g):
	while not g.winner:
		if g.turn == "X":
			move = p1.get_move(g)
		else:
			move = p2.get_move(g)
		if move:
			g.move(move)
		else:
			g.winner = "CAT"

		print(g)

	print(g.winner)
	
p2 = ai.Maximinian("O", ai.hval_boardwins, 2)
p1 = ai.Maximinian("X", ai.hval_winloss, 2)

get_stats(p1, p2, 100)