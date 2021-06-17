import serial 

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
        
        return [lat,dirLat,lon,dirLon]
 
def decode(coord):
    v = coord.split(".")
    
    head = v[0]
    tail = v[1]
    
    deg = head[0:-2]
    min = head[-2:]
    
    return deg + min + "." + tail

def readGPS():

    port = "/dev/serial0"
    lat=0
    lon=0
    dirLar=0
    dirLon=0
    ser = serial.Serial(port, baudrate=9600, timeout=0.5)
    while True:
        data = ser.readline()
        if ("$GPGGA" in data):
            lat,dirLat,lon,dirLon = parse(data)
        break
    return [lat,dirLat,lon,dirLon]

def main():
    lat,dirLat,lon,dirLon=readGPS()
    print "Latitude: %s(%s) -- Longitude %s(%s)" %(lat, dirLat, lon, dirLon)

if __name__ == "__main__":
    main()
