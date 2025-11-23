import serial
import pyaudio
import wave
import threading
import time
import os
from datetime import datetime
import sys

# Configuration
SERIAL_PORT = "COM3"
BAUD_RATE = 921600  # Match ESP32 baud rate
SAMPLE_RATE = 16000
CHUNK = 1024
RECORD_DURATION = 10  # seconds

class AudioRecorder:
    def __init__(self):
        self.ser = None
        self.audio = None
        self.recording = False
        self.audio_data = []
        self.current_label = ""
        
    def connect_serial(self):
        """Connect to ESP32"""
        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
            print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud")
            return True
        except serial.SerialException as e:
            print(f"Error connecting to {SERIAL_PORT}: {e}")
            return False
    
    def initialize_audio(self):
        """Initialize PyAudio"""
        try:
            self.audio = pyaudio.PyAudio()
            return True
        except Exception as e:
            print(f"Error initializing audio: {e}")
            return False
    
    def record_audio(self, label):
        """Record audio for specified duration"""
        if self.recording:
            print("Already recording! Please wait...")
            return
        
        self.current_label = label
        self.audio_data = []
        self.recording = True
        
        print(f"Recording {label} for {RECORD_DURATION} seconds...")
        
        # Calculate number of chunks needed for recording duration
        chunks_needed = int((SAMPLE_RATE * RECORD_DURATION) / CHUNK)
        chunks_recorded = 0
        
        try:
            while self.recording and chunks_recorded < chunks_needed:
                if self.ser.in_waiting >= CHUNK * 2:
                    data = self.ser.read(CHUNK * 2)
                    self.audio_data.append(data)
                    chunks_recorded += 1
                    
                    # Progress indicator
                    if chunks_recorded % (chunks_needed // 10) == 0:
                        progress = (chunks_recorded / chunks_needed) * 100
                        print(f"Recording... {progress:.0f}%")
            
            # Save the recording
            self.save_recording()
            
        except Exception as e:
            print(f"Error during recording: {e}")
        finally:
            self.recording = False
    
    def save_recording(self):
        """Save recorded audio as WAV file"""
        if not self.audio_data:
            print("No audio data to save!")
            return
        
        # Create recordings directory if it doesn't exist
        if not os.path.exists("recordings"):
            os.makedirs("recordings")
        
        # Generate filename with timestamp and label
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recordings/{self.current_label}_{timestamp}.wav"
        
        try:
            # Save as WAV file
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(1)  # Mono
                wf.setsampwidth(2)  # 2 bytes (16 bits) per sample
                wf.setframerate(SAMPLE_RATE)
                wf.writeframes(b''.join(self.audio_data))
            
            print(f"Recording saved as: {filename}")
            print(f"File size: {len(b''.join(self.audio_data))} bytes")
            
        except Exception as e:
            print(f"Error saving recording: {e}")
    
    def start_recording_thread(self, label):
        """Start recording in a separate thread"""
        recording_thread = threading.Thread(target=self.record_audio, args=(label,))
        recording_thread.daemon = True
        recording_thread.start()
    
    def run(self):
        """Main program loop"""
        print("ESP32 Audio Recorder")
        print("====================")
        print(f"Sample rate: {SAMPLE_RATE} Hz")
        print(f"Recording duration: {RECORD_DURATION} seconds")
        print("\nCommands:")
        print("  Type any word (e.g., 'hello') to record with that label")
        print("  Type 'quit' or 'exit' to stop the program")
        print("-" * 50)
        
        # Initialize connections
        if not self.connect_serial():
            return
        
        if not self.initialize_audio():
            self.ser.close()
            return
        
        try:
            # Main command loop
            while True:
                if not self.recording:
                    command = input("\nEnter label for recording: ").strip().lower()
                    
                    if command in ['quit', 'exit', 'q']:
                        break
                    elif command == 'rec':
                        self.start_recording_thread("recording")
                    elif command:
                        self.start_recording_thread(command)
                    else:
                        print("Please enter a valid label")
                else:
                    # Wait a bit if recording is in progress
                    time.sleep(0.1)
                    
        except KeyboardInterrupt:
            print("\nProgram interrupted by user")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        print("\nCleaning up...")
        if self.ser and self.ser.is_open:
            self.ser.close()
        if self.audio:
            self.audio.terminate()
        print("Goodbye!")

def main():
    recorder = AudioRecorder()
    recorder.run()

if __name__ == "__main__":
    main()