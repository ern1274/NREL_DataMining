import unittest
import NREL_DataMining.src.Data_Preprocess as Organizer
import pandas as pd


class MyTestCase(unittest.TestCase):
    def test_assign_temp_bucket(self):
        self.assertEqual(Organizer.assign_temp_bucket('20.0'), '<=20.0')
        self.assertEqual(Organizer.assign_temp_bucket('0.0'), '<=20.0')
        self.assertEqual(Organizer.assign_temp_bucket('19.9'), '<=20.0')
        self.assertEqual(Organizer.assign_temp_bucket('10.0'), '<=20.0')

        self.assertEqual(Organizer.assign_temp_bucket('20.1'), '<=37.0')
        self.assertEqual(Organizer.assign_temp_bucket('27.0'), '<=37.0')
        self.assertEqual(Organizer.assign_temp_bucket('37.0'), '<=37.0')
        self.assertEqual(Organizer.assign_temp_bucket('36.9'), '<=37.0')

        self.assertEqual(Organizer.assign_temp_bucket('37.1'), '<=70.0')
        self.assertEqual(Organizer.assign_temp_bucket('45.8'), '<=70.0')
        self.assertEqual(Organizer.assign_temp_bucket('70.0'), '<=70.0')
        self.assertEqual(Organizer.assign_temp_bucket('69.9'), '<=70.0')

        self.assertEqual(Organizer.assign_temp_bucket('70.1'), '<=100.0')
        self.assertEqual(Organizer.assign_temp_bucket('84.9'), '<=100.0')
        self.assertEqual(Organizer.assign_temp_bucket('100.0'), '<=100.0')
        self.assertEqual(Organizer.assign_temp_bucket('99.9'), '<=100.0')

        self.assertEqual(Organizer.assign_temp_bucket('100.1'), '>100')
        self.assertEqual(Organizer.assign_temp_bucket('110.2'), '>100')
    def test_assign_wind_bucket(self):
        self.assertEqual(Organizer.assign_wind_bucket('1.5'), 'Calm - Gentle Breeze')
        self.assertEqual(Organizer.assign_wind_bucket('0.0'), 'Calm - Gentle Breeze')
        self.assertEqual(Organizer.assign_wind_bucket('2.4'), 'Calm - Gentle Breeze')
        self.assertEqual(Organizer.assign_wind_bucket('3.9'), 'Calm - Gentle Breeze')

        self.assertEqual(Organizer.assign_wind_bucket('4.0'), 'Moderate - Strong Breeze')
        self.assertEqual(Organizer.assign_wind_bucket('4.9'), 'Moderate - Strong Breeze')
        self.assertEqual(Organizer.assign_wind_bucket('5.7'), 'Moderate - Strong Breeze')
        self.assertEqual(Organizer.assign_wind_bucket('6.9'), 'Moderate - Strong Breeze')

        self.assertEqual(Organizer.assign_wind_bucket('7.0'), 'Near - Severe Gale')
        self.assertEqual(Organizer.assign_wind_bucket('7.8'), 'Near - Severe Gale')
        self.assertEqual(Organizer.assign_wind_bucket('8.7'), 'Near - Severe Gale')
        self.assertEqual(Organizer.assign_wind_bucket('9.9'), 'Near - Severe Gale')

        self.assertEqual(Organizer.assign_wind_bucket('12.4'), 'Storm - Hurricane Forces')
        self.assertEqual(Organizer.assign_wind_bucket('10.0'), 'Storm - Hurricane Forces')
        self.assertEqual(Organizer.assign_wind_bucket('12.9'), 'Storm - Hurricane Forces')
        self.assertEqual(Organizer.assign_wind_bucket('13'), 'Storm - Hurricane Forces')

        self.assertEqual(Organizer.assign_wind_bucket('13.1'), 'Beyond Hurricane Forces')
        self.assertEqual(Organizer.assign_wind_bucket('200.0'), 'Beyond Hurricane Forces')
    def test_bucket_data(self):
        self.assertEqual(Organizer.bucket_data('Month', '0'), '0')
        self.assertEqual(Organizer.bucket_data('Month','5'), '5')

        self.assertEqual(Organizer.bucket_data('Year','2017'), '2017')
        self.assertEqual(Organizer.bucket_data('Year','2030'), '2030')


        self.assertEqual(Organizer.bucket_data('Temperature','19.9'), '<=20.0')
        self.assertEqual(Organizer.bucket_data('Temperature','36.9'), '<=37.0')
        self.assertEqual(Organizer.bucket_data('Temperature','69.9'), '<=70.0')
        self.assertEqual(Organizer.bucket_data('Temperature','99.9'), '<=100.0')
        self.assertEqual(Organizer.bucket_data('Temperature', '100.1'), '>100')

        self.assertEqual(Organizer.bucket_data('Wind Speed','3.9'), 'Calm - Gentle Breeze')
        self.assertEqual(Organizer.bucket_data('Wind Speed','6.9'), 'Moderate - Strong Breeze')
        self.assertEqual(Organizer.bucket_data('Wind Speed','9.9'), 'Near - Severe Gale')
        self.assertEqual(Organizer.bucket_data('Wind Speed','13'), 'Storm - Hurricane Forces')
        self.assertEqual(Organizer.bucket_data('Wind Speed', '13.1'), 'Beyond Hurricane Forces')

        self.assertEqual(Organizer.bucket_data('Mock Attribute','13.1'), '13.1')
        self.assertEqual(Organizer.bucket_data('Mock Attribute', '200.0'), '200.0')

    def test_organize_by_month(self):
        attribute = 'Month'
        test_df = {'US': {'California': pd.DataFrame({attribute:['1','2','3']})}}
        actual_df = {'ALL': {'1':[pd.Series(data=['1'],index=[attribute],dtype=object)], '2': [pd.Series(data=['2'],index=[attribute],dtype=object)], '3':[pd.Series(data=['3'],index=[attribute],dtype=object)]}, 'US': {'California': {'1':[pd.Series(data=['1'],index=[attribute],dtype=object)], '2': [pd.Series(data=['2'],index=[attribute],dtype=object)], '3':[pd.Series(data=['3'],index=[attribute],dtype=object)]}}}
        result_df = Organizer.organize_by_month(test_df)
        #Testing on US
        actual_all = actual_df['ALL']
        result_all = result_df['ALL']
        actual_us_cali = actual_df['US']['California']
        result_us_cali = result_df['US']['California']
        for key in actual_all.keys():
            actual_entry = actual_all[key]
            result_entry = result_all[key]
            for i in range(len(actual_entry)):
                self.assertTrue(actual_entry[i].equals(result_entry[i]))
        for i in range(1,len(actual_us_cali)+1):
            index = str(i)
            actual_entry = actual_us_cali[index]
            result_entry = result_us_cali[index]
            for h in range(len(actual_entry)):
                self.assertTrue(actual_entry[h].equals(result_entry[h]))

    def test_organize_by_year(self):
        attribute = 'Year'
        test_df = {'US': {'California': pd.DataFrame({attribute: ['1', '2', '3']})}}
        actual_df = {'ALL': {'1': [pd.Series(data=['1'], index=[attribute], dtype=object)],
                             '2': [pd.Series(data=['2'], index=[attribute], dtype=object)],
                             '3': [pd.Series(data=['3'], index=[attribute], dtype=object)]}, 'US': {
            'California': {'1': [pd.Series(data=['1'], index=[attribute], dtype=object)],
                           '2': [pd.Series(data=['2'], index=[attribute], dtype=object)],
                           '3': [pd.Series(data=['3'], index=[attribute], dtype=object)]}}}
        result_df = Organizer.organize_by_year(test_df)
        # Testing on US
        actual_all = actual_df['ALL']
        result_all = result_df['ALL']
        actual_us_cali = actual_df['US']['California']
        result_us_cali = result_df['US']['California']
        for key in actual_all.keys():
            actual_entry = actual_all[key]
            result_entry = result_all[key]
            for i in range(len(actual_entry)):
                self.assertTrue(actual_entry[i].equals(result_entry[i]))
        for i in range(1,len(actual_us_cali)+1):
            index = str(i)
            actual_entry = actual_us_cali[index]
            result_entry = result_us_cali[index]
            for h in range(len(actual_entry)):
                self.assertTrue(actual_entry[h].equals(result_entry[h]))

    def test_organize_by_wind_speed(self):
        attribute = 'Wind Speed'
        test_df = {'US': {'California': pd.DataFrame({attribute: ['3.9', '6.9', '9.9']})}}
        actual_df = {'ALL': {'Calm - Gentle Breeze': [pd.Series(data=['3.9'], index=[attribute], dtype=object)],
                             'Moderate - Strong Breeze': [pd.Series(data=['6.9'], index=[attribute], dtype=object)],
                             'Near - Severe Gale': [pd.Series(data=['9.9'], index=[attribute], dtype=object)]}, 'US': {
            'California': {'Calm - Gentle Breeze': [pd.Series(data=['3.9'], index=[attribute], dtype=object)],
                             'Moderate - Strong Breeze': [pd.Series(data=['6.9'], index=[attribute], dtype=object)],
                             'Near - Severe Gale': [pd.Series(data=['9.9'], index=[attribute], dtype=object)]}}}
        result_df = Organizer.organize_by_wind_speed(test_df)
        actual_all = actual_df['ALL']
        result_all = result_df['ALL']
        actual_us_cali = actual_df['US']['California']
        result_us_cali = result_df['US']['California']
        for key in actual_all.keys():
            actual_entry = actual_all[key]
            result_entry = result_all[key]
            for i in range(len(actual_entry)):
                self.assertTrue(actual_entry[i].equals(result_entry[i]))
        for index in actual_us_cali:
            actual_entry = actual_us_cali[index]
            result_entry = result_us_cali[index]
            for h in range(len(actual_entry)):
                self.assertTrue(actual_entry[h].equals(result_entry[h]))

    def test_organize_by_temperature(self):
        attribute = 'Temperature'
        test_df = {'US': {'California': pd.DataFrame({'Temperature': ['19.9', '36.9', '69.9']})}}
        actual_df = {'ALL': {'<=20.0': [pd.Series(data=['19.9'], index=[attribute], dtype=object)],
                             '<=37.0': [pd.Series(data=['36.9'], index=[attribute], dtype=object)],
                             '<=70.0': [pd.Series(data=['69.9'], index=[attribute], dtype=object)]}, 'US': {
            'California': {'<=20.0': [pd.Series(data=['19.9'], index=[attribute], dtype=object)],
                             '<=37.0': [pd.Series(data=['36.9'], index=[attribute], dtype=object)],
                             '<=70.0': [pd.Series(data=['69.9'], index=[attribute], dtype=object)]}}}
        result_df = Organizer.organize_by_temperature(test_df)
        actual_all = actual_df['ALL']
        result_all = result_df['ALL']
        actual_us_cali = actual_df['US']['California']
        result_us_cali = result_df['US']['California']
        for key in actual_all.keys():
            actual_entry = actual_all[key]
            result_entry = result_all[key]
            for i in range(len(actual_entry)):
                self.assertTrue(actual_entry[i].equals(result_entry[i]))
        for index in actual_us_cali:
            actual_entry = actual_us_cali[index]
            result_entry = result_us_cali[index]
            for h in range(len(actual_entry)):
                self.assertTrue(actual_entry[h].equals(result_entry[h]))
if __name__ == '__main__':
    unittest.main()
