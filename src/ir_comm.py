import threading;
import time;
import new_create;
import 

class IR_Comm(object):
    def __init__(self, connection, callback):
        self._receiving_buffer = [];
        self._sending_buffer = [];
        self._connection = connection;
        self._callback = callback;
        self._running = False;
        self._received_string = [];
        self._sending_pause = False;
    def start(self):
        self._running = True;
        self._r = threading.Thread(target=self._receiving);
        self._s = threading.Thread(target=self._sending);
        self._m = threading.Thread(target=self._messaging);
        self._r.daemon = True;
        self._s.daemon = True;
        self._m.daemon = True;
        self._r.start();
        self._s.start();
        self._m.start();
    def stop(self):
        self._running = False;
    def _receiving(self):
        old_rec = None;
        while(self._running):
            tmp = self._connection.getSensor("IR_BYTE");
            if(tmp == old_rec):
                continue;
            old_rec = tmp;
            if(tmp!=255):
                self._receiving_buffer.append(tmp);
    def _sending(self):
        while(self._running):
            if(len(self._sending_buffer)!=0):
                self._connection.sendIR(self._sending_buffer[0]);
                del self._sending_buffer[0];
    def _messaging(self):
        while(self._running or (len(self._receiving_buffer)!=0)):
            if(len(self._receiving_buffer)!=0):
                self._callback(self._receiving_buffer[0]);
                del self._receiving_buffer[0];
    def send_data(self,data):
        self._sending_buffer.append(data);

def printout(num):
    print(num);
        
if __name__ == '__main__':
    connection = new_create.Create("/dev/ttyUSB3");
    temp = [];
    ir = IR_Comm(connection, printout);
    ir.start();
    while(1):
        ir.send_data(156);
        time.sleep(1);