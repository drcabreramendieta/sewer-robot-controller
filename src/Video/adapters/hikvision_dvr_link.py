from Video.ports.dvr_link import DvrLink
from Video.domain.entities import ImageInfo, RecordInfo
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import os
import requests
import subprocess
import shlex
from logging import Logger
from Inspection.ui.main_window import MainWindow

TIMEOUT = 2  # Definimos un timeout de 10 segundos

class HikvisionDvrLink(DvrLink):
    def __init__(self, url: str, user: str, password: str, dir: str, logger: Logger) -> None:
        super().__init__()
        self.url = url
        self.username = user
        self.password = password
        self.folder = None
        self.dir = dir
        self.logger = logger
        
        os.makedirs(self.dir, exist_ok=True)

    def take_image(self) -> ImageInfo:
        if self.folder:
            image_url = f"{self.url}/ISAPI/Streaming/channels/101/picture?videoResolutionWidth=1280&videoResolutionHeight=720"
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            image_name = f'image_{timestamp}.jpg' 
            image_path = os.path.join(self.storage, image_name)
            
            try:
                response = requests.get(image_url, auth=HTTPBasicAuth(self.username, self.password), timeout=TIMEOUT)
                response.raise_for_status()
                with open(image_path, 'wb') as image_file:
                    image_file.write(response.content)
                
                return ImageInfo(image_path, timestamp)
            except requests.exceptions.Timeout:
                self.logger.error("Timeout al capturar la imagen.")
                MainWindow.show_error_dialog_restart()
                return ImageInfo('', '')
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Error al capturar la imagen: {e}")
                return ImageInfo('', '')

    def search_video(self, session_info):
        records = session_info.get("records", [])
        if not records:
            self.logger.info("No existen grabaciones.")
            return []

        playback_uris = []
        for record in records:
            start_time = datetime.strptime(record["start_date_time"], "%Y%m%d_%H%M%S").strftime("%Y-%m-%dT%H:%M:%SZ")
            stop_time = datetime.strptime(record["stop_date_time"], "%Y%m%d_%H%M%S").strftime("%Y-%m-%dT%H:%M:%SZ")
            self.logger.info(f"Start Time: {start_time}, Stop Time: {stop_time}")

            video_url = f"{self.url}/ISAPI/ContentMgmt/search"
            xml_body = f"""<?xml version="1.0" encoding="utf-8"?>
                            <CMSearchDescription>
                            <searchID>484c3433-3733-3131-3636-e0baadf09c77</searchID>
                            <trackList>
                            <trackID>101</trackID>
                            </trackList>
                            <timeSpanList>
                            <timeSpan>
                            <startTime>{start_time}</startTime>
                            <endTime>{stop_time}</endTime>
                            </timeSpan>
                            </timeSpanList>
                            <maxResults>100</maxResults>
                            <searchResultPosition>0</searchResultPosition>
                            <metadataList>
                            <metadataDescriptor>//recordType.meta.std-cgi.com</metadataDescriptor>
                            </metadataList>
                            </CMSearchDescription>"""

            headers = {'Content-Type': 'application/xml'}
            try:
                response = requests.post(video_url, data=xml_body, headers=headers, auth=HTTPBasicAuth(self.username, self.password), timeout=TIMEOUT)
                response.raise_for_status()
                root = ET.fromstring(response.text)
                ns = {'default': 'http://www.hikvision.com/ver20/XMLSchema'}
                playback_uris.extend([elem.text for elem in root.findall(".//default:mediaSegmentDescriptor/default:playbackURI", namespaces=ns)])
                search_success = True
            except requests.exceptions.Timeout:
                self.logger.error("Timeout en la conexión a la API.")
                search_success = False
                MainWindow.show_error_dialog_restart()
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Error en la conexión a la API: {e}")
                search_success = False
            except ET.ParseError as e:
                self.logger.error(f"Error al parsear la respuesta XML: {e}")
                search_success = False

        return playback_uris, search_success

    def download_video(self, session_info, target_folder):

        [video_uris, search_success] = self.search_video(session_info)

        if search_success == False:
            download_success = False
        else:
            download_success = True

        download_url = f"{self.url}/ISAPI/ContentMgmt/download"
        
        session_name = session_info.get("name")

        for i, uri in enumerate(video_uris, start=1):
            xml_body = f"""<?xml version="1.0" encoding="utf-8"?>
                        <downloadRequest version="1.0" xmlns="http://www.isapi.org/ver20/XMLSchema">
                        <playbackURI>{uri}</playbackURI>
                        </downloadRequest>"""

            if not target_folder.endswith("/"):
                target_folder += "/"
            output_file = f"{target_folder}_video_{session_name}_{i}.mp4"

            curl_command = f'curl -X POST -d \'{xml_body}\' -H "Content-Type: application/xml" --user "{self.username}:{self.password}" -o "{output_file}" "{download_url}"'

            args = shlex.split(curl_command)

            try:
                download_success = True
                subprocess.run(args, check=True)
                self.logger.info(f"Descarga exitosa para: {uri}, guardado en {output_file}")
            except subprocess.CalledProcessError as e:
                download_success = False  
                self.logger.error(f"Error en la descarga para: {uri} - Error: {e}")               
                
        return download_success
       
    def adjust_time(self, time_str: str, delta: int, unit: str = 'minutes') -> str:
        try:
            time = datetime.strptime(time_str, '%Y%m%d_%H%M%S')
            adjusted_time = time - timedelta(**{unit: delta})
            adjusted_time_str = adjusted_time.strftime('%Y%m%d_%H%M%S')
            return adjusted_time_str
        except ValueError as e:
            self.logger.error(f"Error al ajustar el tiempo: {e}")
            return time_str

    def start_recording(self) -> bool:
        start_url = f"{self.url}/ISAPI/ContentMgmt/record/control/manual/start/tracks/101"
        try:
            response = requests.put(start_url, auth=HTTPBasicAuth(self.username, self.password), timeout=TIMEOUT)
            response.raise_for_status()
            self.logger.info("Grabación iniciada con éxito.")
            self.start_time = datetime.now().strftime('%Y%m%d_%H%M%S')
            return True
        except requests.exceptions.Timeout:
            self.logger.error("Timeout al iniciar grabación.")
            MainWindow.show_error_dialog_restart()
            self.stop_recording()
            return False
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error al iniciar grabación: {e}")
            return False

    def stop_recording(self) -> RecordInfo:
        stop_url = f"{self.url}/ISAPI/ContentMgmt/record/control/manual/stop/tracks/101"
        try:
            response = requests.put(stop_url, auth=HTTPBasicAuth(self.username, self.password), timeout=TIMEOUT)
            response.raise_for_status()
            self.logger.info("Grabación detenida con éxito.")
            end_time = datetime.now().strftime('%Y%m%d_%H%M%S')
            return RecordInfo(self.storage, end_time, self.start_time)
        except requests.exceptions.Timeout:
            self.logger.error("Timeout al detener grabación.")
            MainWindow.show_error_dialog_restart()
            return RecordInfo(self.storage, '', '')
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error al detener grabación: {e}")
            return RecordInfo(self.storage, '', '')

    def set_folder(self, name: str):
        self.folder = name
        self.storage = os.path.join(self.dir, self.folder)
        os.makedirs(self.storage, exist_ok=True)
