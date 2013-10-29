import new_create as our_create
from threading import Timer, Thread
from job import Job

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
        assert self.connection, "Please create the connection first!"
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
        print(datetime.datetime.now().strftime("%H:%M:%S"), "[%s] <%s> %s"%(method_name, level, message))
    def connect(self):
        if not self.connection:
            try:
                self.connection = new_create.Create(self.port)
            except Exception as e:
                self._log("Error occured while connecting: %s" % e, "connect")
    def disconnect(self):
        if self.connection:
            self.connection.stop()
            self.connection.shutdown()
            self.connection = None
    def stop(self):
        assert self.connection, "Please create the connection first!"
        self.connection.stop()
    def go_forward_until_black_line(self, speed, darkness=500):
        """
        Go forward at user-specified speed until WILMA reaches a black line,
        where the user specifies the “darkness” of the line.
        Feature: 5a-1
        Contributor: Xiangqing Zhang
        """
        self.stop() # TODO: Please add this to all methods that will be sent to our_create.
        self._job(self._go_forward_until_black_line, [speed, darkness])
    def _go_forward_until_black_line(self, speed, darkness):
        sensor = [our_create.cliff_front_left_signal, our_create.cliff_front_right_signal]
        # TODO: MARK.
        
    def __repr__(self):
        """
        Returns a string that represents this object.
        Contributor: Xiangqing Zhang
        """
        return 'An our_create robot connection with port {}'.format(self.port)
print("hello")

# git add .
# git status
# git commit -m "message"
# git push
