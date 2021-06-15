import pandas as pd
import DecisionTreeRegressor
import datetime

def preprocess():

    columns_names=['Date','Time','In_Temperature','In_Humidity','SB-51-00','SP-11-00','SP-19-01'
        ,'TGS2602-B00','TGS2620-C00','SP-31-00','SP3S-AQ2-01']

    df_processed = pd.DataFrame(columns=columns_names)
    df_classifier = pd.DataFrame(columns=columns_names)


    model_data = pd.read_csv('../smartiago_v2/Mean_Data.csv')
    df = pd.read_csv('../smartiago/Mean_Data.csv')

    model_SB5100 = DecisionTreeRegressor.create_model(model_data,"SB-51-00")
    model_SP1100 = DecisionTreeRegressor.create_model(model_data,"SP-11-00")
    model_SP1901 = DecisionTreeRegressor.create_model(model_data,"SP-19-01")
    model_TGS2602 = DecisionTreeRegressor.create_model(model_data,"TGS2602-B00")
    model_TGS2620 = DecisionTreeRegressor.create_model(model_data,"TGS2620-C00")
    model_SP3100 = DecisionTreeRegressor.create_model(model_data,"SP-31-00")
    model_SP3SAQ201 = DecisionTreeRegressor.create_model(model_data,"SP3S-AQ2-01")


    s1=0
    s2=0
    s3=0
    s4=0
    s5=0
    s6=0
    s7=0

    for index,row in df.iterrows():

        date = row['Date']
        time = row['Time']

        hour,min,sec=time.split(":")

        hour = int(hour)
        min = int(min)
        sec = int(min)

        temp = row["Temperature"]
        hum = row["Humidity"]

        if (((hour >= 10 and min) and (hour <= 12)) or ((hour >= 14) and (hour < 16))):

            SB5100 = s1
            SP1100 = s2
            SP1901 = s3
            TGS2602 = s4
            TGS2620 = s5
            SP3100 = s6
            SP3SAQ201 = s7

        else:

            SB5100 = abs(row["SB-51-00"]-model_SB5100.predict([[temp,hum]])[0])
            SP1100 = abs(row["SP-11-00"]-model_SP1100.predict([[temp,hum]])[0])
            SP1901 = abs(row["SP-19-01"]-model_SP1901.predict([[temp,hum]])[0])
            TGS2602 = abs(row["TGS2602-B00"]-model_TGS2602.predict([[temp,hum]])[0])
            TGS2620 = abs(row["TGS2620-C00"]-model_TGS2620.predict([[temp,hum]])[0])
            SP3100 = abs(row["SP-31-00"]-model_SP3100.predict([[temp,hum]])[0])
            SP3SAQ201 = abs(row["SP3S-AQ2-01"]-model_SP3SAQ201.predict([[temp,hum]])[0])

            df_temp=pd.DataFrame([[date, time, temp, hum, SB5100, SP1100, SP1901,

                TGS2602, TGS2620, SP3100, SP3SAQ201]], columns=columns_names)

            df_classifier=df_classifier.append(df2, ignore_index=True)

            s1 = SB5100
            s2 = SP1100
            s3 = SP1901
            s4 = TGS2602
            s5 = TGS2620
            s6 = SP3100
            s7 = SP3SAQ201

        df2=pd.DataFrame([[date, time, temp, hum, SB5100, SP1100, SP1901,

            TGS2602, TGS2620, SP3100, SP3SAQ201]], columns=columns_names)

        df_processed=df_processed.append(df2, ignore_index=True)

    df_processed.to_csv('Data_processed/processed_no.csv')
    df_classifier.to_csv('Data_processed/processed_classifier.csv')


    return 0

def main():

    preprocess()

    return 0


if __name__ == "__main__":
    main()
