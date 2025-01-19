
/**
 * @file ROBOT_INSPECCION_V8.ino
 * @brief Inspection robot program using CAN and I2C communication.
 *
 * This code manages sensors, motors, and telemetry for an inspection robot.
 * It includes configurations for CAN communication, SPI, and I2C devices.
 *
 * @author Ing.Diego Cabrera Phd.
 * @date YYYY-MM-DD
 * @version 8.0
*/


#include <mcp_can.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"
#include <Wire.h>
#include <MPU9250_asukiaaa.h>


#ifdef _ESP32_HAL_I2C_H_
#define SDA_PIN 21
#define SCL_PIN 22
#endif

/**
 * @brief Timer configuration for message handling.
 */
// Configuración para las interrupciones por tiempo que enviarán los mensajes a los motores y cámara
hw_timer_t *Timer0_Cfg = NULL;
/**
 * @brief Control variable for managing periodic messages.
 */
int control_mensajes = 10;
/**
 * @brief Timer interrupt service routine.
 *
 * This ISR sets the control variable to indicate a new message needs to be processed.
 */
void IRAM_ATTR Timer0_ISR() {
  control_mensajes = 1;
}

/**
 * @brief CAN message variables.
 */
// Variables to manage the Id and buffer of the SPI to CAN communication module
unsigned long rxId; ///< ID of the received CAN message.
byte len;           ///< Length of the CAN message.
byte rxBuf[8];      ///< Buffer to store received CAN message data.
/**
 * @brief Serial output buffer.
 */
// Array to store serial string that is shown in the monitor serial
char msgString[128];///< Buffer to store strings for serial output.
/**
 * @brief Camera control commands.
 */
// Arrays to store the message which is sent to control the camera movements and light
byte camera_control[] = { 0xaa, 0x01, 0xaa, 0x02, 0xaa, 0x03, 0xaa, 0x04, 0xbb, 0x2a };
char camera_init[] = { 0xaa, 0x77 };
/**
 * @brief UART configuration for RS485 communication.
 */
// Configuration of the serial port which is used by the TTL to RS485 communication module
#define RXD1 16  //RX to UART
#define TXD1 17  //TX to UART
/**
 * @brief Motor speed variables.
 */
// Variables to define the speed of the wheels modules
int left_speed = 0;         ///< Speed of the left wheels.
int right_speed = 0;        ///< Speed of the right wheels.
int nominal_speed = 1000;   ///< Maximum nominal speed.
int received_speed;         ///< Speed set by the user in the panel.
uint8_t speed_left_data0;   ///< To store the HEX value of the left speed byte1
uint8_t speed_left_data1;   ///< To store the HEX value of the left speed byte2
uint8_t speed_right_data0;  ///< To store the HEX value of the right speed byte1
uint8_t speed_right_data1;  ///< To store the HEX value of the right speed byte2
byte m_left[8];             ///< To store message left module
byte m_right[8];            ///< To store message right module
/**
 * @brief Motor telemetry variables.
 */
//Variables to send motor data to control panel
uint16_t revolution_counter1; ///< Revolution counter for motor .
uint16_t angular_position1;   ///< Angular position for motor .
uint16_t angular_speed1;      ///< Angular speed for motor .
uint16_t current1;            ///< Current draw for motor 1.
byte data1_m1[7];                                                                  ///<To store state of motors
byte data2_m2[] = { 0xaa, 0xaa, 0xaa, 0xaa, 0xaa, 0xaa, 0xaa, 0xaa, 0xaa, 0xaa };  ///< To reset state of motors


//Variables to control the synchronous sending of telemetry data
unsigned long previousMillis = 0;  ///< will store last time LED was updated
int interval = 5000;               ///< interval at which the data will be sent

unsigned long previousMillis1 = 0;  ///< will store last time LED was updated
int interval1 = 15000;              ///< interval at which the data will be sent

//Variables of temperature and humidity data
Adafruit_BME680 bme;
int temperature = 0; ///< Temperature data.
int humidity = 0;    ///< Humidity data.
byte telemetry[8];   ///< Buffer to store telemetry data.

/**
 * @brief Slope calculation variables.
 */
//Variables to calculate the slop and send
MPU9250_asukiaaa mySensor;  ///< MPU9250 sensor object.
float aX, aY, aZ;           ///< Accelerometer readings.
int incl_x;                 ///< Inclination on the X-axis.
int incl_y;                 ///< Inclination on the Y-axis.
unsigned char byte1_incl_x; ///< MSB of X-axis inclination.
unsigned char byte0_incl_x; ///< LSB of X-axis inclination.
unsigned char byte1_incl_y; ///< MSB of Y-axis inclination.
unsigned char byte0_incl_y; ///< LSB of Y-axis inclination.


