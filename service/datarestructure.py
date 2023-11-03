import json
import os
from common.MyConvert import MyConvert
from models.samplemodel import lastReadFile, mlsType
from service.filestatus import FileReadStatus

class Mapping:
    property_mapping_flags = {}
    feature_mapping_flags = {}
    user_mapping_flags = {}
    media_mapping_flags = {}
    
    def __init__(self, data_path=None):
        #self.field_mapping_flags = {}
        self.data_path = data_path
        
    def prepare_mapping_object(self,properties_file,table_name):
        field_mapping_flags = {}
        #print("properties_file path",properties_file)
        if table_name == 'property':
            with open(properties_file, 'r') as f:
                for line in f:
                    if line.strip():
                        key, value, flag = line.strip().split("|")
                        key = key.strip()
                        value = value.strip()
                        flag = flag.strip()
                        field_mapping_flags[key] = {'value': value, 'flag': flag}
            Mapping.property_mapping_flags = field_mapping_flags
            
        if table_name == 'feature':
            with open(properties_file, 'r') as f:
                for line in f:
                    if line.strip():
                        key, value, flag = line.strip().split("|")
                        key = key.strip()
                        value = value.strip()
                        flag = flag.strip()
                        field_mapping_flags[key] = {'value': value, 'flag': flag}
            Mapping.feature_mapping_flags = field_mapping_flags
        
        if table_name == 'media':
            with open(properties_file, 'r') as f:
                for line in f:
                    if line.strip():
                        key, value, flag = line.strip().split("|")
                        key = key.strip()
                        value = value.strip()
                        flag = flag.strip()
                        field_mapping_flags[key] = {'value': value, 'flag': flag}
            Mapping.media_mapping_flags = field_mapping_flags
            
        if table_name == 'user':
            with open(properties_file, 'r') as f:
                for line in f:
                    if line.strip():
                        key, value, flag = line.strip().split("|")
                        key = key.strip()
                        value = value.strip()
                        flag = flag.strip()
                        field_mapping_flags[key] = {'value': value, 'flag': flag}
            Mapping.user_mapping_flags = field_mapping_flags
            
        
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
        
    def prepare_media_object(entry):
        media_section = {}
        media_data = {}
        bfcid = Mapping.create_bfcid(entry.get('ListingKey'))
        mls_number = entry.get('ListingKey')
        media_obj = entry.get('Media')
        i = 0
        if media_obj is not None:
            for obj in media_obj:
                for key, field_mapping in Mapping.media_mapping_flags.items():
                    file_key = field_mapping['value']
                    if '_' in file_key:
                        parts = file_key.split('_')
                        if len(parts) > 1:
                            file_key = parts[1]
                    field_value = obj.get(file_key)
                    
                            
                    if key == 'BFCID':
                        field_value = bfcid
                    if key == 'MLS_NUMBER':
                        field_value = mls_number
                               
                    media_section[key] = field_value if field_value is not None else None
                        # media_section['BFCID'] = bfcid
                        # media_section['MLS_NUMBER'] = mls_number
                        # media_section['PHOTO_TYPE'] = obj.get('MediaType')
                        # media_section['CAPTION'] = obj.get('LongDescription')
                        # media_section['URL'] = obj.get('MediaURL')
                        # media_section['PHOTOORDER'] = obj.get('Order')
                media_data[str(bfcid)+'_'+str(i)] = media_section
                i = i + 1
            return media_data
    
    def prepare_user_object(entry):
        user_section = {}
        user_data = {}
        bfcid = Mapping.create_bfcid(entry.get('ListingKey'))
        for key, field_mapping in Mapping.user_mapping_flags.items():
            field_value = entry.get(field_mapping['value'])
            if key == 'BFCID' and field_value is not None:
                field_value = bfcid
            elif key == 'OFFICE_NAME' and field_value is not None:
                field_value = '' + field_value + ''
            user_section[key] = field_value if field_value is not None else None
        user_data = user_section
        return user_data
        
    def prepare_property_object(entry):
        property_section = {}
        property_data = {}
        bfcid = Mapping.create_bfcid(entry.get('ListingKey'))
        for key, field_mapping in Mapping.property_mapping_flags.items():
            field_value = entry.get(field_mapping['value'])
            if key == 'BFCID' and field_value is not None:
                field_value = bfcid
                property_section[key] = field_value if field_value is not None else None
            elif key == 'MISC' and field_value is not None:  # Handle MISC field within PROPERTY section
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
        property_data = property_section
        return property_data
        
    def prepare_feature_object(entry):
       feature_section = {}
       feature_data = {}
       bfcid = Mapping.create_bfcid(entry.get('ListingKey'))
       for key, field_mapping in Mapping.feature_mapping_flags.items():
            field_value = entry.get(field_mapping['value'])
            if key == 'BFCID' and field_value is not None:
                field_value = bfcid
            elif key == 'NUMFLOORS':
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
            feature_section[key] = field_value if field_value is not None else None
       feature_data = feature_section
       return feature_data


    def restructure_data(self,data_path,file_list):
        
        #print("inside restructure data")
        dict_list = {}
        final_item = {}
        combined_property_data = {}
        combined_features_data = {}
        combined_user_data = {}
        combined_media_data = {}
        
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
               
               # to handle nested object 
                #mls_number = entry.get(Mapping.property_mapping_flags['BFCID']['value'])
                mls_number = Mapping.create_bfcid(entry.get(Mapping.property_mapping_flags['BFCID']['value']))
                if mls_number:
                   
                    property_section = {}
                    features_section = {}
                    user_section = {}
                    
                    media_section_separate = Mapping.prepare_media_object(entry)
                    property_section_separate = Mapping.prepare_property_object(entry)
                    feature_section_separate = Mapping.prepare_feature_object(entry)
                    user_section_separate = Mapping.prepare_user_object(entry)

                    # for key, field_mapping in Mapping.field_mapping_flags.items():
                    #     field_value = entry.get(field_mapping['value'])
                    #     if field_mapping['flag'] == 'P':
                    #         if key == 'MISC' and field_value is not None:  # Handle MISC field within PROPERTY section
                    #             misc_keys = [k.strip() for k in field_value.split(',')]
                    #             misc_values = [entry.get(k.strip()) for k in misc_keys]
                    #             #print(misc_values)
                    #             property_section[key] = '|'.join([f"{k}:{v}" for k, v in zip(misc_keys, misc_values) if v is not None])
                    #             #print(property_section)
                    #         elif key == 'DISPLAY_ADDRESS' or key == 'DISPLAY_LISTING':
                    #             property_section[key] = 2 if field_value is True else 0
                    #         elif key == 'ADDRESS':
                    #             StreetNumber = entry.get('StreetNumber')
                    #             StreetName = entry.get('StreetName')
                    #             StreetDirPrefix = entry.get('StreetDirPrefix')
                    #             StreetSuffix = entry.get('StreetSuffix')
                    #             StreetDirSuffix = entry.get('StreetDirSuffix')
                    #             values = [value for value in [StreetNumber, StreetName, StreetDirPrefix, StreetSuffix, StreetDirSuffix] if value is not None]
                    #             property_section[key] = ','.join(values)
                    #         else:
                    #             property_section[key] = field_value if field_value is not None else None
                                
                                
                    #     elif field_mapping['flag'] == 'M':
                    #         pass
                    #         #media_section[key] = field_value if field_value is not None else None
                            
                    #     elif field_mapping['flag'] == 'U':
                            
                    #         if key == 'OFFICE_NAME' and field_value is not None:
                    #             field_value = '' + field_value + ''
                                
                    #         user_section[key] = field_value if field_value is not None else None
                            
                    #     elif field_mapping['flag'] == 'F':
                    #         if key == 'NUMFLOORS':
                    #             StoriesTotaltmp = entry.get('StreetNumber')
                    #             StoriesTotal = str(StoriesTotaltmp) if StoriesTotaltmp is not None else None
                    #             Storiestmp = entry.get('Stories')
                    #             Stories = str(Storiestmp) if Storiestmp is not None else None
                    #             Levelstmp = entry.get('Levels')
                    #             Levels = str(Levelstmp) if Levelstmp is not None else None
                    #             values = [value for value in [StoriesTotal, Stories, Levels] if value is not None]
                    #             try:
                    #                 field_value = ','.join(values)
                    #             except Exception as e:
                    #                 print('Error in generating NUMFLOORS',e)
                    #         features_section[key] = field_value if field_value is not None else None
                            
                    #     elif field_mapping['flag'] == 'A':  # processing fields that are common for all tables
                    #         if key == 'BFCID' and field_value is not None:
                    #             #field_value = Mapping.create_bfcid(field_value) # creating BFCID
                    #             field_value = mls_number
                               
                    #         #media_section[key] = field_value if field_value is not None else None
                    #         features_section[key] = field_value if field_value is not None else None
                    #         property_section[key] = field_value if field_value is not None else None
                    #         user_section[key] = field_value if field_value is not None else None
                            
                    if property_section_separate:
                        #item['PROPERTY'] = property_section
                        combined_property_data[mls_number] = property_section_separate

                    if media_section_separate:
                        #item['MEDIA'] = media_section
                        #media_data[mls_number] = media_section
                        for key, value in media_section_separate.items():
                            if key in combined_media_data:
                                pass
                                #combined_media_data[key].append(value)
                            else:
                                combined_media_data[key] = value
                                
                        
                        #media_data.append(media_section_separate)

                    if feature_section_separate:
                        #item['FEATURES'] = features_section
                        combined_features_data[mls_number] = feature_section_separate
                        
                    if user_section_separate:
                        #item['FEATURES'] = features_section
                        combined_user_data[mls_number] = user_section_separate

                    #restructured_data[mls_number] = item
       
        
       
        final_item['PROPERTY_SECTION'] = combined_property_data
        final_item['MEDIA_SECTION'] = combined_media_data
        final_item['FEATURES_SECTION'] = combined_features_data
        final_item['USER_SECTION'] = combined_user_data
        
        # inserting last read file 
        
        return final_item
