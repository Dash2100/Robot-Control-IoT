from flask import Flask, Response, render_template
import pyaudio

app = Flask(__name__)

p = pyaudio.PyAudio()

def generateAudio():
    FORMAT = pyaudio.paInt16
    CHUNK = 64  # 調整緩衝區大小
    CHANNELS = 1
    RATE = 44100
    sampleRate = 44100
    bitsPerSample = 16
    channels = 1

    def genHeader(sampleRate, bitsPerSample, channels):
        datasize = 2000*10**6
        o = bytes("RIFF",'ascii')
        o += (datasize + 36).to_bytes(4,'little')
        o += bytes("WAVE",'ascii')
        o += bytes("fmt ",'ascii')
        o += (16).to_bytes(4,'little')
        o += (1).to_bytes(2,'little')
        o += (channels).to_bytes(2,'little')
        o += (sampleRate).to_bytes(4,'little')
        o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')
        o += (channels * bitsPerSample // 8).to_bytes(2,'little')
        o += (bitsPerSample).to_bytes(2,'little')
        o += bytes("data",'ascii')
        o += (datasize).to_bytes(4,'little')
        return o

    wav_header = genHeader(sampleRate, bitsPerSample, channels)
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=1, frames_per_buffer=CHUNK)

    print("* Mendengarkan suara...")
    yield wav_header

    while True:
        data = stream.read(CHUNK)
        yield data

@app.route("/audio")
def audio():
    return Response(generateAudio(), mimetype="audio/x-wav")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, threaded=True, port=5000)
