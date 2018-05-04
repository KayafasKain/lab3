import os
from random import randint, choice
from copy import deepcopy


class Game2048:
    def __init__(self, size=2):
        self.field_size = size
        self.score = 0
        self.free_spots = []
        self.play_field = [[0 for j in range(self.field_size)]
                           for i in range(self.field_size)]
        self.generate_new_value()
        self.generate_new_value()

    def check_avaliable_cells(self):
        self.free_spots = []
        space_avaliable = False
        for i, row in enumerate(self.play_field):
            for j, val in enumerate(row):
                if not val:
                    self.free_spots.append((i, j))
                    space_avaliable = True
        return space_avaliable

    def generate_new_value(self):
        while True:
            if not self.check_avaliable_cells():
                break
            else:
                i, j = choice(self.free_spots)
                if randint(0, 10) < 9:
                    self.play_field[i][j] = 2
                else:
                    self.play_field[i][j] = 4
                break
        return self.play_field

    def move_up(self):
        for j in range(0, self.field_size):
            while True:
                actions_performed = 0
                for i in range(1, self.field_size):
                    if self.play_field[i][j] != 0:
                        if self.play_field[i - 1][j] == 0:
                            temp = self.play_field[i][j]
                            self.play_field[i - 1][j] = temp
                            self.play_field[i][j] = 0
                            actions_performed += 1
                        elif self.play_field[i - 1][j] == self.play_field[i][j]:
                            self.play_field[i - 1][j] *= 2
                            self.play_field[i][j] = 0
                            self.score += self.play_field[i - 1][j]
                            actions_performed += 1
                if actions_performed == 0:
                    break
        self.generate_new_value()
        self.generate_new_value()
        return self.play_field

    def move_down(self):
        for j in range(0, self.field_size):
            while True:
                actions_performed = 0
                for i in range(self.field_size, 1, -1):
                    if self.play_field[-i][j] != 0:
                        if self.play_field[-i + 1][j] == 0:
                            temp = self.play_field[-i][j]
                            self.play_field[-i + 1][j] = temp
                            self.play_field[-i][j] = 0
                            actions_performed += 1
                        elif self.play_field[-i + 1][j] == self.play_field[-i][j]:
                            self.play_field[-i + 1][j] *= 2
                            self.play_field[-i][j] = 0
                            self.score += self.play_field[-i + 1][j]
                            actions_performed += 1
                if actions_performed == 0:
                    break
        self.generate_new_value()
        self.generate_new_value()
        return self.play_field

    def move_right(self):
        for i in range(0, self.field_size):
            while True:
                actions_performed = 0
                for j in range(self.field_size, 1, -1):
                    if self.play_field[i][-j] != 0:
                        if self.play_field[i][-j + 1] == 0:
                            temp = self.play_field[i][-j]
                            self.play_field[i][-j + 1] = temp
                            self.play_field[i][-j] = 0
                            actions_performed += 1
                        elif self.play_field[i][-j + 1] == self.play_field[i][-j]:
                            self.play_field[i][-j + 1] *= 2
                            self.play_field[i][-j] = 0
                            self.score += self.play_field[i][-j + 1]
                            actions_performed += 1
                if actions_performed == 0:
                    break
        self.generate_new_value()
        self.generate_new_value()
        return self.play_field

    def move_left(self):
        for i in range(0, self.field_size):
            while True:
                actions_performed = 0
                for j in range(1, self.field_size):
                    if self.play_field[i][j] != 0:
                        if self.play_field[i][j - 1] == 0:
                            temp = self.play_field[i][j]
                            self.play_field[i][j - 1] = temp
                            self.play_field[i][j] = 0
                            actions_performed += 1
                        elif self.play_field[i][j - 1] == self.play_field[i][j]:
                            self.play_field[i][j - 1] *= 2
                            self.play_field[i][j] = 0
                            self.score += self.play_field[i][j - 1]
                            actions_performed += 1
                if actions_performed == 0:
                    break
        self.generate_new_value()
        self.generate_new_value()
        return self.play_field

    def possible_options_check(self):
        temp_map = deepcopy(self.play_field)
        temp_score = self.score
        self.move_left()
        self.move_right()
        self.move_down()
        self.move_up()
        is_any_turn_possible = temp_map != self.play_field
        self.play_field = deepcopy(temp_map)
        self.score = temp_score
        return is_any_turn_possible

    def print_playfield(self):
        print("")

        print("+" + "======" * (self.field_size) + "+")
        form_str = "{:^" + str(self.field_size * 6) + "}"
        score_section = form_str.format(self.score)
        print("|{}|".format(score_section))
        print("+" + "======" * (self.field_size) + "+")
        print("")
        wall = "+-----" * (len(self.play_field[0])) + "+"
        print(wall)
        for row in self.play_field:
            core = "|".join("{:^5}".format(val) for val in row)
            print("|{}|".format(core))
            print(wall)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def main():
    try:
        size = int(input("Enter field size: "))
        if size < 2:
            size = 2
    except:
        size = 2

    game_session = Game2048(size)

    while game_session.possible_options_check():
        cls()
        game_session.print_playfield()
        select_action = input("(WASD) + Enter: ")
        if (select_action == "a" or select_action == "A"):
            game_session.move_left()
        if (select_action == "d" or select_action == "D"):
            game_session.move_right()
        if (select_action == "w" or select_action == "W"):
            game_session.move_up()
        if (select_action == "s" or select_action == "S"):
            game_session.move_down()
    form_str = "{:*^" + str(game_session.field_size * 6) + "}"
    print(form_str.format("( Game Over! )"))


main()
