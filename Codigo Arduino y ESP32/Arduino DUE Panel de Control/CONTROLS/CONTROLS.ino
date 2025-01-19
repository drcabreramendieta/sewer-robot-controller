/**
 * @file CONTROLS.ino
 * @brief Control panel firmware for robot inspection system
 * @details Handles encoder readings, robot movement, camera control and feeder operations
 * @author IIoT Inspection System Team
 */
//Señales del encoder
#define encoderPinA 2
#define encoderPinB 3
#define ResetButton 5

//Señales de joysticks del robot
#define Backward 13
#define Left 12
#define Right 11
#define Forward 10

//Señales del joystick de la camara
#define TiltUp 6
#define TiltDown 9
#define PanLeft 8
#define PanRight 7

//Señales de focus in y focus out
#define FocusIn 36
#define FocusOut 40

//Potenciómetro para control de iluminación
#define Light A1

//Señal de fin carrera del feeder
#define FeederButton 4

//Variables para función de envío de mensajes del encoder
bool resetMessageSent = false;
unsigned long lastPrintTime = 0;
const unsigned long printInterval = 1000;

//Variables para procesamiento de señal del encoder
volatile long pulseCount = 0;
int encoderStateB;

//Variables para procesamiento de señal de reset encoder
unsigned long resetDebounceDelay = 50;
unsigned long lastResetDebounceTime = 0;


//Variables para procesamiento de señales de joystick de robot
unsigned long debounceDelay_direction = 50;
unsigned long lastDebounceTime_direction = 0;
int lastResetState = LOW;
int prevBackwardState = HIGH;
int prevLeftState = HIGH;
int prevRightState = HIGH;
int prevForwardState = HIGH;
int prevtiltdownState = HIGH;
int prevtiltupState = HIGH;
int prevpanleftState = HIGH;
int prevpanrightState = HIGH;
int prevFocusOutState = HIGH;
int prevFocusInState = HIGH;

//Variables para procesamiento de señales del joystick de la cámara e iluminación
int prevScaledLightValue = 0;
int lastCameraCommand = 0;
bool cameraStateChanged = false;
bool lightStateChanged = false;
bool focusStateChanged = false;
unsigned long debounceDelay_camera = 50;
unsigned long lastDebounceTime_camera = 0;


//Variables para feeder control
int lastFeederState = LOW;
unsigned long resetDebounceDelayFeeder = 50;
unsigned long lastResetDebounceTimeFeeder = 0;
bool resetMessageSentFeeder = false;
int RobotCommand = 0;
String RobotMessage = "Empty";
String FocusMessage = "Empty";
/**
 * @brief Initial setup configuration
 * @details Configures pin modes, interrupts and serial communication
 */
void setup() {
  //Definición de entradas
  pinMode(encoderPinA, INPUT_PULLUP);
  pinMode(encoderPinB, INPUT_PULLUP);
  pinMode(Backward, INPUT_PULLUP);
  pinMode(Left, INPUT_PULLUP);
  pinMode(Right, INPUT_PULLUP);
  pinMode(Forward, INPUT_PULLUP);
  pinMode(TiltDown, INPUT_PULLUP);
  pinMode(TiltUp, INPUT_PULLUP);
  pinMode(PanLeft, INPUT_PULLUP);
  pinMode(PanRight, INPUT_PULLUP);
  pinMode(ResetButton, INPUT_PULLUP);
  pinMode(FeederButton, INPUT_PULLUP);
  pinMode(FocusIn, INPUT_PULLUP);
  pinMode(FocusOut, INPUT_PULLUP);

  //Valor inicial de referencia para el canal B del encoder
  encoderStateB = digitalRead(encoderPinB);

  //Interrupción evento RISING canal A encoder
  attachInterrupt(digitalPinToInterrupt(encoderPinA), handleEncoder, RISING);

  //Comunicación serial con el panel (Programa Python)
  Serial.begin(115200);

  //Comunicación motores NEMA
  Serial1.begin(9600);
}
/**
 * @brief Main program loop
 * @details Handles robot control, camera control and feeder operations
 */
void loop() {
  //printPulseCount();
  handleRobotControl();
  handleCameraAndLightControl();
  //checkResetButton();
  //readSerialMessages();
  //motorFeeder();
}

//Función interrupción para procesamiento de señal encoder
/**
 * @brief Encoder interrupt handler
 * @details Increments/decrements pulse count based on encoder state
 */
