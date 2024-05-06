import os
import time
import threading
import json

from AWSInteraction.S3Handler import S3ExtractionHandler
from extractors.custom_extractors.custom_extractos import custom_extractors

# TODO: 
# - documentare


class ThreadedFunction(threading.Thread):
    """
    Create a thread to run a function in parallel with other threads.
    """
    def __init__(self, function, scope):
        threading.Thread.__init__(self)
        self.function = function
        self.scope = scope
        self.result = None
        self.total_runtime= None

    def download_file(self, file_key):
        s3handler = S3ExtractionHandler(file_key)
     
        file = s3handler.download(file_key)
        if file['statusCode'] == 200:
            return file['body']
        else:
            print("File {} not found".format(file_key))
            return None
        
    def download_files_from_dir(self, folder_key):
        local_file_list = []
        s3handler = S3ExtractionHandler(folder_key)
        files_list = s3handler.list_files()
        if files_list['statusCode'] != 200:
            return None
        for file in files_list['body']:
            file_path = self.download_file(file)
            if file_path is not None:
                local_file_list.append(file_path)
        return local_file_list
                
    def run(self):
        # time counter
        start_time = time.time()
        if self.scope.get("type").lower() == "directory":
            # get list of files
            local_files_path = self.download_files_from_dir(self.scope["key"])
        else:
            local_files_path = self.download_file(self.scope["key"])
        
        # Execute extraction
        if local_files_path is None or len(local_files_path) == 0:
            self.result = {'error': 'file not found'}
        else:
            extractor = self.function(local_files_path)
            self.result = extractor.process()
        self.total_runtime = time.time() - start_time



class ExtractionHandler:
    """Handles the extraction of data from listo of files or folders located in S3.

    Returns:
        json: extracted data in sjon format
    """

    def __init__(self, request_context) -> None:
        self.request_context = request_context
        self.tenant = request_context.payload['TENANT']
        self.extractor_type = request_context.payload['extractor_type']
        self.extactor = custom_extractors[self.tenant][self.extractor_type]
        self.extractions = {}
        self.local_saved_files = {} 

    def _delete_local_files(self):
        """ 
        Delete all the files that have been downloaded locally.
        """
        for file in self.local_saved_files.values():
            try:
                os.remove(file)
            except Exception as error:
                print("Could not delete file{} for error:{}".format(file, repr(error)))
                continue


    def run(self):

        files_list = self.request_context.payload['files']
        print("working_files:", files_list)
        threads = {}
        for file_key in files_list:
            thread = ThreadedFunction(self.extactor, file_key)
            threads[file_key["key"]] = thread
            thread.start()
        
        for _, thread in threads.items():
            thread.join()
        
        for file_key, thread in threads.items():
            dict_result = thread.result
            dict_result['extraction_time'] = thread.total_runtime
            self.extractions[file_key] = json.dumps(dict_result,indent=4, ensure_ascii=False)

        self._delete_local_files()

        return self.extractions

