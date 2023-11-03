from common.config_param import config_dict

class MappingFilePath:
    
   def __init__(self,mls_name):
        self.property_file_path = config_dict['data'][mls_name]['mappingfile']+'\\'+mls_name+'_property.properties'
        self.feature_file_path = config_dict['data'][mls_name]['mappingfile']+'\\'+mls_name+'_feature.properties'
        self.media_file_path = config_dict['data'][mls_name]['mappingfile']+'\\'+mls_name+'_media.properties'
        self.user_file_path = config_dict['data'][mls_name]['mappingfile']+'\\'+mls_name+'_user.properties'
        
        