void handleEncoder() {
  int currentEncoderStateB = digitalRead(encoderPinB);
  if (currentEncoderStateB == HIGH) {
    pulseCount++;
  } else {
    pulseCount--;
  }
}

//Función para procesamiento señal de joystick robot
/**
 * @brief Process robot joystick controls
 * @details Reads joystick inputs and sends movement commands
 */  
void handleRobotControl() {
  int backwardState = digitalRead(Backward);
  int leftState = digitalRead(Left);
  int rightState = digitalRead(Right);
  int forwardState = digitalRead(Forward);


  if (millis() - lastDebounceTime_direction > debounceDelay_direction) {
    lastDebounceTime_direction = millis();


    if (backwardState != prevBackwardState || leftState != prevLeftState || rightState != prevRightState || forwardState != prevForwardState) {
      prevBackwardState = backwardState;
      prevLeftState = leftState;
      prevRightState = rightState;
      prevForwardState = forwardState;


      if (backwardState == LOW && leftState == HIGH && rightState == HIGH) {
        Serial.println("robot B");
        RobotCommand = 1;
      } else if (backwardState == LOW && leftState == LOW && rightState == HIGH) {
        Serial.println("robot BL");
        RobotCommand = 2;
      } else if (backwardState == LOW && leftState == HIGH && rightState == LOW) {
        Serial.println("robot BR");
        RobotCommand = 3;
      } else if (forwardState == LOW && leftState == HIGH && rightState == HIGH) {
        Serial.println("robot F");
        RobotCommand = 4;
      } else if (forwardState == LOW && leftState == LOW && rightState == HIGH) {
        Serial.println("robot FL");
        RobotCommand = 5;
      } else if (forwardState == LOW && leftState == HIGH && rightState == LOW) {
        Serial.println("robot FR");
        RobotCommand = 6;
      } else if (forwardState == HIGH && backwardState == HIGH && leftState == HIGH && rightState == HIGH) {
        Serial.println("robot STOP");
        RobotCommand = 0;
      }
    }
  }
}

//Función de procesamiento señal de cámara e iluminación
/**
 * @brief Process camera and light controls
 * @details Handles camera movement, focus and light intensity
 */
void handleCameraAndLightControl() {
  int panleftState = digitalRead(PanLeft);
  int panrightState = digitalRead(PanRight);
  int tiltdownState = digitalRead(TiltDown);
  int tiltupState = digitalRead(TiltUp);
  int FocusInState = digitalRead(FocusIn);
  int FocusOutState = digitalRead(FocusOut);
  int LightValue = analogRead(Light);
  int scaledLightValue = map(LightValue, 0, 1023, 100, 0);


  if (millis() - lastDebounceTime_camera > debounceDelay_camera) {
    lastDebounceTime_camera = millis();

    if (tiltdownState != prevtiltdownState || tiltupState != prevtiltupState || panleftState != prevpanleftState || panrightState != prevpanrightState) {
      prevtiltdownState = tiltdownState;
      prevtiltupState = tiltupState;
      prevpanleftState = panleftState;
      prevpanrightState = panrightState;
      cameraStateChanged = true;

      int newCameraCommand;
      if (tiltdownState == LOW && panleftState == HIGH && panrightState == HIGH) {
        newCameraCommand = 1;  // TD
      } else if (tiltupState == LOW && panleftState == HIGH && panrightState == HIGH) {
        newCameraCommand = 2;  // TU
      } else if (panleftState == LOW && tiltdownState == HIGH && tiltupState == HIGH) {
        newCameraCommand = 3;  // PL
      } else if (panrightState == LOW && tiltdownState == HIGH && tiltupState == HIGH) {
        newCameraCommand = 4;  // PR
      } else {
        newCameraCommand = 5;  // STOP
      }

      if (newCameraCommand != lastCameraCommand) {
        lastCameraCommand = newCameraCommand;
      } else {
        cameraStateChanged = false;
      }
    }

    if (FocusInState != prevFocusInState || FocusOutState != prevFocusOutState) {
      prevFocusInState = FocusInState;
      prevFocusOutState = FocusOutState;
      focusStateChanged = true;
      if (FocusInState == LOW) {
        FocusMessage = "IN";
      } else if (FocusOutState == LOW) {
        FocusMessage = "OUT";
      } else if (FocusInState == HIGH || FocusOutState == HIGH) {
        FocusMessage = "NONE";
      }
    }
  }


  if (abs(scaledLightValue - prevScaledLightValue) > 11) {
    prevScaledLightValue = scaledLightValue;
    lightStateChanged = true;
  }



  if (cameraStateChanged || lightStateChanged || focusStateChanged) {
    String message = "camera ";
    switch (lastCameraCommand) {
      case 1: message += "TD "; break;
      case 2: message += "TU "; break;
      case 3: message += "PL "; break;
      case 4: message += "PR "; break;
      case 5: message += "STOP "; break;
      default: message += "STOP ";
    }
    message += String(prevScaledLightValue);
    message += " " + FocusMessage;
    Serial.println(message);


    cameraStateChanged = false;
    lightStateChanged = false;
    focusStateChanged = false;
  }
}

