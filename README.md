# ESP32-WROOM-INMP441-Keyword-Spotting-Project
A voice command recognition system using ESP32-WROOM and INMP441 microphone for keyword spotting. This project enables real-time voice command detection with Edge Impulse machine learning.

## 🎯 Project Overview
This system captures audio using an INMP441 microphone, processes it on an ESP32-WROOM board, and detects voice commands like "開" and "関" using a trained Edge Impulse model. The detected commands control an built in LED, demonstrating real-time voice-activated control.

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
