#!/usr/bin/env python
import serial
import time
from datetime import datetime


def create_csv(csv_data):

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

        for data in file_data:

            chain += str(data) + ","
            n += 1
            if n % 10 == 0:
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

    n = 0

    while n < 10:
        print("Iteracion: " + str(n + 1) + " de 10")

        ser.write('T'.encode())
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

        n += 1

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
    create_csv(csv_data)


def main():

    mediciones()


if __name__ == "__main__":
    main()