//Función para procesamiento señal de reseteo encoder
/**
 * @brief Handle encoder reset button
 * @details Resets pulse count and sends notification
 */
void checkResetButton() {
  int resetState = digitalRead(ResetButton);
  unsigned long currentTime = millis();

  if (resetState != lastResetState) {
    lastResetDebounceTime = currentTime;
    resetMessageSent = false;
  }


  if ((currentTime - lastResetDebounceTime) > resetDebounceDelay) {

    lastResetState = resetState;


    if (resetState == LOW && !resetMessageSent) {

      if (lastResetState == LOW) {
        pulseCount = 0;
        Serial.println("feeder " + String(pulseCount) + " RESET");
        resetMessageSent = true;
      }
    }
  }
}


//Función para enviar por serial información de encoder
/**
 * @brief Send encoder count over serial
 * @details Periodically sends current pulse count
 */
void printPulseCount() {
  unsigned long currentTime = millis();
  if (currentTime - lastPrintTime >= printInterval) {
    Serial.println("feeder " + String(pulseCount) + " NO");
    lastPrintTime = currentTime;
  }
}


// Función para leer los mensajes entrantes del serial
/**
 * @brief Read incoming serial messages
 * @details Reads incoming messages and processes them
 */
void readSerialMessages() {
  if (Serial.available() > 0) {
    String incomingMessage = Serial.readStringUntil('\n');
    processIncomingMessage(incomingMessage);
  }
}
/**
 * @brief Process incoming serial messages
 * @details Handles commands received from control system
 * @param message Serial command string
 */
void processIncomingMessage(String message) {

  int firstSpace = message.indexOf(' ');
  String command = message.substring(0, firstSpace);
  String parameter = message.substring(firstSpace + 1);


  if (command == "feeder" && parameter == "RESET") {
    pulseCount = 0;
    Serial.println("Encoder reset.");
  }
}
/**
 * @brief Get robot movement state
 * @details Converts command codes to movement strings
 */
void RobotState() {
  if (RobotCommand == 1 || RobotCommand == 2 || RobotCommand == 3) {
    RobotMessage = "Backward";
  } else if (RobotCommand == 4 || RobotCommand == 5 || RobotCommand == 6) {
    RobotMessage = "Forward";
  } else {
    RobotMessage = "Stop";
  }
}
// Función para movimiento de NEMAs
/**
 * @brief Control feeder motor movement
 * @details Handles feeder button input and motor control
 */
void motorFeeder() {
  int feederState = digitalRead(FeederButton);
  unsigned long currentTimeFeeder = millis();

  // Verificar si el estado del botón ha cambiado
  if (feederState != lastFeederState) {
    lastResetDebounceTimeFeeder = currentTimeFeeder;
    resetMessageSentFeeder = false;
  }

  // Verificar el tiempo de rebote (debounce)
  if ((currentTimeFeeder - lastResetDebounceTimeFeeder) > resetDebounceDelayFeeder) {

    // Actualizar el estado anterior del botón
    lastFeederState = !feederState;

    // Verificar si el botón ha sido soltado
    if (feederState == HIGH && !resetMessageSentFeeder) {
      RobotState();
      Serial1.print("STOP " + RobotMessage + "\n");
      Serial.print("STOP " + RobotMessage + "\n");
      resetMessageSentFeeder = true;
    }

    // Verificar si el botón ha sido presionado
    if (feederState == LOW && !resetMessageSentFeeder) {
      RobotState();
      Serial1.print("MOVE " + RobotMessage + "\n");
      Serial.print("MOVE " + RobotMessage + "\n");
      resetMessageSentFeeder = true;
    }
  }
}
