#!/usr/bin/env python3

import time
import i2c_sensor
import subprocess
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime


def upload_data():
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y_%H%M%S")
    process = subprocess.Popen('/home/pi/repo/Enose/gitpush.sh %s' % (str(dt_string),), shell=True)
    process.wait()
    return 0


def create_csv(csv_data):

    now = datetime.now()
    date = now.strftime("%d%m%Y")
    hour = now.strftime("%H%M%S")
    file_name = "mediciones_smartiago_" + str(date) + ".csv"
    path = "/home/pi/repo/Enose/smartiago/" + str(file_name)

    if os.path.isfile(path):

        f = open(path, "a")

    else:

        f = open(path, "w")
        date = now.strftime("%d/%m/%Y")
        f.write("Date,Time,Temperature,Humidity,SP3S-AQ2-01,TGS832-A00,TGS822,SP-11-00,NA,SK25F,NA,SB-51-00,SP-19-01,SP-31-00,TGS2602-B00,TGS2620-C00")
        f.write("\n")

    mean_div = len(csv_data)
    new_arr = [0] * len(csv_data[0])

    for file_data in csv_data:

        n = 0
        chain = ""
        size = len(file_data)

        for data in file_data:

            new_arr[n] += data
            n += 1

    average = [x / mean_div for x in new_arr]

    size = len(average)
    n = 0
    chain = ""

    for data in average:

        n += 1
        if n == size:
            chain += str(data)
        else:
            chain += str(data) + ","

    chain = now.strftime("%d/%m/%Y,%H:%M:%S") + "," + chain
    f.write(chain)
    f.write("\n")
    f.close()
    return chain


def update_mean(chain):

    path = "/home/pi/repo/Enose/smartiago/Mean_Data.csv"
    f = open(path, "a")
    f.write(chain)
    f.write("\n")
    f.close()

    return 0


def mediciones():
    now = datetime.now()
    muestras = 0
    csv_data = []
    num_muestras = 30
    temp_obj = 25
    wait_time = 15

    print("Starting Heating")

    i2c_sensor.mcp23008(0, "OUT", True, 0x23)
    time.sleep(300)

    minute_start = now.minute

    while True:

        now = datetime.now()

        temperature = i2c_sensor.sht31("temp", 1)
        time.sleep(1)

        if (temperature>temp_obj or now.minute-minute_start > wait_time):

            print("Temperature reached, taking measures: "+str(temperature)+"C")
            print("-----------------------------------------")

            while muestras < num_muestras:
                T = []
                H = []

                print("Sample: " + str(muestras + 1) + " of " + str(num_muestras))

                T.append(i2c_sensor.sht31("temp", 1))
                H.append(i2c_sensor.sht31("hum", 1))
                adc0 = i2c_sensor.ads1115_4ch(0x48, 1)
                adc1 = i2c_sensor.ads1115_4ch(0x49, 1)
                adc2 = i2c_sensor.ads1115_4ch(0x4B, 1)

                csv_data.append(T + H + adc0 + adc1 + adc2)

                muestras += 1

            i2c_sensor.mcp23008(0, "OUT", False, 0x23)
            avr_list = create_csv(csv_data)
            update_mean(avr_list)
            upload_data()
            print("Data recollection ended successfully")
            break

        else:
            print("Device heating sensors " + "Goal temperature: " + str(temp_obj))
            print("Temperature read: " + str(temperature) + " C")
            print("------------------------------------------------")


def main():
    
    sched = BlockingScheduler()

    sched.add_job(mediciones, 'cron', day_of_week='mon-sun', hour='0-23', minute="0,20,40")
    sched.start()
#    mediciones()


if __name__ == "__main__":
    main()
