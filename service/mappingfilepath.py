from common.config_param import config_dict
from service.datarestructure import Mapping
from service.dataservice import *

class MappingFilePath:
   property_file_path = ''
   feature_file_path = ''
   media_file_path = ''
   user_file_path = ''
   data_folder = ''
    
   def __init__(self,mls_name):
        MappingFilePath.property_file_path = config_dict['data'][mls_name]['mappingfile']+'\\'+mls_name+'_property.properties'
        MappingFilePath.feature_file_path = config_dict['data'][mls_name]['mappingfile']+'\\'+mls_name+'_feature.properties'
        MappingFilePath.media_file_path = config_dict['data'][mls_name]['mappingfile']+'\\'+mls_name+'_media.properties'
        MappingFilePath.user_file_path = config_dict['data'][mls_name]['mappingfile']+'\\'+mls_name+'_user.properties'
        MappingFilePath.openhouse_file_path = config_dict['data'][mls_name]['mappingfile']+'\\'+mls_name+'_openhouse.properties'
        MappingFilePath.data_folder = config_dict['data'][mls_name]['datapath']
        
   def createMappingObject(self):
        mappinginstance = Mapping()
        mappinginstance.prepare_mapping_object(MappingFilePath.property_file_path,'property')
        mappinginstance.prepare_mapping_object(MappingFilePath.feature_file_path,'feature')
        mappinginstance.prepare_mapping_object(MappingFilePath.media_file_path,'media')
        mappinginstance.prepare_mapping_object(MappingFilePath.user_file_path,'user')
        mappinginstance.prepare_mapping_object(MappingFilePath.openhouse_file_path,'openhouse')
        
        
