import cv2
from flask import Flask, render_template, Response
import imutils

app = Flask(__name__)

# Function to capture video frames
def generate_frames():
    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()
        if not ret:
            break
        else:
            frame = imutils.resize(frame, width=600)

            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route to display video stream on a web page
@app.route('/')
def index():
    return render_template('index.html')

# Route to stream video frames
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5090)
