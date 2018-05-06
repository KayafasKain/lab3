import os
from game2048_core import game2048 as game



is_curses_avaliable = True

try:
    import curses
except ImportError:
    is_curses_avaliable = False


class Renderer:
    """
        Class stands for rendering playfield and 
        intercepting input
    """
    def __init__(self, size = 2, stdscr = None):
        """
            Initializing class with size, and curses object
            both are optional, have following default values:
            size = 2
            stdscr = None
        """
        self.game_session = game.Game2048(size)
        self.stdscr = stdscr

    def cls(self):
        """
            Clearing console, depending on OS
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_playfield_console(self):
        """
            Printing console scores and playfield
        """
        self.cls()
        field_size = self.game_session.get_size()
        play_field = self.game_session.get_field()
        score = self.game_session.get_score()

        print("+" + "======" * (field_size) + "+")
        form_str = "{:^" + str(field_size * 6) + "}"
        score_section = form_str.format(score)
        print("|{}|".format(score_section))
        print("+" + "======" * (field_size) + "+")
        print()
        wall = "+-----" * (field_size) + "+"
        print(wall)
        for row in play_field:
            core = "|".join("{:^5}".format(val) for val in row)
            print("|{}|".format(core))
            print(wall)


    def console_input(self):
        """
            Classic input from console
        """        
        select_action = input("(WASD) + Enter: ")
        if (select_action == "a" or select_action == "A"):
            self.game_session.move("l")
        if (select_action == "d" or select_action == "D"):
            self.game_session.move("r")
        if (select_action == "w" or select_action == "W"):
            self.game_session.move("u")
        if (select_action == "s" or select_action == "S"):
            self.game_session.move("d") 

    def print_playfield_curses(self):
        """
            Playfield render, using curses
        """
        field_size = self.game_session.get_size()
        play_field = self.game_session.get_field()
        score = self.game_session.get_score()

        self.stdscr.clear()

        self.stdscr.addstr("+" + "======" * (field_size) + "+")
        self.stdscr.addstr("\n")
        form_str = "{:^" + str(field_size * 6) + "}"
        score_section = form_str.format(score)
        self.stdscr.addstr("|{}|".format(score_section))
        self.stdscr.addstr("\n")
        self.stdscr.addstr("+" + "======" * (field_size) + "+")
        self.stdscr.addstr("\n")
        wall = "+-----" * (len(play_field[0])) + "+"
        self.stdscr.addstr(wall)
        self.stdscr.addstr("\n")
        for row in play_field:

            core = "|".join("{:^5}".format(val) for val in row)
            self.stdscr.addstr("|{}|".format(core))
            self.stdscr.addstr("\n")
            self.stdscr.addstr(wall)
            self.stdscr.addstr("\n")      
            
    def curses_input(self): 
        """
            Input, using curses
        """   
        c = self.stdscr.getch()
        if c in [ord('a'), curses.KEY_LEFT]:
            self.game_session.move('l')
        elif c in [ord('s'), curses.KEY_DOWN]:
            self.game_session.move('d')
        elif c in [ord('w'), curses.KEY_UP]:
            self.game_session.move('u')
        elif c in [ord('d'), curses.KEY_RIGHT]:
            self.game_session.move('r')
    
    def render_game(self):
        """
            Rendering playfield and 
            intercepting commands depending
            on conditions
        """
        form_str = "{:*^" + str(self.game_session.get_size() * 6) + "}"

        if self.stdscr != None:
            while self.game_session.has_moves():
                self.print_playfield_curses()
                self.curses_input()

            self.stdscr.addstr(form_str.format("( Game Over! )"))
            self.stdscr.addstr("\n")
            self.stdscr.addstr("Press any key to exit")
            c = self.stdscr.getch()
        else:
            while self.game_session.has_moves():
                self.print_playfield_console()
                self.console_input() 
                
            print(form_str.format("( Game Over! )"))      
             


def draw_game(stdscr, size):
    try:
        render = Renderer(size, stdscr)
        render.render_game()
    except KeyboardInterrupt:
        pass
 
def main():
    try:
        size = int(input("Enter field size: "))
        if size < 2:
            size = 2
    except:
        size = 2 
           
    if is_curses_avaliable:   
        curses.wrapper(draw_game, size)
    else:
        render = Renderer(size)
        render.render_game()


    

if __name__ == "__main__":
    main()