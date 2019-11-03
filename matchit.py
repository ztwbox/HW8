# ----------------------------------------------------------------------
# Name:        matchit
# Purpose:     Implement a single player matching game
#
# Author(s):
# ----------------------------------------------------------------------
"""
A single player matching game.

usage: matchit.py [-h] [-f] {blue,green,magenta} image_folder
positional arguments:
  {blue,green,magenta}  What color would you like for the player?
  image_folder          What folder contains the game images?

optional arguments:
  -h, --help            show this help message and exit
  -f, --fast            Fast or slow game?
"""
import tkinter
import os
import random
import argparse


class MatchGame(object):

    """
    GUI Game class for a matching game.

    Arguments:
    parent: the root window object
    player_color (string): the color to be used for the matched tiles
    folder (string) the folder containing the images for the game
    delay (integer) how many milliseconds to wait before flipping a tile

    Attributes:
    Please list ALL the instance variables here
    """

    # Add your class variables if needed here - square size, etc...)
    score = 100
    counter = 0
    delay = 300

    def __init__(self, parent, player_color, folder, delay):
        parent.title('Match it!')
        self.parent = parent
        self.color = player_color
        self.folder = folder
        self.delay = delay
        self.images = []
        for f in os.listdir(folder):
            try:
                self.images.append(tkinter.PhotoImage(file=folder+'/'+f))
            except Exception:
                pass
        self.images.extend(self.images)
        random.shuffle(self.images)
            # Create the restart button widget
        restart_button = tkinter.Button(parent, text='Restart', width=20,
                                        command=self.restart)
        restart_button.grid()
        # Create a canvas widget
        self.canvas = tkinter.Canvas(parent, width=400, height=400)
        for i in range(0, 400, 100):
            for k in range(0, 400, 100):
                self.canvas.create_rectangle(i, k, 100+i, 100+k,
                                             outline='black', fill="yellow")
                self.canvas.create_image(50+i, 50+k, image=self.images[
                                         self.counter], state='hidden')
                self.counter += 1

        self.canvas.bind("<Button-1>", self.play)
        self.canvas.grid()
        # Create a label widget for the score and end of game messages
        self.label_score = tkinter.Label(parent, text=f'Score: {self.score}')
        self.label_score.grid()
        self.label_endgame = tkinter.Label(parent, text='Game Over!')
        # Create any additional instance variable you need for the game



    def restart(self):
        """
        This method is invoked when player clicks on the RESTART button.
        It shuffles and reassigns the images and resets the GUI and the
        score.
        :return: None
        """
        self.canvas.delete("all")
        self.counter = 0
        self.score = 100
        random.shuffle(self.images)
        for i in range(0, 400, 100):
            for k in range(0, 400, 100):
                self.canvas.create_rectangle(i, k, 100+i, 100+k,
                                             outline='black', fill="yellow")
                self.canvas.create_image(50+i, 50+k, image=self.images[
                                         self.counter], state='hidden')
                self.counter += 1

    def play(self, event):
        """
        This method is invoked when the user clicks on a square.
        It implements the basic controls of the game.
        :param event: event (Event object) describing the click event
        :return: None
        """

        image = self.canvas.find_above(tkinter.CURRENT)

        print(self.canvas.gettags(image))
        if 'selected' not in self.canvas.gettags(image):
            self.canvas.itemconfigure(image, tag='selected', state='normal')
            print("show")

        self.canvas.after(1000, self.match_check('selected'))

    def match_check(self, select):
        if len(self.canvas.find_withtag(select)) == 2:
            img1 = self.canvas.find_withtag(select)[0]
            img2 = self.canvas.find_withtag(select)[1]
            if self.canvas.itemcget(img1, 'image') == self.canvas.itemcget(
                    img2, 'image'):
                print("True")
                rect = self.canvas.find_below(img1)
                self.canvas.itemconfigure(rect, fill='blue')
                rect = self.canvas.find_below(img2)
                self.canvas.itemconfigure(rect, fill='blue')
                self.canvas.delete(img1)
                self.canvas.delete(img2)
                print(self.canvas.find_withtag('selected'))
            else:
                self.canvas.itemconfigure(img1, tag='', state='hidden')
                # self.canvas.after(1000, self.canvas.itemconfigure(img2,
                #                                                  tag='',
                #                                                  state='hidden'))
                self.canvas.itemconfigure(img2, tag='', state='hidden')
                print("False")
    # Enter your additional method definitions below
    # Make sure they are indented inside the MatchGame class
    # Make sure you include docstrings for all the methods.



# Enter any function definitions here to get and validate the
# command line arguments.  Include docstrings.


def valid_dir(folder):
    counter = 0
    if os.path.isdir(folder):
        for f in os.listdir(folder):
            if f[-3:] == 'gif':
                counter += 1
        if counter >= 8:
            return folder
        else:
            raise argparse.ArgumentTypeError(f'{folder} must contain at '
                                             f'leaset 8 gif images')
    else:
        raise argparse.ArgumentTypeError(f'{folder} is not a valid folder')

def main():
    # Retrieve and validate the command line arguments using argparse
    # parser = argparse.ArgumentParser()
    # parser.add_argument('color',
    #                     help='{blue,green,magenta}What color would you like '
    #                          'for the player',
    #                     choices=['blue', 'green', 'magenta'])
    # parser.add_argument('image_folder',
    #                     help='What folder contains the game images')
    # parser.add_argument('-f', '--fast',
    #                     help='Fast or slow game?',
    #                     action='store_true')
    # Instantiate a root window
    # Instantiate a MatchGame object with the correct arguments
    # Enter the main event loop
    root = tkinter.Tk()
    # Instantiate our painting app object
    painting = MatchGame(root, 1, 'SJSUimages', True)
    # enter the main event loop and wait for events
    root.mainloop()

if __name__ == '__main__':
    main()
    
