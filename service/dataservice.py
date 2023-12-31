from datetime import datetime
import time
from models.samplemodel import *
from common.rdb_dal.sql import Sql
from configs import sql_query
from common.MyConvert import *
from common.config_param import config_dict
from service.filestatus import *
from service.datarestructure import *
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from service.mappingfilepath import *
from service.mappingfilepath import MappingFilePath
from common.logs.log import *



class DataService:
    data_folder = ''
    field_mapping_flags = ''
    
    def get(searchModel:searchModel())->list[SampleModel]:
        sql = Sql('default')
        return sql.execute_list(SampleModel,sql_query.property_get_by_id_query, MyConvert.to_dict(searchModel))
    
    
    def insert(SampleModel:SampleModel()):
        sql = Sql('default')
        return sql.execute(sql_query.propert_insert_query, MyConvert.to_dict(SampleModel))
    
    
    def insertData(mymlsType:mlsType()):
        sql = Sql('default')
        
        process_start_time = time.time()
        
        filereadstatusinstance = FileReadStatus()
        last_processed_file_timestamp = filereadstatusinstance.getLastReadFile(mymlsType)
        
        if last_processed_file_timestamp is None:
            file_timestamp = datetime(2000, 1, 1, 0, 0, 0)
            last_processed_file_timestamp = file_timestamp
        else:
            last_processed_file_timestamp = last_processed_file_timestamp[0]['file_timestamp']
        
        
        DataService.data_folder = config_dict['data'][mymlsType.mls_name]['datapath']
        
        # Find correct path of each property file and calling function to create mapping object
        mapping_file_instance = MappingFilePath(mymlsType.mls_name)
        mapping_file_instance.createMappingObject()
        
        new_file_list = []
        new_file_list_timestamp = []
        file_list = os.listdir(DataService.data_folder)
        for file in file_list:
            file_path = os.path.join(DataService.data_folder, file)
            if int(os.path.getmtime(file_path)) > int(last_processed_file_timestamp.timestamp()):
                new_file_list.append(file)
                new_file_list_timestamp.append(os.path.getmtime(file_path))
                
        #file_list.sort(key=lambda x: os.path.getmtime(os.path.join(DataService.data_folder, x)))
        #new_file_list = [file for file in file_list if file > last_processed_file]
        #new_file_list = [file for file in file_list if last_processed_file_timestamp is None or (file is not None and file > last_processed_file_timestamp)]
        #new_file_list = file_list
        print("File List for Processing ::",new_file_list)
        
        batch_docs = [new_file_list[index : index+2] for index in range(0,len(new_file_list),2)]
        time_docs = [new_file_list_timestamp[index : index+2] for index in range(0,len(new_file_list_timestamp),2)]
        thread_count = [i + 1 for i in range(len(batch_docs))]
        datastatsforlog = dataStatsModel()
        
        with ThreadPoolExecutor(3) as executor:
           #print('batch_docs::::',batch_docs)
           #print('time_docs::::',time_docs)
           result =  list(executor.map(DataService.processandinsert,batch_docs,(mymlsType.mls_name,)* len(batch_docs),time_docs,thread_count))
           print(result)
           for rs in result:
                datastatsforlog.totalRecordsProcessed = datastatsforlog.totalRecordsProcessed + rs.totalRecordsProcessed
                datastatsforlog.totalMissingLatLongRecords = datastatsforlog.totalMissingLatLongRecords + rs.totalMissingLatLongRecords
                datastatsforlog.totalErrorRecords = datastatsforlog.totalErrorRecords + rs.totalErrorRecords
        
        process_end_time = time.time()
        log = Log()
        print(f"Total DB Insertion Took : {process_end_time - process_start_time} seconds")
        log.write(f"Total DB Insertion Took : {process_end_time - process_start_time} seconds")
        log.write(f"Total Records Processed : {datastatsforlog.totalRecordsProcessed}")
        log.write(f"Total Records With Missing Coordinates : {datastatsforlog.totalMissingLatLongRecords}")
        log.write(f"Total Records With Error : {datastatsforlog.totalErrorRecords}")
        log.write(f"==================================================={'==='}")
        
        return result
        
    def processandinsert(new_file_list,mls_name,time_docs, thread_count):
        print('Batch File Process and Insert Start for Thread : ', thread_count)
        #print('new_file_list::::',new_file_list)
        sql = Sql('default')
        mappinginstance = Mapping(DataService.data_folder)
        data_to_insert = mappinginstance.restructure_data(DataService.data_folder,new_file_list)
        property_data = list(data_to_insert['PROPERTY_SECTION'].values())
        feature_data = list(data_to_insert['FEATURES_SECTION'].values())
        media_data = list(data_to_insert['MEDIA_SECTION'].values())
        user_data = list(data_to_insert['USER_SECTION'].values())
        openhouse_data = list(data_to_insert['OPENHOUSE_SECTION'].values())
        bfcid_array = (list(data_to_insert['PROPERTY_SECTION'].keys()),)
        
        datastats = dataStatsModel()
        datastats.totalRecordsProcessed = len(bfcid_array[0])
        datastats.totalMissingLatLongRecords = data_to_insert['MISSING_LATLON']
        datastats.totalErrorRecords = data_to_insert['ERROR_DATA']
        
        connecton_obj = sql.open_connection()
        try:
            sql.start_transaction(connecton_obj)
            # deleting entry from all table
            sql.execute(connecton_obj,sql_query.bcfid_delete_query, bfcid_array)
            
            # Inserting into property table
            sql.execute_batch(connecton_obj,sql_query.property_insert_query, property_data)
            
            # Inserting into feature table
            sql.execute_batch(connecton_obj,sql_query.feature_insert_query, feature_data)
            
            # Inserting into media table
            sql.execute_batch(connecton_obj,sql_query.media_insert_query, media_data)
            
            # Inserting into user table
            sql.execute_batch(connecton_obj,sql_query.user_insert_query, user_data)
            
            # Inserting into openhouse table
            sql.execute_batch(connecton_obj,sql_query.openhouse_insert_query, openhouse_data)
            
            if len(time_docs) > 0:
                sorted_timestamps = sorted(time_docs, reverse=True)
                latest_timestamp = sorted_timestamps[0]
                latest_timestamp = datetime.fromtimestamp(latest_timestamp)
                formatted_time = latest_timestamp.strftime('%Y-%m-%d %H:%M:%S')
                lastreadfile = lastReadFile()
                lastreadfile.mls_name = mls_name
                lastreadfile.file_name = new_file_list[-1]
                lastreadfile.file_timestamp = formatted_time
                filereadstatusinstance = FileReadStatus()
                filereadstatusinstance.insertLastReadFile(connecton_obj,MyConvert.to_dict(lastreadfile))
            
            sql.commit_transaction(connecton_obj)
        except Exception as e:
            sql.rollback_transaction(connecton_obj)
            print(f"Error: {e}")
        finally:
            sql.close_connection(connecton_obj)
        
        return datastats
            
        
