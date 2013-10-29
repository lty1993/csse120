import threading
class Job(threading.Thread):
    """
    The robot's job class.
    Keep in mind that currently there is only one robot.
    Therefore, there must not be more than one Job class.
    Author: Xiangqing Zhang
    Reference: http://docs.python.org/3.3/library/threading.html
    """
    in_use = False
    def __init__(self, function, args=None, kwargs=None):
        assert not Job.in_use, "There must not be more than one Job class!"
        Job.in_use = True
        self.job_function = function
        self.job_args = args if args is not None else []
        self.job_kwargs = kwargs if kwargs is not None else {}
        # Prefix "job_" helps avoid conflicts with fields in the Threading class.
        self.terminated = False
        super().__init__()
    def run(self):
        self.job_function(*self.job_args, **self.job_kwargs)
        while 1:
        	if self.terminated: break
        Job.in_use = False

def main():
	import time
	def add(a, b=1):
		print(a + b)
	job_1 = Job(add, [1])
	job_1.start()
	time.sleep(3)
	job_1.terminated = True
	while job_1.is_alive(): pass
	job_1 = None
	job_2 = Job(add, [2], {"b": 1})
	job_2.start()
	time.sleep(3)

if __name__ == '__main__':
	main()