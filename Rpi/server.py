import zmq, serial

COMMAND_PORT = "5556"

context = zmq.Context()
socket = context.socket(zmq.REP)

ser = serial.Serial('/dev/ttyACM0', 9600)

try:
    socket.bind("tcp://*:" + COMMAND_PORT)
except:
    print_str = "Failed to bind at port %s" % (COMMAND_PORT)

while(True):
    message = socket.recv()    
    
    ser.write(message)
    message = ser.readline()

    socket.send(message)

ser.close()
socket.close()
context.destroy()
