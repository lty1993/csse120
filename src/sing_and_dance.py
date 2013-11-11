import new_create
import time

def main():

    robot = new_create.Create("sim")

    play_it_again(robot)

    robot.shutdown()

def play_it_again(robot):

    song = [(60, 8), (64, 8), (67, 8), (72, 8)]
    robot.playSong(song)

if __name__ == '__main__':
    main()