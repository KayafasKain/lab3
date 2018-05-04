import os
import numpy as np
from random import randint, choice
from copy import deepcopy


class Game2048:
    """
        Console incarnation of 2048
    """
    def __init__(self, size=2):
        """
            size - represents the size of playfield, 2 - by default
            here comes playfield initialization
        """
        self.field_size = size
        self.score = 0
        self.free_spots = []
        self.play_field = np.array([[0 for j in range(self.field_size)]
                           for i in range(self.field_size)])
        self.generate_new_value()
        self.generate_new_value()

    def check_avaliable_cells(self):
        """
            here comes the search of free cells,    
            if there are free cells - return True   
            otherwise - False   
            also, filling free spots list with  
            free spots coordinates (turple)
        """
        self.free_spots = []
        space_avaliable = False
        for i, row in enumerate(self.play_field):
            for j, val in enumerate(row):
                if not val:
                    self.free_spots.append((i, j))
                    space_avaliable = True
        return space_avaliable

    def move(self, direction):
        """
            Moving rows/cols depending on 
            passed direction value (l/r/u/d)
        """
        dir_from = 0
        dir_to = 0 
        dir_sign = 1
        if direction == "l":
            dir_from = 1
            dir_to = self.field_size
        if direction == "r":
            dir_from = self.field_size  
            dir_sign = -1
            dir_to = 1
        if direction == "u":
            dir_from = 1
            dir_to = self.field_size
        if direction == "d":
            dir_from = self.field_size  
            dir_sign = -1
            dir_to = 1    

        if direction == "r" or direction == "l":  
            self.play_field = self.play_field.transpose()

        for j in range(0, self.field_size):
            while True:
                actions_performed = 0
                for i in range(dir_from, dir_to, dir_sign):
                    i *= dir_sign
                    k = dir_sign * -1              
                    if self.play_field[i][j] != 0:
                        if self.play_field[i + k][j] == 0:
                            temp = self.play_field[i][j]
                            self.play_field[i + k][j] = temp
                            self.play_field[i][j] = 0
                            actions_performed += 1
                        elif self.play_field[i + k][j] == self.play_field[i][j]:
                            self.play_field[i + k][j] *= 2
                            self.play_field[i][j] = 0
                            self.score += self.play_field[i + k][j]
                            actions_performed += 1
                if actions_performed == 0:
                    break
        if direction == "r" or direction == "l":  
            self.play_field = self.play_field.transpose()
        self.generate_new_value()
        self.generate_new_value()
        return self.play_field


    def generate_new_value(self):
        """
            generating value here, to fill 
            empty cells
        """
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
        """
            Moving down. Iterating on column from up to down
        """        
        return self.move("u")

    def move_down(self):
        """
            Moving down. Iterating on column from down to up
        """
        return self.move("d")

    def move_right(self):
        """
            Moving down. Iterating on column from left to right
        """        
        return self.move("r")

    def move_left(self):
        """
            Moving down
        """        
        return self.move("l")

    def has_moves(self):
        """
            Looking for opportunities, return false if not found
        """         
        temp_map = deepcopy(self.play_field)
        temp_score = self.score
        self.move_left()
        self.move_right()
        self.move_down()
        self.move_up()
        if np.array_equal(temp_map, self.play_field):
            is_any_turn_possible = False
        else:
            is_any_turn_possible = True
        self.play_field = deepcopy(temp_map)
        self.score = temp_score
        return is_any_turn_possible

    def get_field(self):
        """ returns current playfield (matrix) """
        return self.play_field

    def get_size(self):
        """ returns field size (int) """
        return self.field_size                

    def get_score(self):
        """ returns score (int) """
        return self.score               



def print_playfield(field_size, play_field, score):
    """
        Printing scores and playfield
    """
    print("+" + "======" * (field_size) + "+")
    form_str = "{:^" + str(field_size * 6) + "}"
    score_section = form_str.format(score)
    print("|{}|".format(score_section))
    print("+" + "======" * (field_size) + "+")
    print()
    wall = "+-----" * (len(play_field[0])) + "+"
    print(wall)
    for row in play_field:
        core = "|".join("{:^5}".format(val) for val in row)
        print("|{}|".format(core))
        print(wall)


def cls():
    """
        Clearing console, depending on OS
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    try:
        size = int(input("Enter field size: "))
        if size < 2:
            size = 2
    except:
        size = 2

    game_session = Game2048(size)

    while game_session.has_moves():
        cls()
        print_playfield(game_session.get_size(),
                        game_session.get_field(),
                        game_session.get_score())
        select_action = input("(WASD) + Enter: ")
        if (select_action == "a" or select_action == "A"):
            game_session.move("l")
        if (select_action == "d" or select_action == "D"):
            game_session.move("r")
        if (select_action == "w" or select_action == "W"):
            game_session.move("u")
        if (select_action == "s" or select_action == "S"):
            game_session.move("d")
    form_str = "{:*^" + str(game_session.field_size * 6) + "}"
    print(form_str.format("( Game Over! )"))


main()
