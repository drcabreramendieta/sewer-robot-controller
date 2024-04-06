from Video.ports.dvr_link import DvrLink
from Video.domain.entities import ImageInfo, RecordInfo
import requests
from requests.auth import HTTPBasicAuth
import os
from datetime import datetime


class HikvisionDvrLink(DvrLink):
    def __init__(self, url: str, user: str, password: str, dir:str) -> None:
        super().__init__()
        self.url = url
        self.username = user
        self.password = password
        self.folder = None
        self.dir = dir
        os.makedirs(self.dir, exist_ok=True)

    def take_image(self) -> ImageInfo:
        if self.folder:
            image_url = f"{self.url}/ISAPI/Streaming/channels/101/picture?videoResolutionWidth=1280&videoResolutionHeight=720"
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            image_name = f'image_{timestamp}.jpg' 
            image_path = os.path.join(self.storage, image_name)  
            
            response = requests.get(image_url, auth=HTTPBasicAuth(self.username, self.password))
            
            if response.status_code == 200:
                with open(image_path, 'wb') as image_file:
                    image_file.write(response.content)
                
                return ImageInfo(image_path, timestamp)
            else:
                print(f"Error al capturar la imagen: {response.status_code}")
                return ImageInfo('', '')

    def download_image(self, image_info: ImageInfo) -> str:
        if os.path.exists(image_info.path):
            # Las imágenes no se guardan en el DVR, el jpg se envía como respuesta a la  
            # petición HTTP y es almacendado en el propio computador en el path especificado
            return image_info.path
        else:
            
            print("El archivo de imagen no existe en la ruta proporcionada.")
            return ""

    def download_video(self, record_info:RecordInfo) -> str:
        # TODO: Aquí implementar la descarga del archivo de video en una carpeta temporal del raspberry y devolver la ruta del archivo descargado
        return record_info.path

    def start_recording(self) -> bool:
        start_url = f"{self.url}/ISAPI/ContentMgmt/record/control/manual/start/tracks/101"
        response = requests.put(start_url, auth=HTTPBasicAuth(self.username, self.password))
        if response.status_code == 200:
            print("Grabación iniciada con éxito.")
            self.start_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        else:
            print(f"Error al iniciar grabación: {response.status_code}")
        return True

    def stop_recording(self) -> RecordInfo:
        stop_url = f"{self.url}/ISAPI/ContentMgmt/record/control/manual/stop/tracks/101"
        response = requests.put(stop_url, auth=HTTPBasicAuth(self.username, self.password))
        if response.status_code == 200:
            print("Grabación detenida con éxito.")
            end_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        else:
            print(f"Error al detener grabación: {response.status_code}")
        return RecordInfo(self.storage, end_time, self.start_time)
    
    def set_folder(self, name: str):
        self.folder = name
        self.storage = os.path.join(self.dir, self.folder)
        os.makedirs(self.storage, exist_ok=True)
    