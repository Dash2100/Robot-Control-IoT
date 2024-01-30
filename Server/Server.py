from flask import Flask, Response, render_template
import pyaudio

app = Flask(__name__)

p = pyaudio.PyAudio()
mic = 0

def genHeader(sampleRate, bitsPerSample, channels):
    datasize = 2000*10**6  # Adjust estimated data size
    o = bytes("RIFF", 'ascii')
    o += (datasize + 36).to_bytes(4, 'little')
    o += bytes("WAVE", 'ascii')
    o += bytes("fmt ", 'ascii')
    o += (16).to_bytes(4, 'little')
    o += (1).to_bytes(2, 'little')
    o += (channels).to_bytes(2, 'little')
    o += (sampleRate).to_bytes(4, 'little')
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4, 'little')
    o += (channels * bitsPerSample // 8).to_bytes(2, 'little')
    o += (bitsPerSample).to_bytes(2, 'little')
    o += bytes("data", 'ascii')
    o += (datasize).to_bytes(4, 'little')
    return o

def generateAudio():
    FORMAT = pyaudio.paInt16
    CHUNK = 128  # Reduced chunk size
    CHANNELS = 1
    RATE = 44100
    bitsPerSample = 16

    wav_header = genHeader(RATE, bitsPerSample, CHANNELS)
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=mic)

    print("* Mendengarkan suara...")
    yield wav_header  # Yield header first

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            yield data
    finally:
        stream.stop_stream()
        stream.close()

@app.route("/audio")
def audio():
    return Response(generateAudio(), mimetype="audio/x-wav", direct_passthrough=True)  # Prevent Flask buffering

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, threaded=True, port=5090)
