import new_create as our_create
from threading import Timer, Thread
from logger import robotLogger
from job import Job
import random
import time
import math

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
        self._sendIR = False
        self._follow_line = False
        self._forward_until_black_line = False
        self._forward_until_bumps = False
        self._teleportspeed = [0,0];
        self._ir_signal = -1;

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
        if self.job:
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
        if self.job:
            Job.in_use = False
            self.job = None
        if self.connection: self.connection.stop()

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
        # robotLogger.add("Terminating", "self.stop")
        self._teleportspeed = [0,0]
        self._sendIR = False
        self._follow_line = False
        self._forward_until_black_line = False
        if self.job:
            Job.in_use = False
            self.job = None
        if self.connection: self.connection.stop()

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
        self._forward_until_black_line = True
        sensor = [our_create.Sensors.cliff_front_left_signal, our_create.Sensors.cliff_front_right_signal]
        self._move_autonomously(speed, 0)
        while self._forward_until_black_line:
            sensor_values = [self.connection.getSensor(sensor[0]), self.connection.getSensor(sensor[1])]
            if sensor_values[0] < darkness or sensor_values[1] < darkness: break
            time.sleep(0.05)
        self.stop()
    def go_forward_until_bumps(self, speed, bump_sensor):
        self._job(self._go_forward_until_bumps, [speed, bump_sensor])
    def _go_forward_until_bumps(self, speed, bump_sensor):
        self._forward_until_bumps = True
        sensor = our_create.Sensors.bumps_and_wheel_drops
        self._move_autonomously(speed, 0)
        while self._forward_until_bumps:
            sensor_values = robot.getSensor(sensor)
            left_bumper_state = sensor_values[3]
            right_bumper_state = sensor_values[4]
            if ("L" in bump_sensor) or ("l" in bump_sensor):
                if left_bumper_state==1:
                    break
            if ("R" in bump_sensor) or ("r" in bump_sensor):
                if right_bumper_state==1:
                    break
            time.sleep(0.05)

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
        self._job(self._chat_with_another_robot, [bytecode])
    def _chat_with_another_robot(self, bytecode):
        self._sendIR = True
        sensor = our_create.Sensors.ir_byte
        while self._sendIR:
            self.connection.sendIR(bytecode)
            while self._sendIR:
                sensor_values = self.connection.getSensor(sensor)
                robotLogger.add("bytecode: %d" % sensor_values, "_chat_with_another_robot")
                if sensor_values != 255:
                    break
            temp_bytecode = random.randint(0, 255)
            while temp_bytecode == bytecode:
                temp_bytecode = random.randint(0, 255)
            bytecode = temp_bytecode
    def follow_with_black_line(self):
        self._job(self._follow_with_black_line);
    def _follow_with_black_line(self):
        # ls = our_create.Sensors.None
        # rs = our_create.Sensors.None
        pass
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
        FO = open("tasks-2.r", "r")
        tasks2 = FO.read()
        FO.close()
        FO = open("tasks-3.r", "r")
        tasks3 = FO.read()
        FO.close()
        self._log(tasks1, "_team_info")
        self._log(tasks2, "_team_info")
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
        self.stop()

    def grid_movement(self, coordinates, speed, rotation):
        """
        Moves robot to user-specified coordinates on an imaginary grid.
        Feature 7a-1
        Contributor: Matthew O'Brien
        """
        self._job(self._grid_movement, [coordinates, speed, rotation])
    def _grid_movement(self, coordinates, speed, rotation):
        if coordinates == 'coordinates.txt':
            FO = open("coordinates.txt", "r")
            coordinates_from_file = FO.read()
            FO.close()
            coordinates_temp = coordinates_from_file.split()
            coordinates = [[0, 0]]
            for each_coordinate in coordinates_temp:
                coordinates.append(each_coordinate.split(","))
        else:
            coordinates_temp = coordinates.split()
            coordinates = [[0, 0]]
            for each_coordinate in coordinates_temp:
                coordinates.append(each_coordinate.split(","))

        for k in range(1, len(coordinates)):
            location = coordinates[k - 1]
            coordinate = coordinates[k]
            x_initial = int(location[0])
            y_initial = int(location[1])
            rotation_left = 45
            rotation_right = -45
            x = int(coordinate[0])
            y = int(coordinate[1])
            robotLogger.add("%d,%d==>%d,%d" % (x_initial, y_initial, x, y), "_grid_movement")

            y_distance = y - y_initial
            x_distance = x - x_initial
            r = math.sqrt(x_distance ** 2 + y_distance ** 2)
            if speed == 0:  # give an initial speed if none is provided
                speed = 20
            elif speed > 50:  # limit speed to 50 for accuracy
                speed = 50
            unit_time = (10 / speed) * r
            robotLogger.add("unit_time = %.2f, speed = %.2f, s*u = %.2f, r = %.2f"%(unit_time, speed, speed*unit_time, r), "_grid_movement")

            if x_distance == 0 and y_distance > 0:  # positive y-axis
                degrees = 90
            elif x_distance == 0 and y_distance < 0:  # negative y-axis
                degrees = -90
            elif y_distance == 0 and x_distance < 0:  # negative x-axis
                degrees = 180
            else:
                radians = math.atan(y_distance / x_distance)
                degrees = radians * (180 / math.pi)

            if x_distance < 0 and y_distance > 0:  # 2nd quadrant
                degrees = 90 - degrees
            elif x_distance < 0 and y_distance < 0:  # 3rd quadrant
                degrees = 180 + degrees
            else:
                pass

            self.connection.go(0, degrees / 4)
            time.sleep(4)
            self.connection.go(speed, 0)
            time.sleep(unit_time)
            self.connection.go(0, -degrees / 4)
            time.sleep(4)
            self.connection.stop()

        self.stop()
        robotLogger.add("Finished moving.", "_grid_movement", "SUCCESS")

    def go_forward_until_ir_signal(self, speed, ir_signal):
        self._job(self._go_forward_until_ir_signal, [speed, ir_signal]);
    def _go_forward_until_ir_signal(self, speed, ir_signal):
        

    def teleport(self, commands):
        """
        User can move WILMA forward and backward, spin WILMA left and right.
        User can change speed during teleoperation.
        Feature: 3a
        Contributor: Tianyu Liu
        """
        self._job(self._teleport, [commands]);
    def _teleport(self, command):
        if(command == "Forward"):
            if(self._teleportspeed[0] > 0):
                self._move_autonomously(self._teleportspeed[0] + 10, 0)
                self._teleportspeed[0] += 10
            else:
                self._move_autonomously(10, 0)
                self._teleportspeed[0] = 10
                self._teleportspeed[1] = 0
        if(command == "Backward"):
            if(self._teleportspeed[0] < 0):
                self._move_autonomously(self._teleportspeed[0] - 10, 0)
                self._teleportspeed[0] -= 10
            else:
                self._move_autonomously(-10, 0)
                self._teleportspeed[0] = -10
                self._teleportspeed[1] = 0
        if(command == "Right"):
            if(self._teleportspeed[1] < 0):
                self._move_autonomously(0, self._teleportspeed[1] - 30)
                self._teleportspeed[1] += -30
            else:
                self._move_autonomously(0, -30)
                self._teleportspeed[1] = -30
                self._teleportspeed[0] = 0
        if(command == "Left"):
            if(self._teleportspeed[1] > 0):
                self._move_autonomously(0, self._teleportspeed[1] + 30)
                self._teleportspeed[1] += 30
            else:
                self._move_autonomously(0, 30)
                self._teleportspeed[1] = 30
                self._teleportspeed[0] = 0

    def follow_black_line(self, speed, darkness):
        """
        WILMA can follow a black line and possibly a wall.
        Feature: 6a
        Contributor: Tianyu Liu
        """
        self._job(self._follow_black_line, [speed, darkness]);
    def _follow_black_line(self, speed, darkness):
        self._follow_line = True
        sensor = [our_create.Sensors.cliff_front_left_signal, our_create.Sensors.cliff_front_right_signal];
        if darkness <= 0: darkness = 500;
        self.connection.go(speed, 0);
        while self._follow_line:
            # robotLogger.add("%s"%self._follow_line, "_follow_black_line")
            temp1 = True;
            sensor_value = [self.connection.getSensor(sensor[0]), self.connection.getSensor(sensor[1])];
            if (sensor_value[0]< darkness and sensor_value[1]<darkness and temp1) or (sensor_value[0] < darkness and temp1):
                self.connection.stop();
                self.connection.go(0, 180);
                time.sleep(0.2);
                self.connection.stop();
                temp1 = False;
            if(sensor_value[1] < darkness and temp1):
                self.connection.stop();
                self.connection.go(0, -180);
                time.sleep(0.2);
                self.connection.stop();
                temp1 = False;
            if temp1:
                self.connection.go(speed, 0);
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