/**
 * @brief CAN bus configurations.
 */
// Configuration of the CAN buses. CAN0 corresponds to low speed CAN bus, it is used
// to receive the messages from the control panel. CAN1 corresponds to high speed CAN,
// bus, it is used to send the messages to control the motors
MCP_CAN CAN0(5);     ///< CAN0 interface usins CS on digital pin 5
MCP_CAN CAN1(25);    ///< CAN1 interface using CS on digital pin 25
#define CAN0_INT 32  ///< define interrupt pin for CAN0 receive buffer
#define CAN1_INT 33  ///<define interrupt pin for CAN1 receive buffer

/**
 * @brief Initialize system hardware and peripherals
 * @details Configures:
 *          - SPI chip select pins
 *          - Serial communication
 *          - CAN bus interfaces
 *          - Environmental sensors
 *          - Timer interrupts
 */
void setup() {
   /**
   * @brief Configure chip select pins for CAN controllers
   */
  //CS pines configuration
  digitalWrite(5, HIGH);  // CAN0 CS pin
  pinMode(5, OUTPUT);
  digitalWrite(25, HIGH); // CAN1 CS pin 
  pinMode(25, OUTPUT);


  /**
   * @brief Initialize serial communication
   * @details Serial: Debug monitor at 115200 baud
   *          Serial1: RS485 communication at 9600 baud
   */

  // Start serial communication, Serial corresponds to Serial Monitor of Arduino. Serial1
  // corresponds to the serial port used by TTL to RS485 communication module
  Serial.begin(115200);
  Serial1.begin(9600, SERIAL_8N1, RXD1, TXD1);
  /**
   * @brief Configure CAN bus interrupt pins
   */
  // Declaration of the interrupt pines to CAN communication
  pinMode(CAN0_INT, INPUT_PULLUP);
  pinMode(CAN1_INT, INPUT_PULLUP);

  /**
   * @brief Initialize CAN0 (250kbps) for control panel communication
   */

  // Init CAN0 bus, baudrate: 250k@8MHz

  if (CAN0.begin(MCP_ANY, CAN_250KBPS, MCP_8MHZ) == CAN_OK) {
    Serial.print("CAN0: Init OK!\r\n");
    CAN0.setMode(MCP_NORMAL);
  } else Serial.print("CAN0: Init Fail!!!\r\n");
  /**
   * @brief Initialize CAN1 (1Mbps) for motor control
   */
  // Init CAN1 bus, baudrate: 1000k@8MHz
  if (CAN1.begin(MCP_ANY, CAN_1000KBPS, MCP_8MHZ) == CAN_OK) {
    Serial.print("CAN1: Init OK!\r\n");
    CAN1.setMode(MCP_NORMAL);
  } else Serial.print("CAN1: Init Fail!!!\r\n");
    /**
   * @brief Initialize BME680 environmental sensor
   */
  // Initializate the bme680 sensor
  if (!bme.begin()) {
    Serial.println("Could not find BME680? Check wiring");
  } else {
    Serial.println("BME680 found");
  }
  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);
  bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
  /**
   * @brief Initialize MPU9250 motion sensor
   */
// Initializate the LSM6DS3 sensor
#ifdef _ESP32_HAL_I2C_H_  // For ESP32
  Wire.begin(SDA_PIN, SCL_PIN);
  mySensor.setWire(&Wire);
#endif

  mySensor.beginAccel();

  /**
   * @brief Configure timer interrupt for message handling
   * @details 1MHz timer with ISR for message control
   */
  //Timer message
  Timer0_Cfg = timerBegin(0, 80, true);
  timerAttachInterrupt(Timer0_Cfg, &Timer0_ISR, true);
  timerAlarmWrite(Timer0_Cfg, 1000000, true);
  timerAlarmEnable(Timer0_Cfg);

  /**
   * @brief Initialize telemetry status
   */
  telemetry[6] = 0xC0;
}

