import pandas as pd
import regressor
import datetime
import classifier

class manageCSV_data:

    def __init__(self):

        self.columns_names=['Date','Time','In_Temperature','In_Humidity','SB-51-00','SP-11-00','SP-19-01'
            ,'TGS2602-B00','TGS2620-C00','SP-31-00','SP3S-AQ2-01']

        self.datareg = pd.read_csv('../Dash/Data_processed/Models/reg_data.csv')
        self.clfModels= classifier.odor_classifier('./models/classifier_v1.csv')

        self.regresModels = regressor.regressionModels(self.datareg,2)

    def check_time(self,time):

        hour,min,sec=time.split(":")

        hour = int(hour)
        min = int(min)
        sec = int(min)

        invalid=False

        if ((hour >= 10) and (hour <= 19)) or ((hour >= 14) and (hour < 20)):

            valid=True

        else:

            valid=False

        return valid

    def getRegression(self, new_vals):

        df_lastVals = pd.DataFrame(columns=self.columns_names)

        s1 = s2 = s2 = s3 = s4 = s5 = s6 = s7 = 0

        for index,row in new_vals.iterrows():

            date = row['Date']
            time = row['Time']
            in_t = row['Temperature']
            in_h = row['Humidity']

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

        return sensorData

def main():

    mng = manageCSV_data()

    csv=pd.read_csv('./regression/regression_v1_preprocessed.csv')
    new_row=mng.getLabel(csv)
    new_row.to_csv('./classifier_label_v1.csv')

    return 0


if __name__ == "__main__":
    main()
