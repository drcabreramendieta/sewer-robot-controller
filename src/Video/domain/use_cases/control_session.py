from Video.ports.dvr_link import DvrLink
from Video.ports.db_link import DbLink
from Video.domain.entities import DvrOrder

import json
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
    
    def get_sessions(self, json_file_path) -> list:
        with open(json_file_path, 'r') as file:
            json_data = json.load(file)
        return [session_info["name"] for session_info in json_data["_default"].values()]
        
    
    def download_session(self, json_path, session_name, target_folder):
        os.makedirs(target_folder, exist_ok=True)
        with open(json_path, 'r') as file:
            json_data = json.load(file)

        print(f"Buscando sesión: {session_name}")
        image_success = True
        session_found = False
        content_found = False

        for session_info in json_data["_default"].values():
            if session_info["name"] == session_name:
                print(f"Sesión encontrada: {session_name}")
                session_found = True
                captures = session_info.get("captures", [])
                if captures:
                    content_found = True
                    for capture in captures:
                        source_path = capture["path"]
                        if os.path.exists(source_path):
                            file_name = os.path.basename(source_path)
                            destination_path = os.path.join(target_folder, file_name)
                            shutil.copy(source_path, destination_path)
                            print(f"Archivo {file_name} copiado correctamente.")
                        else:
                            print(f"El archivo {source_path} no existe y no puede ser copiado.")
                            image_success = False
                break

        if not session_found:
            print("Sesión no encontrada.")
            return False

        video_uris = self.dvr_link.search_video(json_path, session_name)
        video_success = True
        if video_uris:
            content_found = True
            video_success = self.dvr_link.download_video(json_path, session_name, target_folder)

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