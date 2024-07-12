from Video.domain.entities import ImageInfo, RecordInfo
from tinydb import TinyDB, Query
from Video.ports.db_link import DbLink
from logging import Logger

class TinyDbLink(DbLink):
    def __init__(self, db_name: str, logger: Logger) -> None:
        self.db = TinyDB(db_name)
        self.doc_id = None
        self.logger = logger

    def create(self, name: str) -> bool:
        try:
            if not self.session_exists(name=name):
                self.doc_id = self.db.insert(
                    {
                        'name': name,
                        'captures': [],
                        'records': [],
                        'recording': False
                    }
                )
                return True
            else:
                return False
        except Exception as e:
            self.logger.error(f"Error creating session: {e}")
            return False

    def add_capture(self, capture: ImageInfo):
        try:
            self.db.update(lambda doc: doc['captures'].append(capture.__dict__), doc_ids=[self.doc_id])
        except Exception as e:
            self.logger.error(f"Error adding capture: {e}")

    def add_record(self, record: RecordInfo):
        def update_record(doc):
            try:
                records = doc['records']
                if records and record.path == records[-1]['path']:
                    records[-1]['stop_date_time'] = record.stop_date_time
                else:
                    record_dict = record.__dict__
                    record_dict['stop_date_time'] = record.stop_date_time
                    records.append(record_dict)
            except Exception as e:
                self.logger.error(f"Error updating record: {e}")

        try:
            self.db.update(update_record, doc_ids=[self.doc_id])
        except Exception as e:
            self.logger.error(f"Error adding record: {e}")

    def update_status(self, recording: bool):
        try:
            self.db.update({'recording': recording}, doc_ids=[self.doc_id])
        except Exception as e:
            self.logger.error(f"Error updating status: {e}")

    def get_status(self):
        try:
            return self.db.get(doc_id=self.doc_id)['recording']
        except Exception as e:
            self.logger.error(f"Error getting status: {e}")
            return False

    def session_exists(self, name):
        try:
            doc = self.db.search(Query().name == name)
            return bool(doc)
        except Exception as e:
            self.logger.error(f"Error checking if session exists: {e}")
            return False

    def print_session(self):
        try:
            print(self.db.get(doc_id=self.doc_id))
        except Exception as e:
            self.logger.error(f"Error printing session: {e}")

    def print_all_sessions(self):
        try:
            print(self.db.all())
        except Exception as e:
            self.logger.error(f"Error printing all sessions: {e}")

    def get_sessions(self):
        try:
            return self.db.all()
        except Exception as e:
            self.logger.error(f"Error getting sessions: {e}")
            return []

    def get_session(self, name: str) -> dict:
        try:
            return self.db.get(Query().name == name)
        except Exception as e:
            self.logger.error(f"Error getting session: {e}")
            return {}

    def is_session_attached(self):
        return self.doc_id is not None
