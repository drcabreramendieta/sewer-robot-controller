# Explicación
En el módulo Video se implementó el puerto dvr_link con un mock del adaptador hikvision_dvr_link para las operaciones con el DVR. También se implementó el puerto db_link como interface para el adaptador tiny_db_link para las operaciones con la base de datos TinyDB. Estos elementos interactuan en el caso de uso control_session que es la API que usan otros servicios para controlar las sesiones. 

Concretamente, en el módulo Inspection se implementó un controlador de sesiones (session_controller y gidtec_session_controller) que hace uso de la API mencionada previamente para el control de las sesiones desde la GUI. Las operaciones y la lógica implementada son las siguientes:
1. Cuando se inicia una sesión, luego de escribir el nombre se pide a la API que cree una sesión en la base de datos. Si la sesión no existe se crea la instancia en la base y se indica al controlador en la GUI que prosiga con la activación de los botones, caso contrario si se detecta la existencia del mismo nombre de sesión no se crea la instancia y se notifica de este problema al controlador en la GUI para actual en consecuencia.
2. Luego de tener una sesión iniciada, el usuario puede presionar el boton de captura de imagen. En este caso, el controlador envía esta acción a la API donde se realizará una captura mediante el dvr_link y se almacenarán los datos de la captura en la base de datos mediante db_link.
3. Cuando se presiona el botón de inicio de grabación solamente cambia el estado de la sesión en la base de datos a recording==True y se pide al DVR que empiece a grabar. Luego que se presiona finalizar grabación, la información de la grabación se almacenará en la base de datos y se pedirá al DVR que termine la grabación.

# TODO
- Implementar el código del adaptador hikvision_dvr_link para realizar las operaciones en el DVR hikvision.
- Modificar si es necesario los campos de ImageInfo y RecordInfo para almacenar la información suficiente para poder luego recuperar las imágenes y videos grabados.
- Cambiar los botones de login y start record a toggle button para que se actúe ante los eventos pressed and released en vez de la verificación de texto. La implementación actual para el inicio de la grabación ya actúa sobre estos eventos por lo que solamente habría que modificar el tipo de botón. El mismo comportamiento se debe lograr para el login.
- Refactorizar los nombres para que estén auto-documentados. Tomó un tiempo encontrar el objeto del botón recording y capture con los nombres actuales de button1 y button2.
- Refactorizar el código de main_window. En primera instancia se debería usar un archivo por clase definida.

# Notas
- En el archivo containers están 2 líneas comentadas. Esas pueden ser útiles cuando se desea probar sin cámara y sin el robot.