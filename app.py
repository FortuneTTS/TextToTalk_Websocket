import websocket
import _thread
import time
import rel
import json
from TTS.api import TTS
import playsound

# Init TTS with the target model name
tts = TTS(model_name="tts_models/en/ljspeech/glow-tts", progress_bar=False, gpu=False)

#websocket
def on_message(ws, message):
    Json_message = json.loads(message)
    if Json_message["Type"] == "Say":
        tts.tts_to_file(text=Json_message["Payload"], file_path="output.wav")
        playsound.playsound('output.wav', True)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

if __name__ == "__main__":
    websocket.enableTrace(False) 
    ws = websocket.WebSocketApp("ws://localhost:8000/Messages",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()