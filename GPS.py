import serial 

port = "/dev/serial0"

def parse(data):
    if data[0:6] == "$GPGGA":
        s = data.split(",")
        if s[7] == '0':
            print "No satellite data available"
            return
        
        time = s[1][0:2] + ":" + s[1][2:4] + ":" + s[1][4:6]
        
        lat = decode(s[2])
        dirLat = s[3]
        
        lon = decode(s[4])
        dirLon = s[5]
        
        alt = s[9] + " m"
        sat = s[7]
        
        print "Latitude: %s(%s) -- Longitude %s(%s)" %(lat, dirLat, lon, dirLon)
 
 
def decode(coord):
    v = coord.split(".")
    
    head = v[0]
    tail = v[1]
    
    deg = head[0:-2]
    min = head[-2:]
    
    return deg + min + "." + tail


ser = serial.Serial(port, baudrate=9600, timeout=0.5)
while True:
    data = ser.readline()
    parse(data)
