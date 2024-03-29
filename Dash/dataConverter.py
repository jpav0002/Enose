import pandas as pd
import regressor
import datetime
import classifier

class manageCSV_data:

    def __init__(self):

        self.columns_names=['Date','Time','In_Temperature','In_Humidity','SB-51-00','SP-11-00','SP-19-01'
            ,'TGS2602-B00','TGS2620-C00','SP-31-00','SP3S-AQ2-01']

        self.clfModels= classifier.odor_classifier('./Data_processed/Models/classifier_v1.csv')

        self.regresModels = regressor.regressionModels('./Data_processed/Models/reg_data.csv', 2)

    def check_time(self,time):

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

    def getRegression(self, new_vals):

        df_processed = pd.read_csv('./Data_processed/processed_classifier_smartiago_v2.csv')
        lastrow = df_processed.tail(1)
        print(lastrow)

        s1 = (lastrow['SB-51-00'].values)[0]
        s2 = (lastrow['SP-11-00'].values)[0]
        s3 = (lastrow['SP-19-01'].values)[0]
        s4 = (lastrow['TGS2602-B00'].values)[0]
        s5 = (lastrow['TGS2620-C00'].values)[0]
        s6 = (lastrow['SP-31-00'].values)[0]
        s7 = (lastrow['SP3S-AQ2-01'].values)[0]

        df_lastVals = pd.DataFrame(columns=self.columns_names)

        for index,row in new_vals.iterrows():

            date = row['Date']
            time = row['Time']
            in_t = row['In_Temperature']
            in_h = row['In_Humidity']

            invalid=self.check_time(time)

            if (invalid):

                SB5100 = s1
                SP1100 = s2
                SP1901 = s3
                TGS2602 = s4
                TGS2620 = s5
                SP3100 = s6
                SP3SAQ201 = s7

            else:

                SB5100 = abs(row["SB-51-00"]-self.regresModels.predict_value(in_t,in_h,"SB-51-00"))
                SP1100 = abs(row["SP-11-00"]-self.regresModels.predict_value(in_t,in_h,"SP-11-00"))
                SP1901 = abs(row["SP-19-01"]-self.regresModels.predict_value(in_t,in_h,"SP-19-01"))
                TGS2602 = abs(row["TGS2602-B00"]-self.regresModels.predict_value(in_t,in_h,"TGS2602-B00"))
                TGS2620 = abs(row["TGS2620-C00"]-self.regresModels.predict_value(in_t,in_h,"TGS2620-C00"))
                SP3100 = abs(row["SP-31-00"]-self.regresModels.predict_value(in_t,in_h,"SP-31-00"))
                SP3SAQ201 = abs(row["SP3S-AQ2-01"]-self.regresModels.predict_value(in_t,in_h,"SP3S-AQ2-01"))

                s1 = SB5100
                s2 = SP1100
                s3 = SP1901
                s4 = TGS2602
                s5 = TGS2620
                s6 = SP3100
                s7 = SP3SAQ201


            df_temp=pd.DataFrame([[date, time, in_t, in_h, SB5100, SP1100, SP1901,

                TGS2602, TGS2620, SP3100, SP3SAQ201]], columns=self.columns_names)

            df_lastVals=df_lastVals.append(df_temp, ignore_index=True)

        return df_lastVals

    def getLabel(self, sensorData):

        # order for classifier SB-51-00,SP-11-00,SP-19-01,TGS2602-B00,TGS2620-C00,SP-31-00,SP3S-AQ2-01

        label=[]

        for index,row in sensorData.iterrows():

            classifier=[row["SB-51-00"],row["SP-11-00"],row["SP-19-01"],

                            row["TGS2620-C00"],row["SP-31-00"],

                                row["SP3S-AQ2-01"]]

            label_val=self.clfModels.predict_value(classifier)
            label.append(label_val)

        sensorData['Intensity']=label
        print(sensorData)

        return sensorData

    def checkNewVal(self,class_data,raw_data):

        raw=pd.read_csv(raw_data)
        labels=pd.read_csv(class_data)

        col_raw=len(raw)
        col_class=len(labels)

        new_vals=pd.DataFrame()

        if (col_raw != col_class):

            number_new_vals = col_raw-col_class
            new_rows=raw.tail(number_new_vals)
            reg_new=self.getRegression(new_rows)
            labels_new=self.getLabel(reg_new)
            labels=labels.append(labels_new, ignore_index=True)
            labels.to_csv(class_data)

        else:
            print("No hay valores nuevos")


def main():

    mng = manageCSV_data()

    csv=pd.read_csv('../smartiago_v2/Mean_data.csv')
    reg_new=mng.getRegression(csv)
    new_row=mng.getLabel(reg_new)
    new_row.to_csv('./Data_processed/processed_classifier_what.csv')

    return 0


if __name__ == "__main__":
    main()
