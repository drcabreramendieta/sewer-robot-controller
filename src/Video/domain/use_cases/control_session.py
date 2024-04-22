from Video.ports.dvr_link import DvrLink
from Video.ports.db_link import DbLink
from Video.domain.entities import DvrOrder


import shutil
import os


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
        sessions = self.db_link.get_sessions()
        return [session["name"] for session in sessions]

    
    def download_session(self, session_name, target_folder):
        os.makedirs(target_folder, exist_ok=True)
        session_info = self.db_link.get_session(session_name)
        print(session_info)
        
        if not session_info:
            print("Sesión no encontrada.")
            return False

        print(f"Sesión encontrada: {session_name}")
        image_success = True
        content_found = False

        captures = session_info.get("captures", [])
        if captures:
            content_found = True
            for capture in captures:
                source_path = capture["path"]
                if os.path.exists(source_path):
                    file_name = os.path.basename(source_path)
                    destination_path = os.path.join(target_folder, file_name)
                    print(destination_path)
                    shutil.copy(source_path, destination_path)
                    print(f"Archivo {file_name} copiado correctamente.")
                else:
                    print(f"El archivo {source_path} no existe y no puede ser copiado.")
                    image_success = False

        video_uris = self.dvr_link.search_video(session_info)
        video_success = True
        if video_uris:
            content_found = True
            video_success = self.dvr_link.download_video(session_info, target_folder)

        if not content_found:
            print("La sesión no cuenta con videos ni imágenes.")
            return None

        if image_success and video_success:
            print("Todas las imágenes y videos fueron procesados correctamente.")
            return True
        else:
            if not image_success:
                print("Algunas imágenes no pudieron ser procesadas correctamente.")
            if not video_success:
                print("Los videos no pudieron ser procesados correctamente.")
            return False

    def run(self, order:DvrOrder):
        if self.db_link.is_session_attached():
            if order == DvrOrder.TAKE_PHOTO:
                self.db_link.add_capture(self.dvr_link.take_image())
            elif order == DvrOrder.START_RECORDING:
                self.db_link.update_status(self.dvr_link.start_recording())
            elif order == DvrOrder.STOP_RECORDING and self.db_link.get_status():
                self.db_link.add_record(self.dvr_link.stop_recording())
                self.db_link.update_status(recording=False)