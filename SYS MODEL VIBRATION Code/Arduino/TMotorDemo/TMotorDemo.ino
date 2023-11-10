// demo: CAN-BUS Shield, send data
// demo: CAN-BUS Shield, receive data with check mode
// loovee@seeed.cc

//#include <Servo.h>

#include <SPI.h>
#define CAN_2515

// Set SPI CS Pin according to your hardware

#if defined(SEEED_WIO_TERMINAL) && defined(CAN_2518FD)
// For Wio Terminal w/ MCP2518FD RPi Hat：
// Channel 0 SPI_CS Pin: BCM 8
// Channel 1 SPI_CS Pin: BCM 7
// Interupt Pin: BCM25
const int SPI_CS_PIN  = BCM8;
const int CAN_INT_PIN = BCM25;
#else

// For Arduino MCP2515 Hat:
// the cs pin of the version after v1.1 is default to D9
// v0.9b and v1.0 is default D10
const int SPI_CS_PIN = 9;
const int CAN_INT_PIN = 2;
#endif

#ifdef CAN_2515
#include "mcp2515_can.h"
mcp2515_can CAN(SPI_CS_PIN); // Set CS pin
#endif

// Motor Limits
#define P_MIN -12.5f
#define P_MAX 12.5f
#define V_MIN1 -20.94f  // AK70-10 24V
#define V_MAX1 20.94f
#define T_MIN1 -24.8f   // AK70-10
#define T_MAX1 24.8f
#define I_MIN1 -26.1f   // AK70-10
#define I_MAX1 26.1f
#define KP_MIN 0.0f
#define KP_MAX 500.0f
#define KD_MIN 0.0f
#define KD_MAX 5.0f
#define MAP1 2.0f

float p_des = 0.0;     // AK70-10
float v_des = 0.0;
float t_ff = 0.0;
float kp = 3; // Spring
float kd = 0; // Damping

float p = 0.0;

float tout = 0.0;
unsigned long dT;
unsigned long timeold;          // Variable for point time in the last cycle

// CAN to T Motor
unsigned char stmp[8] = {0, 0, 0, 0, 0, 0, 0, 0};
byte MotorModeEnt[8] = {0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFC};
byte MotorModeExt[8] = {0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFD};
byte MotorSetZero[8] = {0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFE};


void setup() {
    SERIAL_PORT_MONITOR.begin(115200);
    //while(!Serial){};
    //while (!SERIAL_PORT_MONITOR) {}

    while (CAN_OK != CAN.begin(CAN_1000KBPS)) {             // init can bus : baudrate = 500k
        SERIAL_PORT_MONITOR.println("CAN init fail, retry...");
        delay(100);
    }
    SERIAL_PORT_MONITOR.println("CAN init ok!");

    CAN.sendMsgBuf(0x01, 0, 8, MotorModeEnt);
    CAN.sendMsgBuf(0x01, 0, 8, MotorSetZero);  
    delay(1000);

    pack_cmd();
    p = read_data();
    delay(1000);
   
}

void loop() {
    
    dT = millis()-timeold;   
    tout = tout + (0.001f*dT);
    timeold = millis();
    SERIAL_PORT_MONITOR.print("\n");
    SERIAL_PORT_MONITOR.print(tout);
    SERIAL_PORT_MONITOR.print("\t");
 
    pack_cmd();
    p = read_data();
    delay(100);
    
    // CAN.sendMsgBuf(0x01, 0, 8, MotorModeExt);
}

void pack_cmd() {
  unsigned int p_int = float_to_uint(p_des,P_MIN,P_MAX,16);  
  unsigned int v_int = float_to_uint(v_des,V_MIN1,V_MAX1,12);
  unsigned int t_int = float_to_uint(t_ff,T_MIN1,T_MAX1,12);
  unsigned int kp_int = float_to_uint(kp,KP_MIN,KP_MAX,12);
  unsigned int kd_int = float_to_uint(kd,KD_MIN,KD_MAX,12);
  byte bufs[8];
  bufs[0] = p_int >> 8;
  bufs[1] = p_int & 0xFF;
  bufs[2] = v_int >> 4;
  bufs[3] = ((v_int & 0xF) << 4) | (kp_int >> 8);
  bufs[4] = kp_int & 0xFF;
  bufs[5] = kd_int >> 4;
  bufs[6] = ((kd_int & 0xF) << 4) | (t_int >> 8);
  bufs[7] = t_int & 0xFF;
  CAN.sendMsgBuf(0x01, 0, 8, bufs);
}

float read_data(){
  unsigned char len = 0;
  unsigned char buf[8];

  if (CAN_MSGAVAIL == CAN.checkReceive()) {         // check if data coming

    CAN.readMsgBuf(&len, buf);    // read data,  len: data length, buf: data buf
        
    //unsigned int canId = CAN.getCanId();
    unsigned int id = buf[0];
    unsigned int p_int2 = (buf[1] << 8) | buf[2];
    unsigned int v_int2 = (buf[3] << 4) | (buf[4] >> 4);
    unsigned int i_int2 = ((buf[4] & 0xF) << 8) | buf[5];

    float p = uint_to_float(p_int2,P_MIN,P_MAX,16);
    SERIAL_PORT_MONITOR.print("0x");
    SERIAL_PORT_MONITOR.print(id, HEX);
    SERIAL_PORT_MONITOR.print("\t");
    SERIAL_PORT_MONITOR.print(p);
    SERIAL_PORT_MONITOR.print("\t");
    
    float v = uint_to_float(v_int2,V_MIN1,V_MAX1,12);
    float i = uint_to_float(i_int2,I_MIN1,I_MAX1,12);
    i = MAP1*i;     // Return Torque (N-m)
    SERIAL_PORT_MONITOR.print(v);
    SERIAL_PORT_MONITOR.print("\t");
    SERIAL_PORT_MONITOR.print(i);
    SERIAL_PORT_MONITOR.print("\t");
    
    return p;
  }
}

unsigned int float_to_uint(float x, float x_min, float x_max, unsigned int bits) {
  //convert a float to an unsigned int, given range and number of bits  ///
  float span = x_max-x_min;
  float offset = x-x_min;
  
  unsigned int pgg = 0;
  if(bits == 12){
    pgg = (unsigned int)((offset/span)*4095.0f);
  }
  if(bits == 16){
    pgg = (unsigned int)((offset/span)*65535.0f);
  }
  return pgg;
}

float uint_to_float(unsigned int x_int, float x_min, float x_max, unsigned int bits) {
  //convert unsingned int to float, given range and number of bits ///
  float span = x_max-x_min;
  float pgg = 0;
  if(bits == 12){
    pgg = (float)(x_int*span/4095.0f) + x_min;
  }
  if(bits == 16){
    pgg = (float)(x_int*span/65535.0f) + x_min;
  }
  return pgg;
}
