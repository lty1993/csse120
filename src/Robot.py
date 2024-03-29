import new_create as our_create
from threading import Timer, Thread
from logger import robotLogger
from job import Job
from secure import RobotEncryption
from eliza import eliza
import time
import random
import math
import map_GUI

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
        self.eliza = eliza()
        self.job = None
        self.robotEncryption = RobotEncryption(0)
        self._send_bytecode_flag = False
        self._receive_bytecode_flag = False
        self._take_other_robot_flag = False
        self._follow_other_robot_flag = False
        self.__receive_bytecode_flag = False
        self._sendIR = False
        self._follow_line = False
        self._forward_until_black_line = False
        self._forward_until_bumps = False
        self._encode_message = False
        self._teleportspeed = [0, 0];
        self._forward_until_ir_signal = -1;
        self.ir_time = 0.1

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
        self._teleportspeed = [0, 0]
        self._sendIR = False
        self._follow_line = False
        self._send_bytecode_flag = False
        self._receive_bytecode_flag = False
        self.__receive_bytecode_flag = False
        self._take_other_robot_flag = False
        self._follow_other_robot_flag = False
        self._forward_until_black_line = False
        self._forward_until_bumps = False
        self._forward_until_ir_signal = -1
        self._encode_message = False
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
        self._job(self._move_autonomously, [speed, rotation, seconds], life_span=seconds)
    def _move_autonomously(self, speed, rotation, seconds, no_seconds = False):
        if not no_seconds and rotation == 0:
            distance_sensor = our_create.Sensors.distance  # Method 2
            self.connection.getSensor(distance_sensor)
            self.connection.go(speed, rotation)

            total = 0
            while True:
                distance = self.connection.getSensor(distance_sensor)
                total += abs(distance)
                if total >= abs(10 * speed * seconds):
                    break
            self.connection.stop()
        else:
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
        self._move_autonomously(speed, 0, 0, True)
        while self._forward_until_black_line:
            sensor_values = [self.connection.getSensor(sensor[0]), self.connection.getSensor(sensor[1])]
            if sensor_values[0] < darkness or sensor_values[1] < darkness: break
            time.sleep(0.05)
        self.stop()
    def go_forward_until_bumps(self, speed, bump_sensor):
        """
        Go forward at user-specified speed until WILMA bumps into something,
        where the user specifies whether to use the left bump sensor, the right bump sensor, or both.
        Feature: 5a-2
        Contributor: Xiangqing Zhang
        """
        self._job(self._go_forward_until_bumps, [speed, bump_sensor])
    def _go_forward_until_bumps(self, speed, bump_sensor):
        self._forward_until_bumps = True
        sensor = our_create.Sensors.bumps_and_wheel_drops
        self._move_autonomously(speed, 0, 0, True)
        while self._forward_until_bumps:
            sensor_values = self.connection.getSensor(sensor)
            left_bumper_state = sensor_values[3]
            right_bumper_state = sensor_values[4]
            if ("L" in bump_sensor) or ("l" in bump_sensor):
                if left_bumper_state == 1:
                    break
            if ("R" in bump_sensor) or ("r" in bump_sensor):
                if right_bumper_state == 1:
                    break
            time.sleep(0.05)
        self.stop()


    def _send_bytecode(self, bytecode_list):
        """
        Send a list of bytecodes using IR sender.
        ___ ___ ___ ___ ___ ___ ___ ___
         a   b   c   d   e   f   g   h
        a: 0 = Regular data; 1 = Special data
        b: If a == 1:
               0 = Content length;
               1 = Other commands;
        cdefgh: If a == 1 and b == 1:
               63 = Send done.
               62 = Group done.
               61 = Ignore this. Used in sending same data twice or more.
               60 = Illegal verify code.
        Send a group of at max 63 bytecodes.
        Contributor: Xiangqing Zhang
        """
        self._send_bytecode_flag = True
        start = 0
        robotLogger.add(bytecode_list, "_send_bytecode")
        while self._send_bytecode_flag and start<len(bytecode_list):
            end = start + 63 # [start, end)
            if end>len(bytecode_list): end = len(bytecode_list)
            content_length = end - start
            success = False
            while self._send_bytecode_flag and (not success):
                # Content length.
                binary_send = [1, 0]
                binary_send.extend(self.__to_binary(content_length, 6))
                binary_expected = [1, 1, 0, 0, 0, 0, 0, 0]
                self.connection.sendIR(self.__from_binary(binary_send))
                while self._send_bytecode_flag and binary_expected != self.__to_binary(self.__receive_bytecode()):
                    self.connection.sendIR(self.__from_binary(binary_send))
                # Content.
                for x in range(start, end):
                    if x > start and bytecode_list[x] == bytecode_list[x - 1]:
                        # Ignore this.
                        binary_send = [1, 1, 1, 0, 1, 1, 1, 1]
                        binary_expected = [1, 1, 0, 1, 0, 0, 0, 0]
                        self.connection.sendIR(self.__from_binary(binary_send))
                        while self._send_bytecode_flag and binary_expected != self.__to_binary(self.__receive_bytecode()):
                            self.connection.sendIR(self.__from_binary(binary_send))
                    current_data = bytecode_list[x]
                    robotLogger.add("%s, %s"%(current_data, self.__to_binary(current_data, 7)), "debugggggg")
                    binary_send = [0]
                    binary_send.extend(self.__to_binary(current_data, 7))
                    binary_expected = [0]
                    binary_expected.extend(self.__to_binary(current_data, 7))
                    self.connection.sendIR(self.__from_binary(binary_send))
                    while self._send_bytecode_flag and binary_expected != self.__to_binary(self.__receive_bytecode()):
                        self.connection.sendIR(self.__from_binary(binary_send))
                # Verify code.
                verify_bytecode = self.__verify_bytecode(bytecode_list[start:end])
                verify_binary = self.__to_binary(verify_bytecode, 6)
                binary_expected = [1, 0]
                binary_expected.extend(verify_binary)
                binary_send = [1, 1, 0, 1, 1, 1, 1, 1]
                self.connection.sendIR(self.__from_binary(binary_send))
                bytecode_received = self.__receive_bytecode()
                while self._send_bytecode_flag and bytecode_received == None:
                    self.connection.sendIR(self.__from_binary(binary_send))
                if binary_expected == self.__to_binary(bytecode_received):
                    # Verify code legal.
                    success = True
                else:
                    # Verify code illegal.
                    binary_send = [1, 1, 0, 0, 1, 1, 1, 1]
                    binary_expected = [1, 1, 1, 1, 0, 0, 0, 0]
                    self.connection.sendIR(self.__from_binary(binary_send))
                    while self._send_bytecode_flag and binary_expected != self.__to_binary(self.__receive_bytecode()):
                        self.connection.sendIR(self.__from_binary(binary_send))
            start += 63
        # Send done.
        binary_send = [1, 1, 1, 1, 1, 1, 1, 1]
        binary_expected = [1, 1, 1, 0, 0, 0, 0, 0]
        self.connection.sendIR(self.__from_binary(binary_send))
        while self._send_bytecode_flag and binary_expected != self.__to_binary(self.__receive_bytecode()):
            self.connection.sendIR(self.__from_binary(binary_send))
    def _receive_bytecode(self):
        """
        Send a list of bytecodes using IR sender.
        ___ ___ ___ ___ ___ ___ ___ ___
         a   b   c   d   e   f   g   h
        a: 0 = Confirm data; 1 = Special feedback
        b: If a == 0:
               0 = Verify code;
               1 = Other status;
        c: If a == 0 and b == 1:
               0 = Content length received.
               1 = Send done received.
               2 = Ignore this received.
               3 = Illegal verify code received.
        If a == 1:
            Other 7-bit should be the same as received.
        Send a group of at max 63 bytecodes.
        Notice: Always start self._receive_bytecode() before self._send_bytecode()!
        Contributor: Xiangqing Zhang
        """
        self._receive_bytecode_flag = True
        received_list = []
        received = False
        content_length = self.__from_binary(self.__to_binary(self.__receive_bytecode(-1))[2:])
        self.connection.sendIR(self.__from_binary([1, 1, 0, 0, 0, 0, 0, 0]))
        while self._receive_bytecode_flag and (not received):
            group_list = []
            each_data_pre = []
            x = -1
            while x < content_length:
                x += 1
                each_data = self.__to_binary(self.__receive_bytecode(-1))
                if each_data==[1, 1, 0, 1, 0, 0, 0, 0]:
                    binary_send = [1, 1, 0, 1, 0, 0, 0, 0]
                    self.connection.sendIR(self.__from_binary(binary_send))
                else:
                    binary_send = [0]
                    binary_send.extend(each_data[1:])
                    robotLogger.add("%s"%self.__from_binary(each_data), "received bytecode:")
                    self.connection.sendIR(self.__from_binary(binary_send))
                    if each_data != each_data_pre:
                        group_list.append(self.__from_binary(each_data[1:]))
                        x -= 1
                each_data_pre = each_data
            group_done = self.__receive_bytecode(-1)
            verify_bytecode = self.__verify_bytecode(group_list)
            verify_binary = [1, 0]
            verify_binary.extend(self.__to_binary(verify_bytecode))
            self.connection.sendIR(self.__from_binary(binary_send))
            verify_result = self.__to_binary(self.__receive_bytecode(-1))
            if verify_result==[1, 1, 1, 1, 0, 0, 0, 0]:
                binary_send = [1, 1, 1, 1, 0, 0, 0, 0]
                self.connection.sendIR(self.__from_binary(binary_send))
                group_list = []
            else:
                if verify_result==[1, 1, 0, 0, 0, 0, 0, 0]:
                    binary_send = [1, 1, 1, 0, 0, 0, 0, 0]
                    self.connection.sendIR(self.__from_binary(binary_send))
                    received = True
                else:
                    content_length = self.__from_binary(verify_result[2:])
                    self.connection.sendIR(self.__from_binary([1, 1, 0, 0, 0, 0, 0, 0]))
            received_list.extend(group_list)
        return received_list
    def __receive_bytecode(self, wait_cycles=10):
        """
        Wait until bytecode received. Will abort after wait_cycles.
        If wait_cycles==-1, it will wait forever until self.stop().
        Contributor: Xiangqing Zhang
        """
        self.__receive_bytecode_flag = True
        sensor = our_create.Sensors.ir_byte
        k = 0
        while self.__receive_bytecode_flag and (wait_cycles == -1 or k < wait_cycles):
            sensor_values = self.connection.getSensor(sensor)
            robotLogger.add("bytecode: %d; binary: %s" % (sensor_values, self.__to_binary(sensor_values)), "__receive_bytecode")
            if sensor_values != 255: return sensor_values
            time.sleep(self.ir_time)
            k += 1
        return None
    def __verify_bytecode(self, bytecode_list):
        """
        Verify the data by multiplying all the bytecodes and mod by 63.
        Contributor: Xiangqing Zhang
        """
        t = 1
        for eachData in bytecode_list:
            t *= eachData
        return t % 63
    def __from_binary(self, binary):
        """
        Converts and returns binary to bytecode.
        Contributor: Xiangqing Zhang
        """
        return sum([binary[k] * (2 ** k) for k in range(len(binary))])
    def __to_binary(self, bytecode, bytecode_length=8):
        """
        Converts and returns bytecode to binary.
        Contributor: Xiangqing Zhang
        """
        if bytecode == None: return None
        result = [0 for k in range(bytecode_length)]
        k = 0
        while bytecode > 0:
            result[k] = bytecode % 2
            bytecode //= 2
            k += 1
        return result

    def chat_with_another_robot(self, bytecode_string):
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
        self._job(self._chat_with_another_robot, [[int(k) for k in bytecode_string.split(",")]])
    def _chat_with_another_robot(self, bytecode_list):
        self._send_bytecode(bytecode_list)
        # self._sendIR = True
        # sensor = our_create.Sensors.ir_byte
        # k = 0
        # while self._sendIR and k<len(bytecode_list):
        #     bytecode = bytecode_list[k]
        #     t = Timer(0.1, lambda: self.connection.sendIR(bytecode))
        #     t.start()
        #     # self.connection.sendIR(bytecode)
        #     while self._sendIR:
        #         sensor_values = self.connection.getSensor(sensor)
        #         robotLogger.add("bytecode: %d" % sensor_values, "_chat_with_another_robot")
        #         if sensor_values != 255:
        #             break
        #         time.sleep(0.05)
        #     k += 1
        # t.cancel()
        self.stop()


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
        if coordinates == 'coordinates.txt':  # Coordinates can come from a file
            FO = open("coordinates.txt", "r")
            coordinates_from_file = FO.read()
            FO.close()
            coordinates_temp = coordinates_from_file.split()
            coordinates = [[0, 0]]
            for each_coordinate in coordinates_temp:
                coordinates.append(each_coordinate.split(","))
        elif type(coordinates) is list:  # Coordinates coming from user clicks on map
            print(coordinates)
            coordinates_temp = []
            for k in range(len(coordinates) // 2):
                coordinates_temp.append([coordinates[2 * k], coordinates[2 * k + 1]])

            coordinates = coordinates_temp
#             print(coordinates)

        else:  # Coordinates coming from list entry in main GUI
            coordinates_temp = coordinates.split()
            coordinates = [[0, 0]]
            for each_coordinate in coordinates_temp:
                coordinates.append(each_coordinate.split(","))

        for k in range(1, len(coordinates)):
            location = coordinates[k - 1]
            coordinate = coordinates[k]
            x_initial = float(location[0])
            y_initial = float(location[1])
            rotation_left = 45
            rotation_right = -45
            no_rotation = 0
            default_speed = 20
            max_speed = 40
            x = float(coordinate[0])
            y = float(coordinate[1])
            robotLogger.add("%d,%d==>%d,%d" % (x_initial, y_initial, x, y), "_grid_movement")

            y_distance = y - y_initial
            x_distance = x - x_initial
            r = math.sqrt(x_distance ** 2 + y_distance ** 2)
            if speed == 0:  # give an initial speed if none is provided
                speed = default_speed
            elif speed > 40:  # limit speed to 40 for accuracy
                speed = max_speed
            unit_time = (10 / speed) * r
#             print(speed, unit_time, speed * unit_time)

            if x_distance == 0 and y_distance > 0:  # positive y-axis
                degrees = no_rotation
            elif x_distance == 0 and y_distance < 0:  # negative y-axis
                degrees = rotation_left * 4
            elif y_distance == 0 and x_distance < 0:  # negative x-axis
                degrees = rotation_left * 2
            elif y_distance == 0 and x_distance > 0:  # positive x-axis
                degrees = rotation_right * 2
            else:
                radians = math.atan(y_distance / x_distance)
                degrees = radians * (180 / math.pi)

            if x_distance > 0 and y_distance > 0:  # 1st quadrant
                degrees = -degrees
            elif x_distance < 0 and y_distance > 0:  # 2nd quadrant
                degrees = -degrees
            elif x_distance < 0 and y_distance < 0:  # 3rd quadrant
                degrees = 90 + degrees
            elif x_distance > 0 and y_distance < 0:  # 4th quadrant
                degrees = -90 + degrees
            else:
                pass

            self.connection.go(0, degrees / 5)
            time.sleep(5)
            self.connection.go(speed, 0)
            time.sleep(4 * unit_time)
            self.connection.go(0, -degrees / 5)
            time.sleep(5)
            self.connection.stop()

        self.stop()
        robotLogger.add("Finished moving.", "_grid_movement", "SUCCESS")

    def go_forward_until_ir_signal(self, speed, bytecode):
        """
        Go forward at user-specified speed until WILMA hears a user-specified IR signal.
        User can generate a user-specified signal while doing so.
        Feature: 5b-1
        Contributor: Xiangqing Zhang
        """
        self._job(self._go_forward_until_ir_signal, [speed, bytecode]);
    def _go_forward_until_ir_signal(self, speed, bytecode):
        self._forward_until_ir_signal = True
        sensor = our_create.Sensors.ir_byte
        self._move_autonomously(speed, 0, 0, True)
        while self._forward_until_ir_signal:
            sensor_values = self.connection.getSensor(sensor)
            if sensor_values == bytecode:
                break
            time.sleep(0.05)
        self.stop()

    def go_forward_until_stuck(self, speed):
        """
        Go forward until it is “stuck” (still trying to move),
        no matter what the direction (not just forward).
        Feature: 5b-2
        Contributor: Xiangqing Zhang
        """
        self._job(self._go_forward_until_stuck, [speed]);
    def _go_forward_until_stuck(self, speed):
        self._forward_until_stuck = True
        self._move_autonomously(speed, 0, 0, True)
        sensor = our_create.Sensors.bumps_and_wheel_drops
        while self._forward_until_stuck:
            sensor_values = self.connection.getSensor(sensor)
            left_bumper_state = sensor_values[3]
            right_bumper_state = sensor_values[4]
            if left_bumper_state == 1 or right_bumper_state == 1:
                total_time = 0
                self._move_autonomously(speed, 45, 0, True)
                while self._forward_until_stuck and total_time < 10:
                    time.sleep(0.05)
                    sensor_values = self.connection.getSensor(sensor)
                    left_bumper_state = sensor_values[3]
                    right_bumper_state = sensor_values[4]
                    robotLogger.add("%d, %d" % (left_bumper_state, right_bumper_state), "_go_forward_until_stuck")
                    if left_bumper_state == 1 or right_bumper_state == 1:
                        total_time += 0.1
                    else:
                        break
                if total_time > 1: break
                self._move_autonomously(speed, 0, 0, True)
            time.sleep(0.05)
        self.stop()

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
                self._move_autonomously(self._teleportspeed[0] + 10, 0, 0, True)
                self._teleportspeed[0] += 10
            else:
                self._move_autonomously(10, 0, 0, True)
                self._teleportspeed[0] = 10
                self._teleportspeed[1] = 0
        if(command == "Backward"):
            if(self._teleportspeed[0] < 0):
                self._move_autonomously(self._teleportspeed[0] - 10, 0, 0, True)
                self._teleportspeed[0] -= 10
            else:
                self._move_autonomously(-10, 0, 0, True)
                self._teleportspeed[0] = -10
                self._teleportspeed[1] = 0
        if(command == "Right"):
            if(self._teleportspeed[1] < 0):
                self._move_autonomously(0, self._teleportspeed[1] - 30, 0, True)
                self._teleportspeed[1] += -30
            else:
                self._move_autonomously(0, -30, 0, True)
                self._teleportspeed[1] = -30
                self._teleportspeed[0] = 0
        if(command == "Left"):
            if(self._teleportspeed[1] > 0):
                self._move_autonomously(0, self._teleportspeed[1] + 30, 0, True)
                self._teleportspeed[1] += 30
            else:
                self._move_autonomously(0, 30, 0, True)
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
            if (sensor_value[0] < darkness and sensor_value[1] < darkness and temp1) or (sensor_value[0] < darkness and temp1):
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

    def de_en_code_message(self, message):
        """
        Uses codes to send letters, words and entire phrases.
        Encrypts and decrypts (perhaps as simple as Caesar’s cipher,
        or as complicated as a public key encryption system).

        Feature: 8b
        Contributor: Xiangqing Zhang
        """
        if message.get():
            self._job(self._encode_code_message, [message.get()])
        else:
            self._job(self._decode_code_message, [message])
    def _encode_code_message(self, message):
        self._encode_message = True
        self._send_bytecode(self.robotEncryption.toIR(self.robotEncryption.encrypt(message)))
    def _decode_code_message(self, message):
        bytecode_list = self._receive_bytecode()
        message.set(self.robotEncryption.decrypt(self.robotEncryption.fromIR(bytecode_list)))

    def take_other_robot(self, speed, bytecode):
        """
        The robot that takes WILMA to go.
        IR signal:
            0 = Stop
            1 = Turn Left
            2 = Turn Right
            Bytecode Specified = Go

        Feature: 9-1
        Contributor: Xiangqing Zhang
        """
        self._job(self._take_other_robot, [speed, bytecode])
    def _take_other_robot(self, speed, bytecode):
        self._take_other_robot_flag = True
        self.connection.go(speed, 0)
        sensor = our_create.Sensors.ir_byte
        sensor_distance = our_create.Sensors.distance
        is_discovered = False
        while self._take_other_robot_flag:
            self.connection.sendIR(bytecode)
            sensor_values = self.connection.getSensor(sensor)
            if sensor_values == bytecode:
                # Being discovered!
                is_discovered = True
                direction = random.randint(0, 1)
                if direction == 0: direction = -1
                if direction == 0:
                    bytecode_direction = 1
                else:
                    bytecode_direction = 2
                rotation = random.randint(20, 40) * direction
                seconds = random.randint(5)

                distance_moved = 0
                distance = distance * seconds * 10
                self.connection.getSensor(sensor_distance)
                self.connection.go(speed, rotation)
                while distance_moved < distance:
                    self.connection.sendIR(bytecode_direction)
                    time.sleep(0.05)
            elif is_discovered:
                is_discovered = False
                self.connection.go(speed, 0)
            time.sleep(0.05)
        self.stop()
    def follow_other_robot(self, speed, bytecode):
        """
        WILMA follows another robot that is emitting an IR signal.
        Notice: call self.take_other_robot() before self.follow_other_robot()!
        IR signal:
            Bytecode Specified = Got you!

        Feature: 9-2
        Contributor: Xiangqing Zhang
        """
        self._job(self._follow_other_robot, [speed, bytecode])
    def _follow_other_robot(self, speed, bytecode):
        self._follow_other_robot_flag = True
        sensor = our_create.Sensors.ir_byte
        self.connection.go(speed, 0)
        anticipated_direction = "LEFT"
        while self._follow_other_robot_flag:
            sensor_values = self.connection.getSensor(sensor)
            if sensor_values == bytecode:
                self.connection.sendIR(bytecode)
            elif sensor_values == 1:
                anticipated_direction = "LEFT"
            elif sensor_values == 2:
                anticipated_direction = "RIGHT"
            else:
                rotation = 30
                if anticipated_direction == "RIGHT": rotation *= -1
                self.connection.go(speed, rotation)
                while self.connection.getSensor(sensor) != bytecode:
                    self.connection.go(speed, rotation)
            time.sleep(0.05)
        self.stop()

    def chat_with_robot(self, message):
        """
        WILMA offers Rogerian psychotherapy, ala Eliza (http://en.wikipedia.org/wiki/ELIZA).
        Uses a third-party library by Joe Strout.
        Converted from Python 2.0 to Python 3.3 by Xiangqing Zhang.
        Feature: 12
        Contributor: Xiangqing Zhang
        """
        robotLogger.add(message.get(), "You say:", "INFO")
        robotLogger.add(self.eliza.respond(message.get()), "Wilma says:", "INFO")
        message.set("")

    def sing_and_dance(self):
        """
        Robot will sing and dance for the user.
        Feature 10
        Contributor: Matthew O'Brien
        """
        self._job(self._sing_and_dance);
    def _sing_and_dance(self):
        dance_data = [[50, 0, 1], [0, 180, 1], [30, 40, 1], [30, -40, 1.3], [0, 180, 1.2], [30, 40, 1.2], [30, -40, 1.3], [-30, -40, 1.2], [0, 180, 0.3], [0, -180, 0.3],
                      [-30, 40, 1.2], [40, 0, 1.2], [-30, 0, 0.3], [30, 0, 0.3], [50, 130, 2], [0, 180, 1.2], [0, -180, 1.2], [-30, 0, 0.8], [25, 50, 1.2], [50, 50, 1.2], [25, 50, 1.2],
                      [50, 50, 1.1], [0, 220, 1.8], [-30, 0, 0.2], [30, 0, 0.2], [-30, 0, 0.2], [30, 0, 0.2], [-30, 0, 0.2], [30, 0, 0.2], [-30, 0, 0.2], [30, 0, 0.2], [-40, 35, 1.2],
                      [40, 0, 1.2], [0, 180, 1], [20, 20, 0.4], [40, -40, 0.4], [60, 60, 0.4], [50, -90, 2.1], [45, 0, 0.7], [30, 0, 0.7], [15, 0, 0.7], [0, 0, 1]]

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

        is_playing_sensor = our_create.Sensors.song_playing
        for k in range(len(fur_elise)):
            self.connection.playSong(fur_elise[k])
            j = 0
            while True:
                self.connection.go(dance_data[j][0], dance_data[j][1])
                time.sleep(dance_data[j][2])
                j += 1
                is_playing = self.connection.getSensor(is_playing_sensor)
                if not is_playing:
                    break
        self.connection.stop()

    def __repr__(self):
        """
        Returns a string that represents this object.
        Contributor: Xiangqing Zhang
        """
        return 'An our_create robot connection with port {}'.format(self.port)

if __name__ == '__main__':
    print("Welcome to the ROBOT CLASS!")
