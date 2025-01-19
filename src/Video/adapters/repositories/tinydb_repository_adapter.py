from Video.domain.entities.repository_entities import ImageInfo
from Video.domain.entities.repository_entities import RecordInfo
from tinydb import TinyDB, Query
from Video.ports.output.repository_port import RepositoryPort
from logging import Logger
"""TinyDB repository adapter implementation.

This module provides database storage functionality using TinyDB
for managing inspection sessions, captures and recordings.
"""
class TinydbRepositoryAdapter(RepositoryPort):
    """Repository adapter using TinyDB for data storage.

    Args:
        db_name (str): Path to TinyDB database file
        logger (Logger): Logger instance for operation tracking

    Attributes:
        db: TinyDB database instance
        doc_id: Current session document ID
        logger: Operations logger
    """
    def __init__(self, db_name: str, logger: Logger) -> None:
        """Initialize TinyDB repository.

        Args:
            db_name (str): Database file path
            logger (Logger): Logger instance

        Raises:
            ValueError: If db_name or logger is invalid
        """
        self.db = TinyDB(db_name)
        self.doc_id = None
        self.logger = logger

    def create(self, name: str) -> bool:
        """Create new inspection session.

        Args:
            name (str): Session name

        Returns:
            bool: True if session created successfully

        Raises:
            Exception: If database operation fails
        """
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
        """Add captured image to session.

        Args:
            capture (ImageInfo): Image capture information

        Raises:
            Exception: If database update fails
        """
        try:
            self.db.update(lambda doc: doc['captures'].append(capture.__dict__), doc_ids=[self.doc_id])
        except Exception as e:
            self.logger.error(f"Error adding capture: {e}")

    def add_record(self, record: RecordInfo):
        """Add recording information to session.

        Args:
            record (RecordInfo): Recording information

        Raises:
            Exception: If database update fails
        """
        def update_record(doc):
            """Update session recording status.

            Args:
                recording (bool): Current recording state

            Raises:
                Exception: If status update fails
            """

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
        """Update session recording status.

        Args:
            recording (bool): Current recording state

        Raises:
            Exception: If status update fails
        """
        try:
            self.db.update({'recording': recording}, doc_ids=[self.doc_id])
        except Exception as e:
            self.logger.error(f"Error updating status: {e}")

    def get_status(self):
        """Get current session recording status.

        Returns:
            bool: True if recording in progress

        Raises:
            Exception: If status query fails
        """
        try:
            return self.db.get(doc_id=self.doc_id)['recording']
        except Exception as e:
            self.logger.error(f"Error getting status: {e}")
            return False

    def session_exists(self, name):
        """Check if session name exists.

        Args:
            name (str): Session name to check

        Returns:
            bool: True if session exists

        Raises:
            Exception: If query fails
        """
        try:
            doc = self.db.search(Query().name == name)
            return bool(doc)
        except Exception as e:
            self.logger.error(f"Error checking if session exists: {e}")
            return False

    def print_session(self):
        """Print current session data.

        Raises:
            Exception: If session query fails
        """
        try:
            print(self.db.get(doc_id=self.doc_id))
        except Exception as e:
            self.logger.error(f"Error printing session: {e}")

    def print_all_sessions(self):
        """Print all session data.

        Raises:
            Exception: If query fails
        """
        try:
            print(self.db.all())
        except Exception as e:
            self.logger.error(f"Error printing all sessions: {e}")

    def get_sessions(self):
        """Get list of all sessions.

        Returns:
            list: List of session documents

        Raises:
            Exception: If query fails
        """
        try:
            return self.db.all()
        except Exception as e:
            self.logger.error(f"Error getting sessions: {e}")
            return []

    def get_session(self, name: str) -> dict:
        """Get session by name.

        Args:
            name (str): Session name to retrieve

        Returns:
            dict: Session document or empty dict if not found

        Raises:
            Exception: If query fails
        """
        try:
            return self.db.get(Query().name == name)
        except Exception as e:
            self.logger.error(f"Error getting session: {e}")
            return {}

    def is_session_attached(self):
        """Check if session is currently attached.

        Returns:
            bool: True if session is attached
        """
        return self.doc_id is not None