void loop() {
    /**
     * @brief Main loop that handles CAN message processing, motor control, camera configuration, and telemetry transmission.
     * 
     * @details This function continuously checks for incoming CAN messages, decodes them, and performs
     * specific actions based on the message ID and data. It also sends periodic telemetry data based on
     * sensor readings and time intervals.
     */
  // Check if there is a CAN0 interrupt signal  
  // If interrupt pin is low, read CAN0 receive buffer
  if (!digitalRead(CAN0_INT)) {
    Serial.println("CAN0 receive message:");
    // Read the CAN message
    // Read data: len = data length, buf = data byte(s)
    CAN0.readMsgBuf(&rxId, &len, rxBuf);

    // Determine if ID is standard (11 bits) or extended (29 bits)
    if ((rxId & 0x80000000) == 0x80000000)
      sprintf(msgString, "Extended ID: 0x%.8lX  DLC: %1d  Data:", (rxId & 0x1FFFFFFF), len);
    else
      sprintf(msgString, "Standard ID: 0x%.3lX       DLC: %1d  Data:", rxId, len);

    Serial.print(msgString);
    // Check if the message is a remote request frame
    if ((rxId & 0x40000000) == 0x40000000) {  // Determine if message is a remote request frame.
      sprintf(msgString, " REMOTE REQUEST FRAME");
      Serial.print(msgString);
    } else {
      for (byte i = 0; i < len; i++) {
        sprintf(msgString, " 0x%.2X", rxBuf[i]);
        Serial.print(msgString);
      }
    }
    Serial.println();


     // Handle motor control messages
    // Verify if the received message is to control the motors speed
    if (rxId == 0x0001) {
      //Get the porcentual speed to the wheels modules setted by the user
      received_speed = (rxBuf[2]);
      Serial.println(received_speed);

      //Define the direction, rotation and speed to the robot.
      if (rxBuf[0] == 0x01) {    // Forward direction
        if (rxBuf[1] == 0x00) {  // Neutral rotation
          left_speed = -(nominal_speed * (received_speed / 100.0));
          right_speed = (nominal_speed * (received_speed / 100.0));
        } else if (rxBuf[1] == 0x01) {  // Left rotation
          left_speed = -0.9 * ((nominal_speed * (received_speed / 100.0)));
          right_speed = (nominal_speed * (received_speed / 100.0));
        } else if (rxBuf[1] == 0x02) {  // Right rotation
          left_speed = -(nominal_speed * (received_speed / 100.0));
          right_speed = 0.9 * ((nominal_speed * (received_speed / 100.0)));
        }
      } else if (rxBuf[0] == 0x02) {  // Backward direction
        if (rxBuf[1] == 0x00) {       // Neutral rotation
          left_speed = (nominal_speed * (received_speed / 100.0));
          right_speed = -(nominal_speed * (received_speed / 100.0));
        } else if (rxBuf[1] == 0x01) {  // Left rotation
          left_speed = 0.9 * ((nominal_speed * (received_speed / 100.0)));
          right_speed = -(nominal_speed * (received_speed / 100.0));
        } else if (rxBuf[1] == 0x02) {  // Right rotation
          left_speed = (nominal_speed * (received_speed / 100.0));
          right_speed = -0.9 * ((nominal_speed * (received_speed / 100.0)));
        }
      } else if (rxBuf[0] == 0x00) {  //Stop
        left_speed = 0;
        right_speed = 0;
        Serial.println("Stop");
      }
      Serial.print("Velocidades calculadas:");
      Serial.print(left_speed);
      Serial.print(", ");
      Serial.println(right_speed);
      //Convert left and right speed to 2 bytes HEX values
      speed_left_data0 = (((left_speed >> 8) & 0xFF));
      speed_left_data1 = (left_speed & 0xFF);
      speed_right_data0 = ((right_speed >> 8) & 0xFF);
      speed_right_data1 = (right_speed & 0xFF);
      // Set the message data to each wheels module
      m_left[0] = speed_left_data0;
      m_left[1] = speed_left_data1;
      m_left[2] = speed_left_data0;
      m_left[3] = speed_left_data1;
      m_left[4] = speed_left_data0;
      m_left[5] = speed_left_data1;
      m_left[6] = 0;
      m_left[7] = 0;
      m_right[0] = speed_right_data0;
      m_right[1] = speed_right_data1;
      m_right[2] = speed_right_data0;
      m_right[3] = speed_right_data1;
      m_right[4] = speed_right_data0;
      m_right[5] = speed_right_data1;
      m_right[6] = 0;
      m_right[7] = 0;

      CAN1.sendMsgBuf(0x202, 0, sizeof(m_left), m_left);
      CAN1.sendMsgBuf(0x203, 0, sizeof(m_right), m_right);
    }
    //Verify if the message is to the camera
    //Configuration message
    if (rxId == 0x0002) {
      if (rxBuf[0] == 0x77) {
        Serial.println("Rotation Reset");
        camera_init[1] = 0x77;
        Serial1.write(camera_init, sizeof(camera_init));
        Serial.println(sizeof(camera_init));
        for (int i = 0; i < sizeof(camera_init); i++) {
          Serial.print(camera_init[i], HEX);
          Serial.print(" ");
        }
        Serial.println();
      }
      if (rxBuf[1] == 0x74) {
        Serial.println("Focus Reset");
        camera_init[1] = 0x74;
        Serial1.print(camera_init);
        for (int i = 0; i < sizeof(camera_init); i++) {
          Serial.print(camera_init[i], HEX);
          Serial.print(" ");
        }
        Serial.println();
      }
    }
    //Operational message
    if (rxId == 0x0003) {
      if (rxBuf[0] == 0x94) {
        Serial.println("Focus Out");
        camera_control[7] = 0x94;
      } else if (rxBuf[0] == 0x91) {
        Serial.println("Focus In");
        camera_control[7] = 0x91;
      } else if (rxBuf[0] == 0x04) {
        Serial.println("Stop Focus");
        camera_control[7] = 0x04;
      }

      if (rxBuf[1] == 0x44) {
        Serial.println("Pan Right");
        camera_control[3] = 0x44;
      } else if (rxBuf[1] == 0x33) {
        Serial.println("Pan Left");
        camera_control[3] = 0x33;
      } else if (rxBuf[1] == 0x02) {
        Serial.println("Stop Pan");
        camera_control[3] = 0x02;
      }

      if (rxBuf[2] == 0x11) {
        Serial.println("Tilt Up");
        camera_control[1] = 0x11;
      } else if (rxBuf[2] == 0x22) {
        Serial.println("Tilt Down");
        camera_control[1] = 0x22;
      } else if (rxBuf[2] == 0x01) {
        Serial.println("Stop Tilt");
        camera_control[1] = 0x01;
      }

      if (rxBuf[3] == 0x2a) {
        Serial.println("0% - 11%");
        camera_control[9] = 0x2a;
      } else if (rxBuf[3] == 0x3a) {
        Serial.println("11% - 22%");
        camera_control[9] = 0x3a;
      } else if (rxBuf[3] == 0x4a) {
        Serial.println("22% - 33%");
        camera_control[9] = 0x4a;
      } else if (rxBuf[3] == 0x5a) {
        Serial.println("33% - 44%");
        camera_control[9] = 0x5a;
      } else if (rxBuf[3] == 0x6a) {
        Serial.println("44% - 55%");
        camera_control[9] = 0x6a;
      } else if (rxBuf[3] == 0x9a) {
        Serial.println("55% - 66%");
        camera_control[9] = 0x9a;
      } else if (rxBuf[3] == 0x5b) {
        Serial.println("66% - 77%");
        camera_control[9] = 0x5b;
      } else if (rxBuf[3] == 0x9b) {
        Serial.println("77% - 88%");
        camera_control[9] = 0x9b;
      } else if (rxBuf[3] == 0x6c) {
        Serial.println("88% - 100%");
        camera_control[9] = 0x6c;
      }

      Serial1.write(camera_control, sizeof(camera_control));
    }
  }


  // Send message to wheels modules
  if (control_mensajes == 1 || !digitalRead(CAN0_INT) == 1) {

    CAN1.sendMsgBuf(0x202, 0, sizeof(m_left), m_left);
    CAN1.sendMsgBuf(0x203, 0, sizeof(m_right), m_right);
    Serial.println("Mensaje para motores.");
    for (int i = 0; i < sizeof(m_left); i++) {
      Serial.print(m_left[i], HEX);
      Serial.print(" ");
    }
    Serial.println();
    for (int i = 0; i < sizeof(m_right); i++) {
      Serial.print(m_right[i], HEX);
      Serial.print(" ");
    }
    Serial.println();

    Serial1.write(camera_control, sizeof(camera_control));
    Serial.println("Mensaje para cámara.");
    for (int i = 0; i < sizeof(camera_control); i++) {
      Serial.print(camera_control[i], HEX);
      Serial.print(" ");
    }
    Serial.println();
    
  }

  //Take the actual time in order to know if the robot telemetry data must be sent
  unsigned long currentMillis = millis();


  //Send motor telemetry data
  if (!digitalRead(CAN1_INT) || control_mensajes == 1 ) {           // If interrupt pin is low, read CAN1 receive buffer
    CAN1.readMsgBuf(&rxId, &len, rxBuf);  // Read data: len = data length, buf = data byte(s)
    switch (rxId) {
      case 0x209:
        data1_m1[0] = rxBuf[2];
        break;
      case 0x20B:
        data1_m1[1] = rxBuf[2];
        break;
      case 0x20D:
        data1_m1[2] = rxBuf[2];
        break;
      case 0x20F:
        data1_m1[3] = rxBuf[2];
        break;
      case 0x211:
        data1_m1[4] = rxBuf[2];
        break;
      case 0x213:
        data1_m1[5] = rxBuf[2];
        break;
      case 0x215:
        data1_m1[6] = rxBuf[2];
        break;
      default:
        break;
    }
    for (int i = 0; i < sizeof(data1_m1); i++) {
      if (data1_m1[i] == 0xE0) {
        telemetry[6] = 0xE0;
      }
    }
    if (currentMillis - previousMillis >= interval) {
      // save the last time data were sent
      previousMillis = currentMillis;
      // Events for telemetry data: Humidity and Temperature
      if (!bme.performReading()) {
        Serial.println("Failed to perform reading :(");
        return;
      }
      temperature = round(bme.temperature);
      humidity = round(bme.humidity);
      telemetry[0] = temperature;
      telemetry[1] = humidity;
      byte1_incl_x = 0;
      byte1_incl_y = 0;

      // Events for telemetry data: Slop
      mySensor.accelUpdate();
      aX = mySensor.accelX();
      aY = mySensor.accelY();
      aZ = mySensor.accelZ();
      incl_x = abs(round(atan(aX / sqrt(pow(aY, 2) + pow(aZ, 2))) * (180.0 / 3.14)) + 86);
      incl_y = abs(round(atan(aY / sqrt(pow(aX, 2) + pow(aZ, 2))) * (180.0 / 3.14)));
      byte1_incl_x = (incl_x >> 8) & 0xFF;  // Upper bit of slope value in x
      byte0_incl_x = incl_x & 0xFF;         // Lower bit of slope value in x
      byte1_incl_y = (incl_y >> 8) & 0xFF;  // Upper bit of slope value in y
      byte0_incl_y = incl_y & 0xFF;         // Lower bit of slope value in y
      telemetry[2] = byte1_incl_x;
      telemetry[3] = byte0_incl_x;
      telemetry[4] = byte1_incl_y;
      telemetry[5] = byte0_incl_y;

      CAN0.sendMsgBuf(0x400, 0, sizeof(telemetry), telemetry);

      Serial.println("Telemetría:");
      for (int i = 0; i < sizeof(telemetry); i++) {
        Serial.print(telemetry[i], HEX);
        Serial.print(" ");
      }
      Serial.println();
    }
    control_mensajes = 0;
    if (currentMillis - previousMillis1 >= interval1) {
      // save the last time data were sent
      previousMillis1 = currentMillis;
      telemetry[6] = 0xC0;
      if (data1_m1[0] == 0xE0) {
        data2_m2[0] = 0x00;
        CAN1.sendMsgBuf(0x300, 0, sizeof(data2_m2), data2_m2);
        data2_m2[0] = 0xaa;
      }
      if (data1_m1[1] == 0xE0) {
        data2_m2[1] = 0x00;
        CAN1.sendMsgBuf(0x300, 0, sizeof(data2_m2), data2_m2);
        data2_m2[1] = 0xaa;
      }
      if (data1_m1[2] == 0xE0) {
        data2_m2[2] = 0x00;
        CAN1.sendMsgBuf(0x300, 0, sizeof(data2_m2), data2_m2);
        data2_m2[2] = 0xaa;
      }
      if (data1_m1[3] == 0xE0) {
        data2_m2[3] = 0x00;
        CAN1.sendMsgBuf(0x300, 0, sizeof(data2_m2), data2_m2);
        data2_m2[3] = 0xaa;
      }
      if (data1_m1[4] == 0xE0) {
        data2_m2[4] = 0x00;
        CAN1.sendMsgBuf(0x300, 0, sizeof(data2_m2), data2_m2);
        data2_m2[4] = 0xaa;
      }
      if (data1_m1[5] == 0xE0) {
        data2_m2[5] = 0x00;
        CAN1.sendMsgBuf(0x300, 0, sizeof(data2_m2), data2_m2);
        data2_m2[5] = 0xaa;
      }
      if (data1_m1[6] == 0xE0) {
        data2_m2[6] = 0x00;
        CAN1.sendMsgBuf(0x300, 0, sizeof(data2_m2), data2_m2);
        data2_m2[6] = 0xaa;
      }
      if (data1_m1[7] == 0xE0) {
        data2_m2[7] = 0x00;
        CAN1.sendMsgBuf(0x300, 0, sizeof(data2_m2), data2_m2);
        data2_m2[7] = 0xaa;
      }
    }
  }
}

/*********************************************************************************************************
  END FILE
*********************************************************************************************************/
