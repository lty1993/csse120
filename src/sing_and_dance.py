import new_create
import time

def main():

    robot = new_create.Create(10)

    sing_and_dance(robot)

    robot.shutdown()

def sing_and_dance(robot):

    fur_elise_song_1 = [(64, 12), (63, 12), (64, 12), (63, 12), (64, 12), (59, 12), (62, 12), (60, 12), (57, 36), (48, 12), (52, 12), (57, 12), (59, 36)]
    fur_elise_song_2 = [(52, 12), (56, 12), (59, 12), (60, 36), (52, 12), (64, 12), (63, 12), (64, 12), (63, 12), (64, 12), (59, 12), (62, 12), (60, 12), (57, 36)]
    fur_elise_song_3 = [(48, 12), (52, 12), (57, 12), (59, 36), (52, 12), (60, 12), (59, 12), (57, 48)]
    fur_elise_song_4 = [(64, 12), (63, 12), (64, 12), (63, 12), (64, 12), (59, 12), (62, 12), (60, 12), (57, 36), (48, 12), (52, 12), (57, 12), (59, 36)]
    fur_elise_song_5 = [(48, 12), (52, 12), (57, 12), (59, 36), (52, 12), (60, 12), (59, 12), (57, 36), (59, 12), (60, 12), (62, 12), (64, 36)]
    fur_elise_song_6 = [(55, 12), (65, 12), (64, 12), (62, 36), (53, 12), (64, 12), (62, 12), (60, 36), (52, 12), (62, 12), (60, 12), (59, 36), (52, 12), (52, 12), (64, 12), (52, 12)]
    fur_elise_song_7 = [(64, 12), (64, 12), (76, 12), (63, 12), (64, 12), (63, 12), (64, 12), (63, 12), (64, 12), (63, 12), (64, 12), (63, 12), (64, 12), (63, 12), (64, 12)]
    fur_elise_song_8 = [(59, 12), (62, 12), (57, 36), (48, 12), (52, 12), (57, 12), (59, 36), (52, 12), (56, 12), (59, 12), (60, 36)]
    fur_elise_song_9 = [(52, 12), (64, 12), (63, 12), (64, 12), (63, 12), (64, 12), (59, 12), (62, 12), (60, 12), (57, 36), (48, 12), (52, 12), (57, 12), (59, 36)]
    fur_elise_song_10 = [(50, 12), (60, 12), (59, 12), (57, 60)]

    fur_elise = [[(64, 12), (63, 12), (64, 12), (63, 12), (64, 12), (59, 12), (62, 12), (60, 12), (57, 36), (48, 12), (52, 12), (57, 12), (59, 36)],
                 [(52, 12), (56, 12), (59, 12), (60, 36), (52, 12), (64, 12), (63, 12), (64, 12), (63, 12), (64, 12), (59, 12), (62, 12), (60, 12), (57, 36)],
                 [(48, 12), (52, 12), (57, 12), (59, 36), (52, 12), (60, 12), (59, 12), (57, 48)],
                 [(64, 12), (63, 12), (64, 12), (63, 12), (64, 12), (59, 12), (62, 12), (60, 12), (57, 36), (48, 12), (52, 12), (57, 12), (59, 36)],
                 [(52, 12), (56, 12), (59, 12), (60, 36), (52, 12), (64, 12), (63, 12), (64, 12), (63, 12), (64, 12), (59, 12), (62, 12), (60, 12), (57, 36)],
                 [(48, 12), (52, 12), (57, 12), (59, 36), (52, 12), (60, 12), (59, 12), (57, 36), (59, 12), (60, 12), (62, 12), (64, 36)],
                 [(55, 12), (65, 12), (64, 12), (62, 36), (53, 12), (64, 12), (62, 12), (60, 36), (52, 12), (62, 12), (60, 12), (59, 36), (52, 12), (52, 12), (64, 12), (52, 12)],
                 [(64, 12), (64, 12), (76, 12), (63, 12), (64, 12), (63, 12), (64, 12), (63, 12), (64, 12), (63, 12), (64, 12), (63, 12), (64, 12), (63, 12), (64, 12)],
                 [(59, 12), (62, 12), (60, 12), (57, 36), (48, 12), (52, 12), (57, 12), (59, 36), (52, 12), (56, 12), (59, 12), (60, 36)],
                 [(52, 12), (64, 12), (63, 12), (64, 12), (63, 12), (64, 12), (59, 12), (62, 12), (60, 12), (57, 36), (48, 12), (52, 12), (57, 12), (59, 36)],
                 [(50, 12), (60, 12), (59, 12), (57, 60)]]

    is_playing_sensor = new_create.Sensors.song_playing
    for k in range(len(fur_elise)):
        robot.playSong(fur_elise[k])
        while True:
            is_playing = robot.getSensor(is_playing_sensor)
            if not is_playing:
                break



#     robot.playSong(fur_elise_song_1)
#     time.sleep(4)
#     robot.playSong(fur_elise_song_2)
#     time.sleep(4)
#     robot.playSong(fur_elise_song_3)
#     time.sleep(4)
#     robot.playSong(fur_elise_song_4)
#     time.sleep(4)
#     robot.playSong(fur_elise_song_2)
#     time.sleep(4)
#     robot.playSong(fur_elise_song_5)
#     time.sleep(4)
#     robot.playSong(fur_elise_song_6)
#     time.sleep(4)
#     robot.playSong(fur_elise_song_7)
#     time.sleep(4)
#     robot.playSong(fur_elise_song_8)
#     time.sleep(4)
#     robot.playSong(fur_elise_song_9)
#     time.sleep(4)
#     robot.playSong(fur_elise_song_10)
#     time.sleep(4)

if __name__ == '__main__':
    main()