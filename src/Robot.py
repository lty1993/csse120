import new_create as our_create
from threading import Timer, Thread
from logger import robotLogger
from job import Job
import random
import time

class Robot(object):
    """
    The bridge class of the Robot.
    Receives the request from the Front and
    passes the command to the Back End (our_create).
    Contributor: Xiangqing Zhang, Matthew O'Brien and Tianyu Liu.
    """
    def __init__(self, port="sim"):
        self.connection = None
        self.port = port
        self.job = None

    def _job(self, function, args=None, kwargs=None, life_span=0):
        """
        Schedules a job for the robot.
        @Parameter function: The NAME of the function.
        @Parameter args: Must be LIST type.
        @Parameter kwargs: Must be DICTIONARY type.
        @Parameter life_span: Terminate the job after the given seconds.
                              If life_span==0, It will run forever unless
                              1. being terminated by code like this:
                                 self._job_clear()
                           OR 2. calling this function (_job) again.

        E.g. _job(robot_go_forward, args=[robot, 10], kwargs={"seconds": 2})
            where robot_go_forward is defined as:
            def robot_go_forward(robot, speed, seconds=2): ...
            Calling this function is doing the same thing as:
            robot_go_forward(robot, 10, seconds=2)
        E.g.2 Check self.go_forward_until_black_line

        Contributor: Xiangqing Zhang
        """
        if not self.connection: self.connect()
        if self.job and self.job.is_alive():
            self._log("The robot connection is busy. Terminating the current process...", "_job", "WARNING")
            self._job_clear()
            self._log("The robot connection has been terminated successfully.", "SUCCESS")
        self.job = None
        self.job = Job(function, args=args, kwargs=kwargs)
        self.job.start()
        if life_span > 0:
            t = Timer(life_span, lambda: self._job_clear())
            t.start()
    def _job_clear(self):
        """
        Clears all jobs.
        Contributor: Xiangqing Zhang
        """
        self.job.terminated = True
        while self.job.is_alive(): pass
        self.connection.stop()

    def _log(self, message, method_name, level="DEBUG", logger=None):
        """
        Method that calls the logger to log events.
        @Parameter message: A STR which is the content of the event to log.
        @Parameter method_name: The name of the method where the event happens.
        @Parameter level: Should be "DEBUG", "WARNING", "SEVERE", "INFO" and "SUCCESS".
        @Parameter logger: Optional. By default, all loggers will be called to log the event.

        E.g.1 self._log("Lost connection.", "disconnect", "DEBUG")
        E.g.2 self._log("This will only be shown on the console.",
                        "test_function", logger="ConsoleLogger")
        Contributor: Xiangqing Zhang
        """
        robotLogger.add(message, method_name, level, logger)
    def connect(self):
        """
        Connects the our_create module.
        Contributor: Tianyu Liu
        """
        if not self.connection:
            try:
                self._log("Establishing the connection...", "_job")
                self.connection = our_create.Create(self.port)
                self._log("Connection established.", "_job", "SUCCESS")
            except Exception as e:
                self._log("Error occured while connecting: %s" % e, "connect")
    def disconnect(self):
        """
        Detach from the our_create module.
        Contributor: Tianyu Liu
        """
        if self.connection:
            self._job_clear()
            self.connection.shutdown()
            self.connection = None
    def stop(self):
        """
        Stops the robot.
        Contributor: Xiangqing Zhang.
        """
        if self.connection: self._job_clear()

    def move_autonomously(self, speed, rotation, seconds):
        """
        Move autonomously at user-specified directional and rotational speed
        for a specific amount of time.
        Feature: 4a-1
        Contributor: Matthew O'Brien
        """
        robotLogger.add("%d,%d,%d" % (speed, rotation, seconds), "move_autonomously")
        self._job(self._move_autonomously, [speed, rotation], life_span=seconds)
    def _move_autonomously(self, speed, rotation):
        self.connection.go(speed, rotation)
    def go_forward_until_black_line(self, speed, darkness=500):
        """
        Go forward at user-specified speed until WILMA reaches a black line,
        where the user specifies the "darkness" of the line.
        Feature: 5a-1
        Contributor: Xiangqing Zhang
        """
        if darkness <= 0: darkness = 500
        self._job(self._go_forward_until_black_line, [speed, darkness])
    def _go_forward_until_black_line(self, speed, darkness):
        sensor = [our_create.Sensors.cliff_front_left_signal, our_create.Sensors.cliff_front_right_signal]
        while True and not self.job.terminated:
            self._move_autonomously(speed, 0)
            sensor_values = [self.connection.getSensor(sensor[0]), self.connection.getSensor(sensor[1])]
            if sensor_values[0] < darkness or sensor_values[1] < darkness: break
        self.connection.stop()
    def chat_with_another_robot(self, bytecode):
        """
        User can make WILMA start/stop emitting a user-specified IR signal.
        WILMA displays whatever IR signal it is currently hearing.
        WILMA can “chat” via user-specified IR numbers sent synchronously:
        WILMA starts sending, then listens until it hears something from the other robot,
        then starts sending something different, then listens until it hears something from the other robot, etc.
        Feature: 8a-1
        Contributor: Xiangqing Zhang
        """
        # TODO: Test in the REAL robot!
        self._job(self._chat_with_another_robot, bytecode)
    def _chat_with_another_robot(self, bytecode):
        sensor = our_create.Sensors.ir_byte
        while True:
            self.robot.sendIR(bytecode)
            while True:
                sensor_values = self.connection.getSensor(sensor)
                if sensor_values != 255: break
            temp_bytecode = random.randint(0, 255)
            while temp_bytecode == bytecode:
                temp_bytecode = random.randint(0, 255)
            bytecode = temp_bytecode
    def team_info(self):
        """
        Displays team members' names and task-list reported hours that have been updated at each sprint.
        Functions to read in files are implented in this function.
        Feature 1a-1
        Contributor: Matthew O'Brien
        """
        self._job(self._team_info)
    def _team_info(self):
        FO = open("tasks-1.r", "r")
        tasks1 = FO.read()
        FO.close()
        self._log(tasks1, "_team_info")
        FO = open("tasks-2.r", "r")
        tasks2 = FO.read()
        FO.close()
        self._log(tasks2, "_team_info")
        FO = open("tasks-3.r", "r")
        tasks3 = FO.read()
        FO.close()
        self._log(tasks3, "_team_info")
    def log_information(self):
        """
        Also displays a short fictitious bio on WILMA.
        Functions to read in files are implented in this function.
        Feature: 1b-1
        Contributor: Matthew O'Brien
        """
        self._job(self._log_information)
    def _log_information(self):
        FO = open("WILMAbio.wilma", "r")
        wilma_bio = FO.read()
        FO.close()
        self._log(wilma_bio, "_log_information")
    def grid_movement(self, coordinates):
        """
        Moves robot to user-specified coordinates on an imaginary grid.
        Feature 7a-1
        Contributor: Matthew O'Brien
        """
        coor_list = []
        coordinates_list = coordinates.split()
        coordinates_list.insert(0, '00')

        for k in range(1, len(coordinates_list)):
            location = coordinates_list[k - 1]
            coordinate = coordinates_list[k]
            self._job(self._grid_movement, [coordinate, location])
        robotLogger.add("%s%s" % (coordinates, location), "grid_movement")
       

    def _grid_movement(self, coordinate, location):
        x_initial = int(location[0])
        y_initial = int(location[1])
        speed = 50
        rotation_left = 45
        rotation_right = -45
        x = int(coordinate[0])
        y = int(coordinate[1])

        if x > x_initial:
            self.connection.go(speed, 0)
            time.sleep((x - x_initial))
        elif x < x_initial:
            self.connection.go(0, rotation_left)
            time.sleep(4)
            self.connection.go(speed, 0)
            time.sleep((x_initial - x))
            self.connection.go(0, 0)
            time.sleep(1)
            self.connection.go(0, rotation_right)
            time.sleep(4)
            self.connection.go(0, 0)
            time.sleep(1)
        else:
            pass

        if y > y_initial:
            self.connection.go(0, rotation_left)
            time.sleep(2)
            self.connection.go(speed, 0)
            time.sleep((y - y_initial))
            self.connection.go(0, rotation_right)
            time.sleep(2)
        elif y < y_initial:
            self.connection.go(0, rotation_right)
            time.sleep(2)
            self.connection.go(speed, 0)
            time.sleep((y_initial - y))
            self.connection.go(0, rotation_left)
            time.sleep(2)
        else:
            pass
        self.connection.stop()    
        self.stop()


    def __repr__(self):
        """
        Returns a string that represents this object.
        Contributor: Xiangqing Zhang
        """
        return 'An our_create robot connection with port {}'.format(self.port)
# print("hello")

# git add .
# git status
# git commit -m "message"
# git push
