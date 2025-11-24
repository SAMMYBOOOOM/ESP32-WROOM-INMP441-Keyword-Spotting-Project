# ESP32-WROOM-INMP441-Keyword-Spotting-Project
A voice command recognition system using ESP32-WROOM and INMP441 microphone for keyword spotting. This project enables real-time voice command detection with Edge Impulse machine learning.

## 🎯 Project Overview
This system captures audio using an INMP441 microphone, processes it on an ESP32-WROOM board, and detects voice commands like "開" and "関" using a trained Edge Impulse model. The detected commands control an built in LED, demonstrating real-time voice-activated control.
![working](https://github.com/SAMMYBOOOOM/ESP32-WROOM-INMP441-Keyword-Spotting-Project/blob/main/img/img.gif)

## 🛠 Hardware Requirements
Components: 
- ESP32-WROOM Development Board
- INMP441 I2S Microphone Module
- Jumper Wires
- Breadboard

### Wiring Diagram
```
INMP441 → ESP32-WROOM
=====================
VCC    → 3.3V
GND    → GND
SD     → GPIO 21
WS     → GPIO 22
SCK    → GPIO 19
```

## Getting_Started

1. Compile and upload the code from [wroom_INMP441.ino](https://github.com/SAMMYBOOOOM/ESP32-WROOM-INMP441-Keyword-Spotting-Project/blob/main/code/wroom_INMP441.ino) to send the audio back to the computer.

2. Run the python script [recorder.py](https://github.com/SAMMYBOOOOM/ESP32-WROOM-INMP441-Keyword-Spotting-Project/blob/main/code/recorder.py) to make the 10s `.wav` audio file

3. Then clone the [Audio Classification - Keyword Spotting](https://studio.edgeimpulse.com/public/499022/latest) project in Edge Impulse.

4. The project is originally make for spotting "helloworld", so just delete every that's not labeled as noise or unknown.

5. Then upload your recorded `.wav` audio file and split the audio into 1s audio

6. Choose Create impulse MFCC + Classifier, then go though both with default option and save&train the model.

7. To deployment and choose Arduino library and build it and download the model.

8. Add the zip to your arduino and in the zip file, find the example name esp32_microphone, and modify the code similar to [esp32-wroom-edge.ino](https://github.com/SAMMYBOOOOM/ESP32-WROOM-INMP441-Keyword-Spotting-Project/blob/main/code/esp32-wroom-edge.ino), then you have your own custom keyword spotting machine.

>Currently, you need to manually configure when the ESP32 records the 1-second audio window and runs inference; otherwise, you must time your speech moment with the serial terminal refresh.

## 📚 Resources
[Edge Impulse Keyword Spotting](https://docs.edgeimpulse.com/datasets/audio/keyword-spotting)

[ESP32 Voice Control with AI (No Cloud Needed!)](https://www.youtube.com/watch?v=gJumlH3rfMo)

[Creating ML Model for Offline Voice Recognition ⚡️⚡️](https://www.youtube.com/watch?v=0X0vkzMOAA0)
