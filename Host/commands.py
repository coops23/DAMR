import sys, zmq, vlc, user, math, GenerateMap
import time

ROBOT_ADDRESS = "192.168.0.28"
VIDEO_STREAM_PORT = "5555"
COMMAND_PORT = "5556"

WHEEL_DIAMETER = 65
WHEEL_ENCODER_RESOLUTION = 10
WHEEL_DISTANCE_PER_TICK = math.pi*WHEEL_DIAMETER*0.1
SERVO_SPEED_DEGREE = 0.0035

SERVO_MIDDLE_POS = 100
SCAN_SAMPLE_SIZE = 20
SCAN_ANGLE_WIDTH = 150

class Command():
    def __init__(self, frame):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.Connect()
        self.map = GenerateMap.GenerateMap()

        self.frame = frame

        # creating a basic vlc instance
        self.instance = vlc.Instance()
        # creating an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()
        self.mediaplayer.set_mrl('http://' + ROBOT_ADDRESS + ":" + VIDEO_STREAM_PORT)
        self.isPaused = False

        if sys.platform == "linux2": # for Linux using the X Server
            self.mediaplayer.set_xwindow(self.frame.winId())
        elif sys.platform == "win32": # for Windows
            self.mediaplayer.set_hwnd(self.frame.winId())
        elif sys.platform == "darwin": # for MacOS
            self.mediaplayer.set_nsobject(self.frame.winId())

    def Connect(self):
        try:
            self.socket.connect("tcp://" + ROBOT_ADDRESS + ":" + COMMAND_PORT)
        except:
            print_str = "Failed to connect to %s:%s" % (ROBOT_ADDRESS, COMMAND_PORT)
            return print_str 
   
        print_str = "Connected to %s:%s" % (ROBOT_ADDRESS, COMMAND_PORT)

        return print_str

    def ParseResponse(self, message):
        print_str = ""
        if not message.strip():
            print_str += "nothing"
            return (0, 0)
        value = (int(message, 10) & 0xFFF0) >> 4
        status = int(message, 10) & 0xF
        return (value, status)

    def Forward(self, movementValue):
        value = (10 * movementValue) / WHEEL_DISTANCE_PER_TICK        
        request = int(round(value)) << 4     
        request += 4 
        print_str = "forward " + str(int(round(value)) * WHEEL_DISTANCE_PER_TICK) + "mm"
        self.socket.send(str(request))
        message = self.socket.recv()
        (_, response) = self.ParseResponse(message)
        if(response == 1):
            print_str += "\nSuccess"
        else:
            print_str += "\nError"
    
        distance = (int(round(value)) * WHEEL_DISTANCE_PER_TICK)
        (status, bearing) = self.Bearing()
        self.map.SetX(((self.map.GetX()) + (math.sin(math.radians(int(bearing))) * distance))/self.map.GetMapScale())
        self.map.SetY(((self.map.GetY()) + (math.cos(math.radians(int(bearing))) * distance))/self.map.GetMapScale())
        self.map.Update()

        return print_str

    def Backward(self, movementValue):
        value = (10 * movementValue) / WHEEL_DISTANCE_PER_TICK        
        request = int(round(value)) << 4     
        request += 5 
        print_str = "forward " + str(int(round(value)) * WHEEL_DISTANCE_PER_TICK) + "mm"
        self.socket.send(str(request))
        message = self.socket.recv()
        (_, response) = self.ParseResponse(message)
        if(response == 1):
            print_str += "\nSuccess"
        else:
            print_str += "\nError"

        distance = (int(round(value)) * WHEEL_DISTANCE_PER_TICK)
        (status, bearing) = self.Bearing()
        self.map.SetX(((self.map.GetX()) - (math.sin(math.radians(int(bearing))) * distance))/self.map.GetMapScale())
        self.map.SetY(((self.map.GetY()) - (math.cos(math.radians(int(bearing))) * distance))/self.map.GetMapScale())
        self.map.Update()

        return print_str

    def Left(self, angleValue):        
        request = angleValue << 4   
        request += 6 
        print_str = "left " + str((request & 0xFFF0) >> 4) + " degrees"
        self.socket.send(str(request))
        message = self.socket.recv()
        (value, response) = self.ParseResponse(message)
        if(response == 1):
            print_str += "\nSuccess"
        else:
            print_str += "\nError"

        return print_str

    def Right(self, angleValue):
        request = angleValue << 4   
        request += 7 
        print_str = "right " + str((request & 0xFFF0) >> 4) + " degrees"
        self.socket.send(str(request))
        message = self.socket.recv()
        (value, response) = self.ParseResponse(message)
        if(response == 1):
            print_str += "\nSuccess"
        else:
            print_str += "\nError"

        return print_str

    def Distance(self):
        request = "10"
        self.socket.send(request)
        message = self.socket.recv()
        (value, response) = self.ParseResponse(message)
        print_str = ""
        print_str += str(value) + "mm\n"
        if(response == 1):
            print_str += "Success"
        else:
            print_str += "Error"
    
        return (print_str, str(value))

    def Bearing(self):
        request = "9"
        self.socket.send(request)
        message = self.socket.recv()
        (value, response) = self.ParseResponse(message)
        print_str = ""
        if(response == 1):
            print_str += "Success"
        else:
            print_str += "Error"
    
        return (print_str, str(value))
    
    def Scan(self):
        increment = 90 / SCAN_SAMPLE_SIZE
        i = SERVO_MIDDLE_POS - (SCAN_ANGLE_WIDTH / 2)
        index = 0
        distances = []
        angles = []
        while(i <= (SERVO_MIDDLE_POS + (SCAN_ANGLE_WIDTH / 2))):
            self.Servo(i)
            (print_str, distance) = self.Distance()
            distances.append(int(distance))
            angles.append(i - SERVO_MIDDLE_POS)
            i = i + increment
        
        (status, bearing) = self.Bearing()
        bearing = math.radians(int(bearing))
        for i in range(len(angles)):
            anglesMap = math.radians(angles[i])
            x = 0
            y = 0
            if(bearing > anglesMap):
                anglesMap = math.fabs(anglesMap)
                bearing = math.fabs(bearing)
                anglesMap = bearing - anglesMap
                x = ((self.map.GetX()) + (math.sin(anglesMap) * distances[i]))
                y = ((self.map.GetY()) + (math.cos(anglesMap) * distances[i]))
            elif(bearing < anglesMap):
                anglesMap = math.fabs(anglesMap)
                bearing = math.fabs(bearing)
                anglesMap = anglesMap - bearing
                x = ((self.map.GetX()) + (math.sin(anglesMap) * distances[i]))
                y = ((self.map.GetY()) + (math.cos(anglesMap) * distances[i]))
            self.map.AddPoint(x, y)
        self.map.Update()

        return "Scan Done"
    
    def Servo(self, position):
        request = "2"
        self.socket.send(request)
        message = self.socket.recv()
        (initialPosition, response) = self.ParseResponse(message)
        print_str = ""
        if(response == 1):
            print_str += "Success"
        else:
            print_str += "Error"

        request = position << 4  
        request += 0
        self.socket.send(str(request))
        message = self.socket.recv()
        (value, response) = self.ParseResponse(message)
        print_str = ""
        if(response != 1):
            print_str += "Error"                   

        delayTime = (math.fabs(position - initialPosition) * SERVO_SPEED_DEGREE) * 2
        time.sleep(delayTime)

        return print_str

    def StreamVideo(self):
        """Toggle play/pause status
        """
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            #self.videoButton.setText("Stream Video")
            print_str = "Stream Video"
            self.isPaused = True
        else:
            self.mediaplayer.play()
            #self.videoButton.setText("Stop Stream")
            print_str = "Stop Stream"
            self.isPaused = False 

        return print_str

