
DATA_LINE_PLACE_HOLDER

//float FREQUENCY = 0.025;

int LED_NUMBER = 5;

void setup() {
  // put your setup code here, to run once:
  pinMode(LED_NUMBER, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  send_data(LED_NUMBER, data, 776);
  delay(2000);
}

void send_data(int led, int data_to_send[766][2], int size) {
    for (int i = 0; i < size; i++) {
      if (data_to_send[i][1] == 1) {
        blink_led(led, data[i][0]);
      } else {
        delay(data[i][0]);
      }
    }
}

void blink_led(int led, int milliseconds) {
  digitalWrite(led, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(milliseconds);                       // wait for a second
  digitalWrite(led, LOW);    // turn the LED off by making the voltage LOW
}
