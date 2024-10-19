import random


class Player:
    def __init__(self):
        self.move = None

    def choose_move(self):
        pass

    def learn(self, opponent_move):
        pass


class AlwaysRockPlayer(Player):
    def choose_move(self):
        return 'rock'


class RandomPlayer(Player):
    def choose_move(self):
        return random.choice(['rock', 'paper', 'scissors'])


class MimicPlayer(Player):
    def __init__(self):
        super().__init__()
        self.opponent_move = None

    def choose_move(self):
        if self.opponent_move is None:
            return random.choice(['rock', 'paper', 'scissors'])
        else:
            return self.opponent_move

    def learn(self, opponent_move):
        self.opponent_move = opponent_move


class CyclePlayer(Player):
    def __init__(self):
        super().__init__()
        self.previous_move = None
        self.moves = ['rock', 'paper', 'scissors']
        self.move_index = 0

    def choose_move(self):
        if self.previous_move is None:
            return random.choice(self.moves)
        else:
            self.move_index = (self.move_index + 1) % 3
            return self.moves[self.move_index]

    def learn(self, opponent_move):
        self.previous_move = opponent_move


class HumanPlayer(Player):
    def __init__(self):
        super().__init__()

    def choose_opponent(self):
        while True:
            choice = input('Choose your opponent strategy:\n'
                           '1. RockPlayer\n'
                           '2. RandomPlayer\n'
                           '3. MimicPlayer\n'
                           '4. CyclePlayer: ')
            if choice in ['1', '2', '3', '4']:
                return int(choice)
            else:
                print("Invalid choice! Please enter a number between 1 and 4.")

    def choose_move(self):
        while True:
            move = input("Enter your move (rock, paper, scissors): ").lower()
            if move in ['rock', 'paper', 'scissors']:
                return move
            else:
                print("Invalid move! enter 'rock', 'paper', or 'scissors'.")


class Game:
    def __init__(self, rounds=3):
        self.rounds = rounds
        self.players = []
        self.scores = []

    def initialize_players(self):
        human_player = HumanPlayer()
        opponent_choice = human_player.choose_opponent()
        self.players.append(AlwaysRockPlayer() if opponent_choice == 1 else
                            RandomPlayer() if opponent_choice == 2 else
                            MimicPlayer() if opponent_choice == 3 else
                            CyclePlayer())
        self.players.append(human_player)
        self.scores = [0] * len(self.players)

    def play_round(self):
        for i, player in enumerate(self.players):
            opponent_moves = [p.move for p in self.players[:i]]
            player.learn(random.choice(opponent_moves)
                         if opponent_moves else None)
            player.move = player.choose_move()

    def determine_winner(self, move1, move2):
        if move1 == move2:
            return 0
        elif (move1 == 'rock' and move2 == 'scissors') or \
             (move1 == 'scissors' and move2 == 'paper') or \
             (move1 == 'paper' and move2 == 'rock'):
            return 1
        else:
            return -1

    def display_results(self, round_num):
        print(f"Round {round_num} Results:")
        for i, player in enumerate(self.players):
            print(f"Player {i + 1} played: {player.move}")
        print("")

    def update_scores(self, winner_index):
        if winner_index != 0:
            self.scores[winner_index - 1] += 1

    def display_scores(self):
        print("Current Scores:")
        for i, score in enumerate(self.scores):
            print(f"Player {i + 1}: {score}")
        print("")

    def display_final_scores(self):
        print("Final Scores:")
        for i, score in enumerate(self.scores):
            print(f"Player {i + 1}: {score}")
        print("")

    def play_game(self):
        print("Welcome to Rock Paper Scissors!")
        self.initialize_players()
        for round_num in range(1, self.rounds + 1):
            print(f"Round {round_num}:")
            self.play_round()
            self.display_results(round_num)
            moves = [player.move for player in self.players]
            for i, player in enumerate(self.players):
                winner_index = self.determine_winner(player.move, moves[i - 1])
                self.update_scores(winner_index)
            self.display_scores()
        self.display_final_scores()


if __name__ == "__main__":
    game = Game(rounds=3)
    game.play_game()
