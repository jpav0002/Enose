import pandas as pd
import DecisionTreeRegressor
import datetime
import treeClassifier

def check_time(time):

    hour,min,sec=time.split(":")

    hour = int(hour)
    min = int(min)
    sec = int(min)

    invalid=False

    if ((hour >= 10 ) and (hour <= 12)) or ((hour >= 14) and (hour < 17)):

        valid=True

    else:

        valid=False

    return valid

def preprocess():

    columns_names=['Date','Time','In_Temperature','In_Humidity','SB-51-00','SP-11-00','SP-19-01'
        ,'TGS2602-B00','TGS2620-C00','SP-31-00','SP3S-AQ2-01']

    df=pd.read_csv('../../smartiago_v2/Mean_data.csv')

    df_processed = pd.DataFrame(columns=columns_names)
    df_classifier = pd.DataFrame(columns=columns_names)

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

        valid=check_time(time)

        in_t = row["In_Temperature"]
        in_h = row["In_Humidity"]

        out_t = row["Out_Temperature"]
        out_h = row["Out_Humidity"]

        if (invalid):

            SB5100 = s1
            SP1100 = s2
            SP1901 = s3
            TGS2602 = s4
            TGS2620 = s5
            SP3100 = s6
            SP3SAQ201 = s7

        else:

            SB5100 = abs(row["SB-51-00"]-regresModels.predict_value(in_t,in_h,"SB-51-00"))
            SP1100 = abs(row["SP-11-00"]-regresModels.predict_value(in_t,in_h,"SP-11-00"))
            SP1901 = abs(row["SP-19-01"]-regresModels.predict_value(in_t,in_h,"SP-19-01"))
            TGS2602 = abs(row["TGS2602-B00"]-regresModels.predict_value(in_t,in_h,"TGS2602-B00"))
            TGS2620 = abs(row["TGS2620-C00"]-regresModels.predict_value(in_t,in_h,"TGS2620-C00"))
            SP3100 = abs(row["SP-31-00"]-regresModels.predict_value(in_t,in_h,"SP-31-00"))
            SP3SAQ201 = abs(row["SP3S-AQ2-01"]-regresModels.predict_value(in_t,in_h,"SP3S-AQ2-01"))

            df2=pd.DataFrame([[date, time, in_t, in_h, out_t, out_h, SB5100, SP1100, SP1901,

                TGS2602, TGS2620, SP3100, SP3SAQ201]], columns=columns_names)

            df_classifier=df_classifier.append(df2, ignore_index=True)

            s1 = SB5100
            s2 = SP1100
            s3 = SP1901
            s4 = TGS2602
            s5 = TGS2620
            s6 = SP3100
            s7 = SP3SAQ201

        df2=pd.DataFrame([[date, time, in_t, in_h, SB5100, SP1100, SP1901,

            TGS2602, TGS2620, SP3100, SP3SAQ201]], columns=columns_names)

        df_processed=df_processed.append(df2, ignore_index=True)

    df_processed.to_csv('../Data_processed_v2/processed.csv')
    #df_classifier.to_csv('Data_processed/processed_classifier_TEST.csv')


    return 0

    def main():

        mng = manageCSV_data()

        csv=pd.read_csv('./Data_processed/test.csv')
        print(csv)
        vals=mng.getRegression(csv)
        print(vals)
        new_row=mng.getLabel(vals)
        print(new_row)


        return 0


    if __name__ == "__main__":
        main()
