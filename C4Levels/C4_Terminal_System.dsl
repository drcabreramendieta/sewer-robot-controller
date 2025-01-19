workspace "Terminal System" "System Context, Container, and Component diagrams" {

    !identifiers hierarchical

    model {
        operator = person "Operator" "Technical person who operates the pipeline inspection robot"
        
        terminal_system = softwareSystem "Terminal System" "Allows operators to control and monitor pipeline inspection robots" {
            
            # Containers
            inspection = container "Inspection Module" "Handles UI, robot control, and module coordination. Configures sessions in the Video module using the Session module API to manage video streams and interactions." {
                
                MainWindow = component "MainWindow" "Serves as the graphical user interface (GUI) for the Inspection Module. Allows monitoring of feeder operations, telemetry data, video updates, session status, and robot activity. Facilitates interaction with all services through PyQt signals" url "https://dl.dropboxusercontent.com/scl/fi/zjnri638wwa5sppfiqqh7/MainWindow.png?rlkey=9l4ipst7ujthuwaqj79z9s51a&st=pr9v4125&dl=0"
                FeederUpdateService = component "FeederUpdateService" "Handles updates and interactions with the feeder system. Uses FeederControllerPort for communication and notifies observers via FeederObserverPort. Communicates with the MainWindow through GuiFeederObserverAdapter." url "https://dl.dropboxusercontent.com/scl/fi/3solj8to9jhuf6fq7f4lk/FeederUpdateServicePort.png?rlkey=61gnbhulsomsolgfdejg7bjnx&st=h9zhkb6x&dl=0"
                TelemetryUpdateService = component "TelemetryUpdateService" "Processes telemetry updates from the robot. Notifies observers via TelemetryObserverPort and communicates with the MainWindow through GuiTelemetryObserverAdapter." url "https://dl.dropboxusercontent.com/scl/fi/n5md50yihf6kjmuqhwtb9/TelemetryUpdateServicePort.png?rlkey=p9m82r96eh04qia7byizz441e&st=ciuqwkem&dl=0"
                VideoUpdateService = component "VideoUpdateService" "Manages video stream updates. Notifies observers via VideoObserverPort and communicates with the MainWindow using GuiVideoObserverAdapter." url "https://dl.dropboxusercontent.com/scl/fi/cifh4vh0rzl0cacyp6sxu/VideoUpdateServicePort.png?rlkey=jdaaglao8t9awvdkgeme7wvsd&st=sulxa4sj&dl=0"
                SessionServices = component "SessionServices" "Handles session management, including starting, stopping, and downloading sessions. Uses SessionControllerPort for session operations and communicates with the MainWindow through SessionServicesPort."  url "https://dl.dropboxusercontent.com/scl/fi/9umdqxyeeiq6tqc2grzwe/SessionServicePort.png?rlkey=uivz6rp4of3icwonadzbicuad&st=eu25fn5f&dl=0"
                PanelUpdateServices = component "PanelUpdateServices" "Manages robot and camera control. Communicates with MovementControllerPort for robot movement and CameraControllerPort for camera operations, and interacts with the MainWindow through PanelUpdateServicesPort." url "https://dl.dropboxusercontent.com/scl/fi/7kosxmo6z7jc5x31quv18/PanelUpdateServicePort.png?rlkey=odvyud46qxwjh9p3lgcua0n3t&st=qph1ez2n&dl=0"            
            }

            communication = container "Communication Module" "Python + python-can" "Manages CAN bus communications with the robot" {

                telemetryServices = component "TelemetryServices" "Handles telemetry data via CAN bus and uses PyQt signal mechanism through PyqtTelemetryObserverAdapter for asynchronous telemetry updates in the GUI" url "https://dl.dropboxusercontent.com/scl/fi/rglwt8rtc55klqdhgyaoc/TelemetryServicePort.png?rlkey=f3j6ex9jz56lpwp0vfryqmh9e&st=6p98r2m4&dl=0"
                cameraServices = component "CameraServices" "Controls camera operations and interfaces with the CAN bus through CanCameraControllerAdapter." url "https://dl.dropboxusercontent.com/scl/fi/pu4x2dsqw7ei9wy5s9quz/CameraServicePort.png?rlkey=oa5zhtm23035ajd778mcrx08r&st=mkrj3710&dl=0"                                                                                               
                movementService = component "MovementService" "Controls robot movement and interfaces with the CAN bus via the CanWheelsControllerAdapter." url "https://dl.dropboxusercontent.com/scl/fi/j2mpget1wbjfyyqjhm4lr/MovementServicePort.png?rlkey=1kbxvq670aftaqaq272vngwfg&st=dz7ghq91&dl=0"
                canBus = component "CAN Bus" "Handles Communication" "Shared communication bus for modules"
            }

            video = container "Video Module" "Python + OpenCV + PyQt" "Handles video streaming, recording, storage, and session management. " {
                SessionServices = component "Session Services" "Manages video recording sessions, including creating, downloading, and retrieving session data. Connects to DVR systems through the DvrControllerPort, implemented by the HikvisionDvrControllerAdapter. Uses the RepositoryPort, implemented by the TinyDBRepositoryAdapter, for local storage and metadata management."  url "https://dl.dropboxusercontent.com/scl/fi/zki2x58brfwm327sozz6d/SessionServicePort.png?rlkey=sxy4jbvjrrejphptrkikiiq6p&st=fwpatcfa&dl=0"
                VideoServices = component "Video Services" "Handles video streaming and observer notifications. Connects to video sources via the VideoControllerPort for video capture and streaming. Manages observer notifications using the VideoObserverPort, implemented by the PyQtVideoObserverAdapter and PyQtSignalCamera, for real-time updates and notifications." url "https://dl.dropboxusercontent.com/scl/fi/x0gpcmtc7dsm5isc9s3yr/VideoServicePort.png?rlkey=b7gmnl7nfc9hjnep48vrs421o&st=9empwzj2&dl=0"
            }


            panel_feeder = container "Panel and Feeder Module" "Python + PySerial" "Controls panel interface and feeder mechanisms" {
            # Services
                panelServices = component "Panel Services" "Implements panel operations and PyQt updates; uses PanelAndFeederControllerPort and implements PanelObserverPort" url "https://dl.dropboxusercontent.com/scl/fi/6wlpwj6wq7ispro6zqwgk/Panel_and_feder.png?rlkey=idoi1dvwbdzeq2qrqnah0q0a1&st=s3mgehrh&dl=0"
                feederServices = component "Feeder Services" "Implements feeder operations and PyQt updates; uses PanelAndFeederControllerPort and implements FeederObserverPort" url "https://dl.dropboxusercontent.com/scl/fi/6wlpwj6wq7ispro6zqwgk/Panel_and_feder.png?rlkey=idoi1dvwbdzeq2qrqnah0q0a1&st=s3mgehrh&dl=0"
                serialPanelFeederAdapter = component "Serial Panel Feeder Adapter" "Implements Panel And Feeder Controller Port with PySerial" 
            }

            
        }

        pipeline_robot = element "Pipeline Inspection Robot" "External physical robot for pipeline inspections" "Hardware System"


        dvr = element "DVR System" "An external system for managing digital video recording, including storage and playback. Receives video streams from the robot camera for recording and live monitoring. Acts as an intermediary to store and provide access to recorded and real-time video feeds."     "Hardware System"


        panel_and_feeder = element "Panel and Feeder System"    "External system for panel and feeder control. Sends user actions to the terminal and receives joystick actions."   "Hardware System"


        ### Context Level Relationships ok

        operator -> terminal_system "Operates through the terminal system to control the robot and monitor inspection data"
        terminal_system -> pipeline_robot "Transmits control commands for robot movement and camera positioning, and receives telemetry data."
        terminal_system -> dvr "Controls DVR operations and retrieves recorded video streams"    
        terminal_system -> panel_and_feeder  "Controls robot movement, camera positioning, and feeder operations" "Serial Communication"
        
        ### Container Level Relationships   
        operator -> terminal_system.inspection "Views and controls through GUI"
        terminal_system.inspection -> terminal_system.panel_feeder "Subscribes to the Panel and Feeder module to receive signals. Handles signals sent from the Panel and Feeder, enabling communication for inspection operations." "PyQt Signals"
        terminal_system.inspection -> terminal_system.video     "The Inspection module subscribes to the Video module to receive video streams and configures sessions in the Video module using the Session module API." "PyQt Signals"   
        // terminal_system.video -> dvr "Controls recording operations and receives video streams. Uses the Hikvision DVR server at 'http://192.168.18.155:80' to send and receive data." "HTTP Server"
        terminal_system.video -> dvr "Manages recording operations and receives video streams. The protocol used is Real-Time Streaming Protocol (RTSP) for real-time video data transmission." "RTSP Protocol"
        //terminal_system.communication -> terminal_system.inspection  "Sends movement commands for the robot's wheels and camera through API calls. Receives telemetry data from the robot." "API Communication"   
        terminal_system.communication -> pipeline_robot    "Controls the camera and robot movements, and receives telemetry data." "CAN"   
        ### Panel and Feeder components Relationships    

        terminal_system.panel_feeder.panelServices -> terminal_system.panel_feeder.serialPanelFeederAdapter "Forward Updates" "PyQt"
        terminal_system.panel_feeder.feederServices -> terminal_system.panel_feeder.serialPanelFeederAdapter "Sends feeder control commands" "Serial Communication"

        terminal_system.panel_feeder -> panel_and_feeder "Controls panel and feeder operations" "Serial Communication"
          
        ### Communication Module Internal Components

        # Services Layer Relationships
        terminal_system.communication.telemetryServices -> terminal_system.communication.canBus "Reads telemetry data"
        terminal_system.communication.movementService -> terminal_system.communication.canBus "Sends movement commands"
        terminal_system.communication.cameraServices -> terminal_system.communication.canBus "Controls camera"  
        # To Robot Hardware
        terminal_system.communication.canBus -> pipeline_robot   "Sends/receives CAN frames"
        
        ### Video Module External Components relatinons
        terminal_system.video.SessionServices -> dvr "Manages video recording sessions"
        terminal_system.video.VideoServices -> dvr "Handles video        streaming"
        ### Inspection Module Internal Components
       terminal_system.inspection.FeederUpdateService -> terminal_system.inspection.MainWindow "Subscribes to feeder updates, sending commands and receiving status notifications." "PyQt"

        terminal_system.inspection.TelemetryUpdateService -> terminal_system.inspection.MainWindow  "Subscribes to telemetry updates from the robot for real-time monitoring." "PyQt"

        terminal_system.inspection.VideoUpdateService -> terminal_system.inspection.MainWindow "Subscribes to video stream updates from the robot for display." "PyQt"

        terminal_system.inspection.SessionServices -> terminal_system.inspection.MainWindow "Subscribes to session management operations, including start, stop, and download." "PyQt"
        terminal_system.inspection.PanelUpdateServices -> terminal_system.inspection.MainWindow "Subscribes to robot and camera control updates for monitoring activity." "PyQt"

        ### Panel And feeder External Components
      

       terminal_system.inspection -> terminal_system.panel_feeder.panelServices "Sends Panel control commands"
       terminal_system.inspection -> terminal_system.panel_feeder.feederServices "Sends feeder control commands"

        ### Video Module Internal Components
        terminal_system.inspection -> terminal_system.video.SessionServices "Configures sessions in the Video module using the Session module API to manage video streams and interactions." "API"
        
        terminal_system.inspection -> terminal_system.video.VideoServices "Subscribes to video streams and updates from the Video module for display in the GUI." "PyQt"
        
      

        operator -> terminal_system.inspection.MainWindow "Views and controls through GUI"
        //terminal_system.communication -> terminal_system.inspection.TelemetryUpdateService "Sends telemetry data"
        terminal_system.inspection.VideoUpdateService -> terminal_system.video "Subscribes to video streams and updates from the Video module for display in the GUI." "PyQt"
        terminal_system.inspection.PanelUpdateServices -> terminal_system.panel_feeder "Subscribes to the Panel and Feeder module to receive signals. Handles signals sent from the Panel and Feeder, enabling communication for inspection operations." "PyQt Signals"

        terminal_system.inspection -> terminal_system.communication "Sends movement commands for the robot's wheels and camera through API calls. Receives telemetry data from the robot" "Api Communication"
        terminal_system.inspection -> terminal_system.communication.telemetryServices "Telemetry data" "CAN" 
        terminal_system.inspection -> terminal_system.communication.cameraServices "Camera Operations" "CAN"
        terminal_system.inspection -> terminal_system.communication.movementService "Movement Operations" "CAN"
      
        terminal_system.panel_feeder.serialPanelFeederAdapter ->  panel_and_feeder

     
    }

    views 
    
        systemContext terminal_system "SystemContext" {
            include *
            autoLayout
        }
        
        
    
        

        container terminal_system "Containers" {
            include *
            autoLayout
        }

        
        component terminal_system.panel_feeder "Panel_and_Feeder_components" {
            include *
            autoLayout
        }


        component terminal_system.inspection "inspection_components" {
            include *
            autoLayout
        }



        component terminal_system.communication "communication_components" {
            include *
            autoLayout
        }

        component terminal_system.video "video_components" {
            include *
            autoLayout
        }


        #  Adding an image associated with Communication=====================================
         image terminal_system.communication.telemetryServices {
            image "https://dl.dropboxusercontent.com/scl/fi/rglwt8rtc55klqdhgyaoc/TelemetryServicePort.png?rlkey=f3j6ex9jz56lpwp0vfryqmh9e&st=6p98r2m4&dl=0"
            title "Detailed Diagram class for Telemetry Services"
        }
        
    
     
         image terminal_system.communication.cameraServices {
            image "https://dl.dropboxusercontent.com/scl/fi/pu4x2dsqw7ei9wy5s9quz/CameraServicePort.png?rlkey=oa5zhtm23035ajd778mcrx08r&st=mkrj3710&dl=0"
            title "Detailed Diagram class for Camera Services"
        }
        
        image terminal_system.communication.cameraServices {
            image "https://dl.dropboxusercontent.com/scl/fi/j2mpget1wbjfyyqjhm4lr/MovementServicePort.png?rlkey=1kbxvq670aftaqaq272vngwfg&st=dz7ghq91&dl=0"
            title "Detailed Diagram class for Movement Services"
        }
        
        # Adding an image associated with Inspection===============================================================================
        image terminal_system.inspection.MainWindow {
            image "https://dl.dropboxusercontent.com/scl/fi/zjnri638wwa5sppfiqqh7/MainWindow.png?rlkey=9l4ipst7ujthuwaqj79z9s51a&st=pr9v4125&dl=0"
              title "Detailed Diagram class for MainWindow"
        }
        
        
        image terminal_system.inspection.FeederUpdateService {
            image "https://dl.dropboxusercontent.com/scl/fi/3solj8to9jhuf6fq7f4lk/FeederUpdateServicePort.png?rlkey=61gnbhulsomsolgfdejg7bjnx&st=h9zhkb6x&dl=0"
              title "Detailed Diagram class for Feeder Update Service"
        }
        
        image terminal_system.inspection.TelemetryUpdateService {
            image "https://dl.dropboxusercontent.com/scl/fi/n5md50yihf6kjmuqhwtb9/TelemetryUpdateServicePort.png?rlkey=p9m82r96eh04qia7byizz441e&st=ciuqwkem&dl=0"
            title "Detailed Diagram class for Telemetry Update Service"
        }
        
        image terminal_system.inspection.VideoUpdateService {
            image "https://dl.dropboxusercontent.com/scl/fi/cifh4vh0rzl0cacyp6sxu/VideoUpdateServicePort.png?rlkey=jdaaglao8t9awvdkgeme7wvsd&st=sulxa4sj&dl=0"
            title "Detailed Diagram class for Video Update Service"
        }
        
        image terminal_system.inspection.SessionServices {
            image "https://dl.dropboxusercontent.com/scl/fi/9umdqxyeeiq6tqc2grzwe/SessionServicePort.png?rlkey=uivz6rp4of3icwonadzbicuad&st=eu25fn5f&dl=0"
            title "Detailed Diagram class for Session Update Service"
        }
        
        image terminal_system.inspection.PanelUpdateServices {
            image "https://dl.dropboxusercontent.com/scl/fi/7kosxmo6z7jc5x31quv18/PanelUpdateServicePort.png?rlkey=odvyud46qxwjh9p3lgcua0n3t&st=qph1ez2n&dl=0"
            title "Detailed Diagram class for Panel Update Service"
        }
        
        #=================================== Adding an image associated with Video===============================================================================
        
        image terminal_system.video.SessionServices {
            image "https://dl.dropboxusercontent.com/scl/fi/zki2x58brfwm327sozz6d/SessionServicePort.png?rlkey=sxy4jbvjrrejphptrkikiiq6p&st=fwpatcfa&dl=0"
            title "Detailed Diagram class for Session Service"
        }
        
        image terminal_system.video.VideoServices {
            image "https://dl.dropboxusercontent.com/scl/fi/x0gpcmtc7dsm5isc9s3yr/VideoServicePort.png?rlkey=b7gmnl7nfc9hjnep48vrs421o&st=9empwzj2&dl=0"
            title "Detailed Diagram class for Video Service"
        }
        
        
         #=================================== Adding an image associated with Panel And Feeder===============================================================================
        image terminal_system.panel_feeder.panelServices {
            image "https://dl.dropboxusercontent.com/scl/fi/6wlpwj6wq7ispro6zqwgk/Panel_and_feder.png?rlkey=idoi1dvwbdzeq2qrqnah0q0a1&st=s3mgehrh&dl=0"
            title "Detailed Diagram class for Panel Service"
        }

        image terminal_system.panel_feeder.feederServices {
            image "https://dl.dropboxusercontent.com/scl/fi/6wlpwj6wq7ispro6zqwgk/Panel_and_feder.png?rlkey=idoi1dvwbdzeq2qrqnah0q0a1&st=s3mgehrh&dl=0"
            title "Detailed Diagram class for Feeder Service"
        }


        styles {
            element "Person" {
                background "#08427B"
                color "#ffffff"
                shape "Person"
            }
            element "Software System" {
                background "#1168BD"
                color "#ffffff"
            }
            element "Container" {
                background "#438DD5"
                color "#ffffff"
            }
            element "Component" {
                background "#85BBF0"
                color "#000000"
                fontSize 12
                shape "RoundedBox"
            }
            element "Database" {
                shape "Cylinder"
                background "#F1C232"
                color "#000000"
            }
            element "Existing System" {
                background "#999999"
                color "#ffffff"
            }
        }
    }
}
