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


def create_csv(csv_data, muestras):

    now = datetime.now()
    dt_string = now.strftime("%d%m%Y_%H%M%S")
    file_name = "mediciones_" + str(dt_string) + ".csv"
    path = "/Users/jpav/Documents/Scripts/Data_files/" + str(file_name)
    f = open(path, "w")
    f.write("Ch,Med1,Med2,Med3,Med4,Med5,Med6,Med7,Med8,Med9,Med10")
    f.write("\n")

    for file_data in csv_data:

        n = 0
        i = 0
        chain = str(i) + ","

        if len(file_data) > muestras:
            div = len(file_data) / 4
        else:
            div = muestras

        for data in file_data:

            chain += str(data) + ","
            n += 1
            if n % div == 0:
                f.write(chain)
                f.write("\n")
                i += 1
                chain = str(i) + ","
                n = 0

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

    T = []
    H = []
    adc0 = []
    adc1 = []
    adc2 = []

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

    while tiempo.minute - minuto_inicio < 2:
        print("Muestra: " + str(muestras + 1) + " por 2 minutos")

        ser.write('t'.encode())
        time.sleep(1)
        T = T + leer_serial(1, ser)

        ser.write('H'.encode())
        H = H + leer_serial(1, ser)

        ser.write('0'.encode())
        adc0 = adc0 + leer_serial(4, ser)

        ser.write('1'.encode())
        adc1 = adc1 + leer_serial(4, ser)

        ser.write('2'.encode())
        adc2 = adc2 + leer_serial(4, ser)

        muestras += 1
        tiempo = datetime.now()

    adcs = [adc0, adc1, adc2]
    adcs_new = [[]] * 3
    index = 0

    for i in adcs:
        adcx_0 = i[0::4]
        adcx_1 = i[1::4]
        adcx_2 = i[2::4]
        adcx_3 = i[3::4]
        adcs_new[index] = adcx_0 + adcx_1 + adcx_2 + adcx_3
        index += 1

    adc0 = adcs_new[0]
    adc1 = adcs_new[1]
    adc2 = adcs_new[2]

    csv_data = [T, H, adc0, adc1, adc2]
    create_csv(csv_data, muestras)
    upload_data()


def main():
    sched = BlockingScheduler()

    #    sched.add_job(mediciones, 'cron', day_of_week='mon-sun', hour='9,13,17,21')
    sched.add_job(mediciones, 'cron', day_of_week='mon-sun', hour='10', minute='33,36')
    sched.start()


if __name__ == "__main__":
    main()
