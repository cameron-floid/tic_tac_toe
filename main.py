class Player:

    def __init__(self):
        self.name = ""
        self.symbol = ""
        self.player_number = 0

    def get_name(self, player_num: int):
        self.name = input(f"What is your name player {player_num}? ")
        self.player_number = player_num

    def set_symbol(self):
        self.symbol = input("Enter a single character for your symbol: ")[0]  # get the first char in string


class Board:

    def __init__(self):

        self.EPS = " "  # empty position symbol (constant)
        self.USER_WON = "WON"  # user won (constant)
        self.NO_EVENT = "NONE"  # no win or invalid move, game continues (constant)
        self.INVALID_MOVE = "Invalid Move"  # invalid move (constant)

        self.rows = [
            [self.EPS, self.EPS, self.EPS],
            [self.EPS, self.EPS, self.EPS],
            [self.EPS, self.EPS, self.EPS]
        ]  # board

    def clear(self):
        # clear board from previous game
        self.rows = [
            [self.EPS, self.EPS, self.EPS],
            [self.EPS, self.EPS, self.EPS],
            [self.EPS, self.EPS, self.EPS]
        ]  # board

    def empty_position(self, x: int, y: int):
        try:
            if self.rows[x][y] == self.EPS:
                return True
            return False

        except IndexError:
            return False  # invalid position such as '3, 0'

    def still_possible_moves(self):
        """
        Check if there are still valid moves by checking for at least one empty position
        :return: StillPossibleMoves Bool
        """

        for row in self.rows:
            for col in row:
                if col == self.EPS:
                    return True

        return False

    def player_won(self, player: Player):

        # check the rows
        for i in range(3):
            streak = True
            for j in range(3):
                if self.rows[i][j] != player.symbol:
                    streak = False
                    break  # break out of the loop if there is no streak

            if streak:
                return True  # if this row is a win for the player, return True and exit the function

        # check the columns
        for i in range(3):
            streak = True
            for j in range(3):
                if self.rows[j][i] != player.symbol:
                    streak = False
                    break  # break out of the loop if there is no streak

            if streak:
                return True  # if this column is a win for the player, return True and exit the function

        # check major diagonal [(0,0), (1,1), (2,2)]
        major_streak = True
        for i in range(3):
            if self.rows[i][i] != player.symbol:
                major_streak = False
                break  # break out of the loop if there is no streak

        if major_streak:
            # if there is a winning streak (lineup) in the major diagonal, return True and exit the function
            return True

        # check minor diagonal [(0,2),(1,1),(2,0)] [(i, 2-i),...]
        minor_streak = True
        for i in range(3):
            if self.rows[i][2 - i] != player.symbol:
                minor_streak = False
                break  # break out of the loop if there is no streak

        if minor_streak:
            # if there is a winning streak (lineup) in the minor diagonal, return True and exit the function
            return True

        return False

    def update_board(self, x: int, y: int, symbol: str):
        self.rows[x][y] = symbol

    def print_board(self, move: int):

        if move == 0:
            print(f"BOARD AT START: \n")
        else:
            print(f"BOARD AT MOVE {move}: \n")

        for i in range(3):
            for j in range(3):

                if j == 0:
                    print("|", end="")  # print the right bar for the first column

                end_string = "\n" if j == 2 else ""  # put columns in the same line
                print(f" {self.rows[i][j]} |", end=end_string)  # print column with bar to the left

            if i != 2:
                print("---------------")  # print bottom border if this is not the last row
            else:
                print("\n")  # print a new line after the last row

    # return "error message, i.e. 'Invalid Move'", "won" or "null"
    def play_move(self, x: int, y: int, player: Player) -> str:

        # check if the position is empty
        if self.empty_position(x, y):

            # play move/ update board
            self.update_board(x, y, player.symbol)

            # check if it is a winning play (use constant's to prevent errors and make code simple to modify)
            if self.player_won(player):
                return self.USER_WON
            else:
                return self.NO_EVENT

        else:
            return self.INVALID_MOVE


class Game:

    def __init__(self):
        self.game_over = False
        self.player1 = Player()
        self.player2 = Player()
        self.board = Board()
        self.setup()

    def setup(self):
        self.board.clear()  # clear board
        self.game_over = False  # set game_over to False after restart
        self.player1.get_name(player_num=1)
        self.player1.set_symbol()
        self.player2.get_name(player_num=2)
        self.player2.set_symbol()

    def play_move(self, move: int, current_player: Player):
        self.board.print_board(move=move)

        # turn the players string input to list
        input_list = input(f"{current_player.name}'s Move (format: x, y): ").strip().split(",")
        x, y = [int(x) for x in input_list]

        outcome = self.board.play_move(x, y, player=current_player)

        if outcome == self.board.INVALID_MOVE:
            print("That is an invalid position, please try again")
            self.play_move(move, current_player)
        else:
            return outcome

    def play(self):

        player1s_turn = True
        move = 0

        while not self.game_over:

            if player1s_turn:
                current_player = self.player1
            else:
                current_player = self.player2

            outcome = self.play_move(move, current_player)

            if outcome == "WON":
                self.board.print_board(move=move)
                print(f"{current_player.name} WON!")
                self.game_over = True

            elif outcome == self.board.NO_EVENT and not self.board.still_possible_moves():
                self.board.print_board(move=move)
                print("DRAW! No more valid moves.")
                self.game_over = True

            else:
                player1s_turn = not player1s_turn
                move += 1

    def run(self):
        # run game
        run = True

        while run:
            self.play()

            try:
                prompt = input("Play again? (click 'e/E' to exit, any other key to continue): ")
                if prompt.lower() == 'e':
                    run = False
                else:
                    self.setup()

            except KeyboardInterrupt:
                run = False

        print("Thank you for playing!")


game = Game()
game.run()
