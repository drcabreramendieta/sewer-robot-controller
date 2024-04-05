from Video.ports.dvr_link import DvrLink
from Video.ports.db_link import DbLink
from Video.domain.entities import DvrOrder

class ControlSession:
    def __init__(self, dvr_link:DvrLink, db_link:DbLink) -> None:
        self.dvr_link = dvr_link
        self.db_link = db_link

    def create_session(self, name:str) -> bool:
        return self.db_link.create(name=name)
    
    def name_exists(self, name:str) -> bool:
        return self.db_link.session_exists(name=name)

    def run(self, order:DvrOrder):
        if self.db_link:
            if order == DvrOrder.TAKE_PHOTO:
                self.db_link.add_capture(self.dvr_link.take_image())
            elif order == DvrOrder.START_RECORDING:
                self.db_link.update_status(self.dvr_link.start_recording())
            elif order == DvrOrder.STOP_RECORDING and self.db_link.get_status():
                self.db_link.add_record(self.dvr_link.stop_recording())
                self.db_link.update_status(recording=False)
            self.db_link.print_session()
    
    def update_session_name(self, new_session_name: str):
        self.dvr_link.update_session_name(new_session_name)