#include <Adafruit_GFX_AS.h>
#include <Adafruit_ILI9341_AS.h>
#include <MySignals.h>
#include <MySignals_BLE.h>
#include "Wire.h"
#include "SPI.h" 

//Global variables
char buffer_tft[30]; //TFT display
Adafruit_ILI9341_AS tft = Adafruit_ILI9341_AS(TFT_CS, TFT_DC);
unsigned long previous;
uint8_t valuetemperature[3]; //temperature
int pulsioximeter_state = 0; //state of scensor
uint8_t valueSPO2[5];
int countern = 0;
uint8_t valueMEG[51]; // get 25 scans at one time use 50 byte 1 byte save lable, as BLE limit 54byte transfer
int megcount = 1; // count number of meg value
bool teststart; //start test lable
bool aleart; //get aleart

void setup()
{
	Serial.begin(115200);
	MySignals.begin();
	valuetemperature[0] = 0b00000001; //set temperature lable equal 1
	valueSPO2[0] = 0b00000010; // set SPO2 lable equal 2
	valueMEG[0] = 0b00001000; //set MEG lable equal 8
	MySignals.begin();
	tft.init();
	tft.setRotation(2);
	tft.fillScreen(ILI9341_BLACK);
	tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);

	//TFT message: Welcome 
	tft.drawString("Muscle Fatigue Monitor ", 0, 0, 2);

	Serial.begin(115200);

	MySignals.initSensorUART();

	MySignals.enableSensorUART(BLE);

	//Enable BLE module power -> bit6: 1
	bitSet(MySignals.expanderState, EXP_BLE_POWER);
	MySignals.expanderWrite(MySignals.expanderState);

	//Enable BLE UART flow control -> bit5: 0
	bitClear(MySignals.expanderState, EXP_BLE_FLOW_CONTROL);
	MySignals.expanderWrite(MySignals.expanderState);


	//Disable BLE module power -> bit6: 0
	bitClear(MySignals.expanderState, EXP_BLE_POWER);
	MySignals.expanderWrite(MySignals.expanderState);

	delay(500);

	//Enable BLE module power -> bit6: 1
	bitSet(MySignals.expanderState, EXP_BLE_POWER);
	MySignals.expanderWrite(MySignals.expanderState);
	delay(1000);

	MySignals_BLE.initialize_BLE_values();

	//Clean the input serial buffer
	while (Serial.available() > 0)
	{
		Serial.read();
	}


	if (MySignals_BLE.initModule() == 1)
	{

		if (MySignals_BLE.sayHello() == 1)
		{
			//TFT message: "BLE init ok";
			strcpy_P((char*)buffer_tft, (char*)pgm_read_word(&(table_MISC[1])));
			tft.drawString(buffer_tft, 0, 15, 2);
		}
		else
		{
			//TFT message:"BLE init fail"
			strcpy_P((char*)buffer_tft, (char*)pgm_read_word(&(table_MISC[2])));
			tft.drawString(buffer_tft, 0, 15, 2);


			while (1)
			{
			};
		}
	}
	else
	{
		//TFT message: "BLE init fail"
		strcpy_P((char*)buffer_tft, (char*)pgm_read_word(&(table_MISC[2])));
		tft.drawString(buffer_tft, 0, 15, 2);

		while (1)
		{
		};
	}

}
void loop()
{
	int rawemg;
	int rawtemperature;
	int rawPulse;
	int rawSPO2;
	uint8_t rawemg_low;
	uint8_t rawemg_high;
	uint8_t rawtemp_low;
	uint8_t rawtemp_high;
	uint8_t rawSPO2_low;
	uint8_t rawSPO2_high;
	uint8_t rawPulse_low;
	uint8_t rawPulse_high;
	pulsioximeter_state = MySignals.getPulsioximeterMicro();
	teststart = 1;
	//SET BLE MODE
	while ((MySignals_BLE.ble_mode_flag == master_mode))
	{

		if (MySignals_BLE.setMode(slave_mode) == 0)
		{
			//TFT message:  "Slave mode ok";
			strcpy_P((char*)buffer_tft, (char*)pgm_read_word(&(table_MISC[3])));
			tft.drawString(buffer_tft, 0, 30, 2);


			MySignals_BLE.ble_mode_flag = slave_mode;
		}
		else
		{
			//TFT message:  "Slave mode fail"
			strcpy_P((char*)buffer_tft, (char*)pgm_read_word(&(table_MISC[4])));
			tft.drawString(buffer_tft, 0, 30, 2);


			MySignals_BLE.hardwareReset();
			delay(100);
			MySignals_BLE.initialize_BLE_values();
		}
	}
	// SET BONDABLE MODE
	if (MySignals_BLE.bond_mode_and_mitm == 0)
	{
		if (MySignals_BLE.setBondableMode(BLE_ENABLE_BONDING) == 0)
		{

			//TFT message:  "Bondable mode ok"
			strcpy_P((char*)buffer_tft, (char*)pgm_read_word(&(table_MISC[5])));
			tft.drawString(buffer_tft, 0, 45, 2);



			//3. SET SM PARAMETERS
			if (MySignals_BLE.setSMParameters(BLE_ENABLE_MITM) == 0)
			{
				//TFT message:  "SM parameters ok"
				strcpy_P((char*)buffer_tft, (char*)pgm_read_word(&(table_MISC[7])));
				tft.drawString(buffer_tft, 0, 60, 2);


				MySignals_BLE.bond_mode_and_mitm = 1;

			}
			else
			{
				//TFT message:  "SM parameters fail"
				strcpy_P((char*)buffer_tft, (char*)pgm_read_word(&(table_MISC[8])));
				tft.drawString(buffer_tft, 0, 60, 2);

				MySignals_BLE.hardwareReset();
				delay(100);
				MySignals_BLE.initialize_BLE_values();
			}
		}
		else
		{
			//TFT message:  "Bondable mode fail"
			strcpy_P((char*)buffer_tft, (char*)pgm_read_word(&(table_MISC[6])));
			tft.drawString(buffer_tft, 0, 45, 2);

			MySignals_BLE.hardwareReset();
			delay(100);
			MySignals_BLE.initialize_BLE_values();
		}
	}
	// BONDING AND CONNECTION CONFIGURATION
	if ((MySignals_BLE.ble_mode_flag == slave_mode) && (MySignals_BLE.bonded_and_connected_flag == 0))
	{

		MySignals_BLE.bonding_correct = 0;
		MySignals_BLE.app_connected_flag = 0;
		MySignals_BLE.bonding_fail = 0;

		/////////////////////

		//TFT message:  "Waiting connections..."
		strcpy_P((char*)buffer_tft, (char*)pgm_read_word(&(table_MISC[9])));
		tft.drawString(buffer_tft, 0, 75, 2);


		uint8_t flag = MySignals_BLE.waitEvent(500);

		if (flag == BLE_EVENT_CONNECTION_STATUS)
		{
			MySignals_BLE.app_connected_flag = 1;
		}
		else if (flag == BLE_EVENT_SM_BOND_STATUS)
		{
			if (MySignals_BLE.event[6] == 0x01)
			{
				MySignals_BLE.bonding_correct = 1;
				delay(1000);
			}
		}
		else if (flag == 0)
		{
			// If there are no events, then no one tried to connect
		}
		else if (flag == BLE_EVENT_ATTRIBUTES_VALUE)
		{
			//Already connected
			MySignals_BLE.app_connected_flag = 1;
			MySignals_BLE.bonding_correct = 1;
			MySignals_BLE.bonded_and_connected_flag = 1;
		}
		else
		{
			// Other event received from BLE module
		}

		/////////////////////

		if ((MySignals_BLE.bonding_correct == 1) || MySignals_BLE.app_connected_flag == 1)
		{
			//TFT message:  "Connection detected..."
			strcpy_P((char*)buffer_tft, (char*)pgm_read_word(&(table_MISC[10])));
			tft.drawString(buffer_tft, 0, 90, 2);

			previous = millis();

			while ((MySignals_BLE.bonded_and_connected_flag == 0) && (MySignals_BLE.bonding_fail == 0))
			{
				//  Timeout 30 sg
				if ((millis() - previous) > 30000)
				{
					MySignals_BLE.bonding_fail = 1;
				}

				flag = MySignals_BLE.waitEvent(1000);

				if (flag == 0)
				{
					//Do nothing
				}
				else if (flag == BLE_EVENT_SM_PASSKEY_DISPLAY)
				{

					uint32_t passkey_temp =
						uint32_t(MySignals_BLE.event[5]) +
						uint32_t(MySignals_BLE.event[6]) * 256 +
						uint32_t(MySignals_BLE.event[7]) * 65536 +
						uint32_t(MySignals_BLE.event[8]) * 16777216;

					//TFT message:  "Passkey:";"
					strcpy_P((char*)buffer_tft, (char*)pgm_read_word(&(table_MISC[11])));
					tft.drawString(buffer_tft, 0, 105, 2);
					tft.drawNumber(passkey_temp, 50, 105, 2);
				}

				else if (flag == BLE_EVENT_ATTRIBUTES_VALUE)
				{
					//Already connected
					MySignals_BLE.app_connected_flag = 1;
					MySignals_BLE.bonding_correct = 1;
					MySignals_BLE.bonded_and_connected_flag = 1;
				}

				else if (flag == BLE_EVENT_SM_BOND_STATUS)
				{

					if (MySignals_BLE.event[6] == 0x01)
					{
						//Man-in-the-Middle mode correct
						MySignals_BLE.bonding_correct = 1;
					}
				}

				else if (flag == BLE_EVENT_CONNECTION_FEATURE_IND)
				{
					//Do nothing
				}

				else if (flag == BLE_EVENT_CONNECTION_VERSION_IND)
				{
					//Do nothing
				}

				else if (flag == BLE_EVENT_SM_BONDING_FAIL)
				{
					MySignals_BLE.bonded_and_connected_flag = 0;
					MySignals_BLE.bonding_fail = 1;
				}
				else if (flag == BLE_EVENT_CONNECTION_STATUS)
				{

					if (MySignals_BLE.event[5] == 0x03)
					{
						//Connection correct
						MySignals_BLE.app_connected_flag = 1;

					}
				}
				else if (flag == BLE_EVENT_CONNECTION_DISCONNECTED)
				{
					MySignals_BLE.bonded_and_connected_flag = 0;
					MySignals_BLE.bonding_fail = 1;
				}
				else
				{
					//Do nothing
				}


				if (MySignals_BLE.bonding_correct && MySignals_BLE.app_connected_flag)
				{

					//TFT message:  "Connected!"
					strcpy_P((char*)buffer_tft, (char*)pgm_read_word(&(table_MISC[12])));
					tft.drawString(buffer_tft, 0, 120, 2);


					//TFT message:  "Sensor list:"
					strcpy_P((char*)buffer_tft, (char*)pgm_read_word(&(table_MISC[14])));
					tft.drawString(buffer_tft, 0, 135, 2);

					//// SENSORES

					//TFT message:  "Temperature:"
					strcpy_P((char*)buffer_tft, (char*)pgm_read_word(&(table_MISC[21])));
					tft.drawString(buffer_tft, 0, 150, 2);

					//TFT message:  "EMG:"
					strcpy_P((char*)buffer_tft, (char*)pgm_read_word(&(table_MISC[25])));
					tft.drawString(buffer_tft, 0, 165, 2);

					//TFT message:  "SPO2:"
					strcpy_P((char*)buffer_tft, (char*)pgm_read_word(&(table_MISC[28])));
					tft.drawString(buffer_tft, 0, 180, 2);

					MySignals_BLE.bonded_and_connected_flag = 1;
				}

			}

			if (MySignals_BLE.bonding_fail == 1)
			{
				//TFT message:  "Connection failed. Reseting"
				strcpy_P((char*)buffer_tft, (char*)pgm_read_word(&(table_MISC[13])));
				tft.drawString(buffer_tft, 0, 120, 2);

				MySignals_BLE.bonded_and_connected_flag = 1;
				MySignals_BLE.hardwareReset();
				delay(100);
				MySignals_BLE.initialize_BLE_values();
			}
		}
	}

	// Start transfer data
	if ((MySignals_BLE.ble_mode_flag == slave_mode) && (MySignals_BLE.app_connected_flag == 1))
	{
		MySignals.enableSensorUART(BLE);
		if (teststart == 1)
		{
			if (megcount < 26)
			{
				rawemg = MySignals.getCalibratedEMG(3, 0, 0, DATA);
				rawemg_low = rawemg & 0b0000000011111111;
				rawemg_high = (rawemg & 0b1111111100000000) / 256;
				valueMEG[(megcount*2 -1)] = rawemg_high;
				valueMEG[(megcount*2)] = rawemg_low;
				megcount++;
				Serial.println("emg");
				delay(2);
			}
			else if (megcount==26)
			{
				megcount = 1;
				MySignals_BLE.writeLocalAttribute(handle_3_3, valueMEG, 51);
				countern++;
			}
			if (countern == 400)
			{
				rawtemperature = MySignals.getTemperature() * 100;
				rawtemp_low = rawtemperature & 0b0000000011111111;
				rawtemp_high = (rawtemperature & 0b1111111100000000) / 256;
				valuetemperature[1] = rawtemp_high;
				valuetemperature[2] = rawtemp_low;
				MySignals_BLE.writeLocalAttribute(handle_3_2, valuetemperature, 3);
				Serial.println("temp");
			}
			else if (countern==800)
			{
				if (pulsioximeter_state== 1)
				{
					rawPulse = MySignals.pulsioximeterData.BPM;
					rawSPO2 = MySignals.pulsioximeterData.O2;
					rawPulse_low = rawPulse & 0b0000000011111111;
					rawPulse_high = (rawPulse & 0b1111111100000000) / 256;
					rawSPO2_low = rawSPO2 & 0b0000000011111111;
					rawSPO2_high = (rawSPO2 & 0b1111111100000000) / 256;
					valueSPO2[1] = rawPulse_high;
					valueSPO2[2] = rawPulse_low;
					valueSPO2[3] = rawSPO2_high;
					valueSPO2[4] = rawSPO2_low;
					MySignals_BLE.writeLocalAttribute(handle_3_8, valueSPO2, 5);
					countern == 0;
					Serial.println("spo2");
				}
				else
				{
					rawPulse = 999;
					rawSPO2 = 999;
					rawPulse_low = rawPulse & 0b0000000011111111;
					rawPulse_high = (rawPulse & 0b1111111100000000) / 256;
					rawSPO2_low = rawSPO2 & 0b0000000011111111;
					rawSPO2_high = (rawSPO2 & 0b1111111100000000) / 256;
					valueSPO2[1] = rawPulse_high;
					valueSPO2[2] = rawPulse_low;
					valueSPO2[3] = rawSPO2_high;
					valueSPO2[4] = rawSPO2_low;
					MySignals_BLE.writeLocalAttribute(handle_3_8, valueSPO2, 5);
					countern == 0;
				}
			}
		}
		else
		{
			delay(1000);
		}
	}
}