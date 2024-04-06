from Video.ports.dvr_link import DvrLink
from Video.ports.db_link import DbLink
from Video.domain.entities import DvrOrder

class ControlSession:
    def __init__(self, dvr_link:DvrLink, db_link:DbLink) -> None:
        self.dvr_link = dvr_link
        self.db_link = db_link

    def create_session(self, name:str) -> bool:
        if self.db_link.create(name=name):
            self.dvr_link.set_folder(name=name)
            return True
        return False
    
    def name_exists(self, name:str) -> bool:
        return self.db_link.session_exists(name=name)
    
    def get_sessions(self) -> list:
        return self.db_link.get_sessions()
    
    def download_session(self, name:str, target:str):
        session = self.db_link.get_session(name=name)
        for image_info in session['captures']:
            # Copia la imagen a la carpeta target
            print(image_info['path'])

        for record_info in session['records']:
            downloaded_path = self.dvr_link.download_video(record_info=record_info)
            # Copiar el video descargado a la carpeta target y eliminarlo de la carpeta temporal
            print(downloaded_path)

    def run(self, order:DvrOrder):
        if self.db_link.is_session_attached():
            if order == DvrOrder.TAKE_PHOTO:
                self.db_link.add_capture(self.dvr_link.take_image())
            elif order == DvrOrder.START_RECORDING:
                self.db_link.update_status(self.dvr_link.start_recording())
            elif order == DvrOrder.STOP_RECORDING and self.db_link.get_status():
                self.db_link.add_record(self.dvr_link.stop_recording())
                self.db_link.update_status(recording=False)