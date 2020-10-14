#!/usr/bin/env python
import serial
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from subprocess import Popen


def upload_data():
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y_%H%M%S")
    Popen('./gitpush.sh %s' % (str(dt_string),), shell=True)
    return 0


def create_csv(csv_data):
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y_%H%M%S")
    file_name = "mediciones_" + str(dt_string) + ".csv"
    path = "/Users/jpav/Documents/Enose/Data_files/" + str(file_name)
    f = open(path, "w")

    f.write(",,48,48,48,48,49,49,49,49,4B,4B,4B,4B")
    f.write("\n")
    f.write(",,0,1,2,3,0,1,2,3,0,1,2,3")
    f.write("\n")
    f.write(
        "Temperatura,Humedad,SP3S-AQ2-01,TGS832-A00,TGS822,4 ó 1,NA,SK25F,NA,SB-51-00,4 ó 1,SP-31-00,TGS2602-B00,TGS2620-C00")
    f.write("\n")

    for file_data in csv_data:

        n = 0
        chain = ""
        size = len(file_data)

        for data in file_data:

            chain += str(data) + ","
            n += 1
            if n == size:
                f.write(chain)
                f.write("\n")

    return 0


def leer_serial(data, ser):
    n = 0
    x = []  # Return of the serial read

    while n < data:

        while ser.in_waiting:
            msg = ser.readline()
            msg = msg.rstrip()
            msg = msg.decode("utf-8")
            if msg != "":
                x.append(msg)
                n += 1

    return x


def mediciones():
    tiempo = datetime.now()

    ser = serial.Serial(

        port='/dev/tty.usbmodem142101',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1,

    )

    ser.readline()
    time.sleep(1)
    ser.flushInput()

    muestras = 0

    minuto_inicio = tiempo.minute

    csv_data = []

    while tiempo.minute - minuto_inicio < 2:

        print("Muestra: " + str(muestras + 1) + " por 1 minutos")

        ser.write('T'.encode())
        time.sleep(1)
        T = leer_serial(1, ser)

        ser.write('H'.encode())
        H = leer_serial(1, ser)

        ser.write('0'.encode())
        adc0 = leer_serial(4, ser)

        ser.write('1'.encode())
        adc1 = leer_serial(4, ser)

        ser.write('2'.encode())
        adc2 = leer_serial(4, ser)

        tiempo = datetime.now()

        csv_data.append(T + H + adc0 + adc1 + adc2)
        muestras += 1

    create_csv(csv_data)
    upload_data()


def main():
    sched = BlockingScheduler()

    sched.add_job(mediciones, 'cron', day_of_week='mon-sun', hour='9,13,17,21')
#    sched.add_job(mediciones, 'cron', day_of_week='mon-sun', hour='18', minute='00,02')
    sched.start()

if __name__ == "__main__":
    main()
