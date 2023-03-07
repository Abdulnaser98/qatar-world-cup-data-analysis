import pandas as pd


aljazerra_data = pd.read_csv("/Users/abdulnaser/Desktop/DHKatar/code_base/data_extraction/raw_data/aljazerra_data.csv",sep=';')
bbc_data = pd.read_csv("/Users/abdulnaser/Desktop/DHKatar/code_base/data_extraction/raw_data/all_bbc_qatar_data.csv")
guardian_data = pd.read_csv("/Users/abdulnaser/Desktop/DHKatar/code_base/data_extraction/raw_data/guardian.CSV",sep= ",",encoding='latin1')

# reset index and assign it as ID
aljazerra_data['ID'] = aljazerra_data.reset_index().index

bbc_data['ID'] = bbc_data.reset_index().index

guardian_data['ID'] = guardian_data.reset_index().index



aljazerra_data.to_csv("/Users/abdulnaser/Desktop/DHKatar/code_base/data_extraction/raw_data/aljazerra_data.csv")
bbc_data.to_csv("/Users/abdulnaser/Desktop/DHKatar/code_base/data_extraction/raw_data/all_bbc_qatar_data.csv")
guardian_data.to_csv("/Users/abdulnaser/Desktop/DHKatar/code_base/data_extraction/raw_data/guardian.CSV")