# import libraries
import pandas as pd
from tqdm import tqdm
import spacy
import nlp
import matplotlib.pyplot as plt


#nlp = spacy.load('en_core_web_sm')




def extract_NER_entities(data):
    nlp = spacy.load('en_core_web_sm')
    named_entities = []
    for content in tqdm(data["main_content"]):
        temp_entity_name = ''
        temp_named_entity = None
        content = nlp(content)
        for word in content:
            term = word.text
            tag = word.ent_type_
            if tag:
                temp_entity_name = ' '.join([temp_entity_name, term]).strip()
                temp_named_entity = (temp_entity_name, tag)
            else:
                if temp_named_entity:
                    named_entities.append(temp_named_entity)
                    temp_entity_name = ''
                    temp_named_entity = None

    entity_frame = pd.DataFrame(named_entities,
                            columns=['Entity Name', 'Entity Type'])
    return entity_frame



def get_top_20_entities(data,not_to_obosrve_entity_types,not_to_obsorve_entites,entity_types_to_change):

    data_entities = extract_NER_entities(data)
    # get the top named entities
    top_entities = (data_entities.groupby(by=['Entity Name', 'Entity Type'])
                           .size()
                           .sort_values(ascending=False)
                           .reset_index().rename(columns={0 : 'Frequency'}))

    # Create a Boolean mask based on column A
    mask = ~top_entities['Entity Type'].isin(not_to_obosrve_entity_types)

    # Filter the DataFrame using the Boolean mask
    filtered_df = top_entities[mask]

    filtered_df = filtered_df[~filtered_df['Entity Name'].isin(not_to_obsorve_entites)]
    filtered_df.loc[filtered_df['Entity Name'] == 'bbc', 'Entity Type'] = 'media outlet'
    for key, value in entity_types_to_change.items():
        filtered_df.loc[filtered_df['Entity Name'] == key, 'Entity Type'] = value

    return filtered_df.head(20)





def main_NER(path_to_cleaned_data_folder,path_to_evaluation_folder):

    print("Start extracting named entities: ")

    # read the three cleaned data sources
    aljazerra_cleaned_data = pd.read_csv( path_to_cleaned_data_folder + "aljazerra_cleaned_data.csv")
    bbc_cleaned_data = pd.read_csv( path_to_cleaned_data_folder + "bbc_cleaned_data.csv")
    guardian_cleaned_data = pd.read_csv( path_to_cleaned_data_folder +  "guardian_cleaned_data.csv")



    # Aljazerra
    aljazerra_not_to_obosrve_entity_types = ['ORDINAL', 'GPE', 'CARDINAL','DATE','NORP','LOC','TIME']
    aljazerra_not_to_obsorve_entites =  ['al jazeera','messi','al','harry kane','pele','hassan al','metro','alvarez','robert lewandowski',
                                         'english','hakim ziyech','louis van gaal','english','luka modric','neymar','tunisia','luis suarez',
                                         'didi dramani','kevin de bruyne','messi argentina']
    aljazerra_entity_types_to_change = {'bbc': 'media outlet','al bayt stadium':'Stadium','al thumama':'Stadium'}
    aljazerra_NER =  get_top_20_entities(aljazerra_cleaned_data,aljazerra_not_to_obosrve_entity_types,aljazerra_not_to_obsorve_entites,aljazerra_entity_types_to_change)
    aljazerra_NER.to_csv(path_to_evaluation_folder + "aljazerra/NER" + "/aljazerra_NER.csv")

   # BBC
    bbc_not_to_obsorve_entity_types = ['ORDINAL', 'GPE', 'CARDINAL','DATE','NORP','LOC','TIME']
    bbc_not_to_obsorve_entites = ['bbc','metro','harry kane','al','english'
                                  'didi dramani','kevin de bruyne','messi argentina']
    bbc_entity_types_to_change = {'al jazeera': 'media outlet','itv':'media outlet','eastofenglandnews bbc':'media outlet','bbc sport':'media outlet','bbc news':'media outlet'}
    bbc_NER = get_top_20_entities(bbc_cleaned_data,bbc_not_to_obsorve_entity_types,bbc_not_to_obsorve_entites,bbc_entity_types_to_change)
    bbc_NER.to_csv(path_to_evaluation_folder + "bbc/NER" + "/bbc_NER.csv")



    # The gaurdian
    guardian_not_to_obsorve_entity_types = ['ORDINAL', 'GPE', 'CARDINAL','DATE','NORP','LOC','TIME']
    guardian_not_to_obsorve_entites =      ['harry kane','messi','english', 'luis enrique', 'kane', 'bin','garcia',
                                            'louis van gaal','bukayo saka','hassan al','al','congress','mohamed bin',
                                            'warner','graham arnold','robert lewandowski','tim' ,'johnson','metro',
                                            'jordan henderson','harry maguire','su rez','john stones','xhaka','david',
                                            'euro','lvarez','michel platini','jude bellingham','six yards','ref','un',
                                            'gregg','williams','sepp blatter','van gaal','vin cius','kevin de bruyne',
                                            'manchester united','hugo lloris','virgil van dijk','lien tchouam','paul'
                                            ,'jordan pickford','lloris','tunisia','luke shaw','zinedine zidane','jack grealish'
                                            ,'james maddison','juventus','kyle','harry souttar','kim','matt','lee','joe allen'
                                            ,'https','luka modric','putin','aaron ramsey','liverpool','kuol','al thani'
                                            ,'de jong','weghorst','messi argentina','mar']

    guardian_entity_types_to_change = {'al jazeera': 'media outlet','itv':'media outlet','bbc':'media outlet','fox':'media outlet','al bayt stadium':'Stadium','al thumama':'Stadium'}
    guardian_NER = get_top_20_entities(guardian_cleaned_data,guardian_not_to_obsorve_entity_types,guardian_not_to_obsorve_entites,guardian_entity_types_to_change)
    guardian_NER.to_csv(path_to_evaluation_folder + "guardian/NER" + "/guardian_NER.csv")

    print("finished extracting entities: ")




