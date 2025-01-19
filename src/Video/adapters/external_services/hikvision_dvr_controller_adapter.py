from Video.domain.entities.repository_entities import ImageInfo
from Video.ports.output.dvr_controller_port import DvrControllerPort
from Video.domain.entities.repository_entities import RecordInfo
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import os
import requests
import subprocess
import shlex
from logging import Logger
from Inspection.adapters.gui.main_window import MainWindow
"""Hikvision DVR controller adapter implementation.

This module provides integration with Hikvision DVR systems through their
HTTP API for video recording, image capture and file downloads.
"""
TIMEOUT = 2  # Definimos un timeout de 10 segundos

class HikvisionDvrControllerAdapter(DvrControllerPort):
    """Adapter for controlling Hikvision DVR through HTTP API.

    Args:
        url (str): Base URL for DVR HTTP API
        user (str): Authentication username
        password (str): Authentication password
        dir (str): Base directory for storing recordings
        logger (Logger): Logger instance for operation tracking

    Attributes:
        url: DVR API base URL
        username: Auth username
        password: Auth password
        folder: Current session folder name
        dir: Base storage directory
        logger: Operations logger
        storage: Current session storage path
    """
    def __init__(self, url: str, user: str, password: str, dir: str, logger: Logger) -> None:
        """Initialize Hikvision DVR controller.

        Args:
            url (str): DVR API base URL
            user (str): Auth username
            password (str): Auth password  
            dir (str): Storage base directory
            logger (Logger): Logger instance

        Raises:
            ValueError: If required parameters are invalid
        """
        super().__init__()
        self.url = url
        self.username = user
        self.password = password
        self.folder = None
        self.dir = dir
        self.logger = logger
        
        os.makedirs(self.dir, exist_ok=True)

    def take_image(self) -> ImageInfo:
        """Capture current camera image.

        Returns:
            ImageInfo: Image path and timestamp info. Empty if failed.

        Raises:
            requests.exceptions.RequestException: If API request fails
            requests.exceptions.Timeout: If request times out
        """
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
        """Search for video recordings in given time range.

        Args:
            session_info (dict): Session info with start/stop times

        Returns:
            tuple: List of video URIs and search success flag

        Raises:
            requests.exceptions.RequestException: If API request fails 
            ET.ParseError: If response XML is invalid
        """
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
        """Download video recordings to target folder.

        Args:
            session_info (dict): Session info with name and times
            target_folder (str): Destination folder path

        Returns:
            bool: True if download successful

        Raises:
            subprocess.CalledProcessError: If download fails
        """

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
        """Adjust timestamp by given delta.

        Args:
            time_str (str): Timestamp string (format: YYYYMMDD_HHMMSS)
            delta (int): Time adjustment amount
            unit (str, optional): Time unit. Defaults to 'minutes'.

        Returns:
            str: Adjusted timestamp string

        Raises:
            ValueError: If time string format is invalid
        """
        try:
            time = datetime.strptime(time_str, '%Y%m%d_%H%M%S')
            adjusted_time = time - timedelta(**{unit: delta})
            adjusted_time_str = adjusted_time.strftime('%Y%m%d_%H%M%S')
            return adjusted_time_str
        except ValueError as e:
            self.logger.error(f"Error al ajustar el tiempo: {e}")
            return time_str

    def start_recording(self) -> bool:
        """Start video recording.

        Returns:
            bool: True if recording started successfully

        Raises:
            requests.exceptions.RequestException: If start request fails
            requests.exceptions.Timeout: If request times out
        """
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
        """Stop current video recording.

        Returns:
            RecordInfo: Recording path and timestamp info. Empty if failed.

        Raises:
            requests.exceptions.RequestException: If stop request fails
            requests.exceptions.Timeout: If request times out
        """
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
        """Set current session folder.

        Args:
            name (str): Folder name for current session

        Raises:
            OSError: If folder creation fails
        """
        self.folder = name
        self.storage = os.path.join(self.dir, self.folder)
        os.makedirs(self.storage, exist_ok=True)
