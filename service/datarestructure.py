import json
import os
from common.MyConvert import MyConvert
from models.samplemodel import lastReadFile, mlsType
from service.filestatus import FileReadStatus

class Mapping:
    def __init__(self, data_path=None):
        #self.field_mapping_flags = {}
        self.data_path = data_path
        
    def prepare_mapping_object(self,properties_file):
        field_mapping_flags = {}
        #print("properties_file path",properties_file)
        with open(properties_file, 'r') as f:
            for line in f:
                if line.strip():
                    key, value, flag = line.strip().split("|")
                    key = key.strip()
                    value = value.strip()
                    flag = flag.strip()
                    field_mapping_flags[key] = {'value': value, 'flag': flag}
        return field_mapping_flags
        
        
    def create_bfcid(field_value):
        numeric_parts = [str(MyConvert.alphabetic_to_number(char)) for char in field_value]
        numeric_value = int("".join(numeric_parts))
        return numeric_value
    
    def insert_lastread_file(file_name, mls_name, file_timestamp):
        lastreadfile = lastReadFile()
        lastreadfile.mls_name = mls_name
        lastreadfile.file_name = file_name
        lastreadfile.file_timestamp = file_timestamp
        
        filereadstatusinstance = FileReadStatus()
        filereadstatusinstance.insertLastReadFile(MyConvert.to_dict(lastreadfile))

    def restructure_data(self,data_path,file_list,mls_name,field_mapping_flags):
        
        #print("inside restructure data")
        final_item = {}
        property_data = {}
        media_data = {}
        features_data = {}
        user_data = {}
        
        for file_name in file_list:
            filetoopen = data_path+'\\'+file_name
            print('Proccesing File :',file_name)
            try:
                with open(filetoopen, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except FileNotFoundError:
                print("The file does not exist.")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                data = {}  # Assign an empty dictionary or another default value
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                data = {}  # Assign an empty dictionary or another default value
            restructured_data = {}

            for entry in data['value']:
                #print("entry",entry)
                #print("mls number",self.field_mapping_flags['ID']['value'])
                mls_number = entry.get(field_mapping_flags['BFCID']['value'])
                mls_number = Mapping.create_bfcid(entry.get(field_mapping_flags['BFCID']['value']))
                if mls_number:
                    item = {}
                    property_section = {}
                    media_section = {}
                    features_section = {}
                    media_section = {}
                    user_section = {}

                    for key, field_mapping in field_mapping_flags.items():
                        field_value = entry.get(field_mapping['value'])
                        if field_mapping['flag'] == 'P':
                            if key == 'MISC' and field_value is not None:  # Handle MISC field within PROPERTY section
                                misc_keys = [k.strip() for k in field_value.split(',')]
                                misc_values = [entry.get(k.strip()) for k in misc_keys]
                                #print(misc_values)
                                property_section[key] = '|'.join([f"{k}:{v}" for k, v in zip(misc_keys, misc_values) if v is not None])
                                #print(property_section)
                            elif key == 'DISPLAY_ADDRESS' or key == 'DISPLAY_LISTING':
                                property_section[key] = 2 if field_value is True else 0
                            elif key == 'ADDRESS':
                                StreetNumber = entry.get('StreetNumber')
                                StreetName = entry.get('StreetName')
                                StreetDirPrefix = entry.get('StreetDirPrefix')
                                StreetSuffix = entry.get('StreetSuffix')
                                StreetDirSuffix = entry.get('StreetDirSuffix')
                                values = [value for value in [StreetNumber, StreetName, StreetDirPrefix, StreetSuffix, StreetDirSuffix] if value is not None]
                                property_section[key] = ','.join(values)
                            else:
                                property_section[key] = field_value if field_value is not None else None
                                
                                
                        elif field_mapping['flag'] == 'M':
                            media_section[key] = field_value if field_value is not None else None
                            
                        elif field_mapping['flag'] == 'U':
                            
                            if key == 'OFFICE_NAME' and field_value is not None:
                                field_value = '' + field_value + ''
                                
                            user_section[key] = field_value if field_value is not None else None
                            
                        elif field_mapping['flag'] == 'F':
                            if key == 'NUMFLOORS':
                                StoriesTotaltmp = entry.get('StreetNumber')
                                StoriesTotal = str(StoriesTotaltmp) if StoriesTotaltmp is not None else None
                                Storiestmp = entry.get('Stories')
                                Stories = str(Storiestmp) if Storiestmp is not None else None
                                Levelstmp = entry.get('Levels')
                                Levels = str(Levelstmp) if Levelstmp is not None else None
                                values = [value for value in [StoriesTotal, Stories, Levels] if value is not None]
                                try:
                                    field_value = ','.join(values)
                                except Exception as e:
                                    print('Error in generating NUMFLOORS',e)
                            features_section[key] = field_value if field_value is not None else None
                            
                        elif field_mapping['flag'] == 'A':  # processing fields that are common for all tables
                            if key == 'BFCID' and field_value is not None:
                                #field_value = Mapping.create_bfcid(field_value) # creating BFCID
                                field_value = mls_number
                               
                            media_section[key] = field_value if field_value is not None else None
                            features_section[key] = field_value if field_value is not None else None
                            property_section[key] = field_value if field_value is not None else None
                            user_section[key] = field_value if field_value is not None else None
                    if property_section:
                        #item['PROPERTY'] = property_section
                        property_data[mls_number] = property_section

                    if media_section:
                        #item['MEDIA'] = media_section
                        media_data[mls_number] = media_section

                    if features_section:
                        #item['FEATURES'] = features_section
                        features_data[mls_number] = features_section
                        
                    if user_section:
                        #item['FEATURES'] = features_section
                        user_data[mls_number] = user_section

                    #restructured_data[mls_number] = item
       
        final_item['PROPERTY_SECTION'] = property_data
        final_item['MEDIA_SECTION'] = media_data
        final_item['FEATURES_SECTION'] = features_data
        final_item['USER_SECTION'] = user_data
        
        # inserting last read file 
        
        return final_item