from Video.domain.entities import ImageInfo, RecordInfo
from tinydb import TinyDB, Query
from Video.ports.db_link import DbLink

class TinyDbLink(DbLink):
    def __init__(self, db_name:str) -> None:
        self.db = TinyDB(db_name)
        self.doc_id = None
        
    def create(self, name:str) -> bool:
        if not self.session_exists(name=name):
            self.doc_id = self.db.insert(
                    {
                    'name':name, 
                    'captures':[], 
                    'records':[], 
                    'recording':False
                    }
                )
            return True
        else:
            return False

    def add_capture(self, capture:ImageInfo):
        self.db.update(lambda doc: doc['captures'].append(capture.__dict__), doc_ids=[self.doc_id])

    def add_record(self, record:RecordInfo):
        def update_record(doc):
            records = doc['records']
            if records and record.path == records[-1]['path']:
                records[-1]['stop_date_time'] = record.stop_date_time
            else:
                record_dict = record.__dict__
                record_dict['stop_date_time'] = record.stop_date_time  
                records.append(record_dict)

        self.db.update(update_record, doc_ids=[self.doc_id])

    def update_status(self, recording:bool):
        self.db.update({'recording':recording}, doc_ids=[self.doc_id])

    def get_status(self):
        return self.db.get(doc_id=self.doc_id)['recording']
    
    def session_exists(self, name):
        doc = self.db.search(Query().name == name)
        if doc:
            return True
        else:
            return False

    def print_session(self):
        print(self.db.get(doc_id=self.doc_id))

    def print_all_sessions(self):
        print(self.db.all())

    def get_sessions(self):
        return self.db.all()
    
    def get_session(self, name:str)->dict:
        return self.db.get(Query().name == name)
    
    def is_session_attached(self):
        if self.doc_id:
            return True
        else:
            return False