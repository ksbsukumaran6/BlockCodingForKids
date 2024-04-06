// NeoPixel Ring simple sketch (c) 2013 Shae Erisson
// Released under the GPLv3 license to match the rest of the
// Adafruit NeoPixel library

#include <Adafruit_NeoPixel.h>
#include <SoftwareSerial.h>

#ifdef __AVR__
#include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

// Which pin on the Arduino is connected to the NeoPixels?
#define PIN        2 // On Trinket or Gemma, suggest changing this to 1

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS 40 // Popular NeoPixel ring size
#define NUM_ROWS 5
#define NUM_COLS 8

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
SoftwareSerial BTSerial(1, 0);  // RX, TX (Pico pins)

//#define DELAYVAL 500 // Time (in milliseconds) to pause between pixels

void setup() {
  BTSerial.begin(9600);
  //  Serial.begin(9600);
  while (!BTSerial) { }
  // These lines are specifically to support the Adafruit Trinket 5V 16 MHz.
  // Any other board, you can remove this part (but no harm leaving it):
#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif
  // END of Trinket-specific code.

  pixels.begin(); // INITIALIZE NeoPixel strip object (REQUIRED)
  pixels.clear(); // Set all pixel colors to 'off'
  BTSerial.print("Ready\n");

  uint8_t datatest[6] = {0x07, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};
  updateLedMatrix(datatest + 1);
}

void loop() {

  if (BTSerial.available() >= 6) {
    // Read the incoming Bluetooth data
    uint8_t data[6];
    for (int i = 0; i < 6; ++i) {
      data[i] = BTSerial.read();
    }

    // Check if the received data is for the LED matrix
    if (data[0] == 0x07) {
      // Update the LED matrix based on the received data
      updateLedMatrix(data + 1);
    }
  }
}


void setPixel(int x, int y) {
  // Map 2D coordinates to 1D index
  int index = x + y * 8;

  // Set the pixel color
  pixels.setPixelColor(index, pixels.Color(255, 255, 255));

}

void clearMatrix() {
  // Turn off all pixels in the strip
  for (int i = 0; i < pixels.numPixels(); i++) {
    pixels.setPixelColor(i, pixels.Color(0, 0, 0));
  }

  // Update the NeoPixel strip
  pixels.show();
}
void updateLedMatrix(uint8_t *rowData) {
  for (int row = 0; row < NUM_ROWS; ++row) {
    for (int col = 0; col < NUM_COLS; ++col) {
      // Extract pixel value for each LED in the row
      uint8_t pixelValue = (rowData[row] >> (NUM_COLS - 1 - col)) & 0x01;

      // Calculate the index for the corresponding LED in the matrix
      int pixelIndex = row * NUM_COLS + col;

      // Set the color of the LED based on the pixel value
      pixels.setPixelColor(pixelIndex, pixelValue ? pixels.Color(255, 255, 255) : pixels.Color(0, 0, 0));
    }
  }

  // Update the LED matrix
  pixels.show();
}
