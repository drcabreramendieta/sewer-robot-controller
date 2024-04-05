# Explicación
En el módulo Video se implementó el puerto dvr_link con un mock del adaptador hikvision_dvr_link para las operaciones con el DVR. También se implementó el puerto db_link como interface para el adaptador tiny_db_link para las operaciones con la base de datos TinyDB. Estos elementos interactuan en el caso de uso control_session que es la API que usan otros servicios para controlar las sesiones. 

Concretamente, en el módulo Inspection se implementó un controlador de sesiones (session_controller y gidtec_session_controller) que hace uso de la API mencionada previamente para el control de las sesiones desde la GUI.

# TODO
- Implementar el código del adaptador hikvision_dvr_link para realizar las operaciones en el DVR hikvision.
- Cambiar los botones de login y start record a toggle button para que se actúe ante los eventos pressed and released en vez de la verificación de texto. La implementación actual para el inicio de la grabación ya actúa sobre estos eventos por lo que solamente habría que modificar el tipo de botón. El mismo comportamiento se debe lograr para el login.
- Refactorizar los nombres para que estén auto-documentados. Tomó un tiempo encontrar el objeto del botón recording y capture con los nombres actuales de button1 y button2.
- Refactorizar el código de main_window. En primera instancia se debería usar un archivo por clase definida.

# Notas
- En el archivo containers están 2 líneas comentadas. Esas pueden ser útiles cuando se desea probar sin cámara y sin el robot.