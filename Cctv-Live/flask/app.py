from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Open the default webcam
camera_index = 0  # Change this index if you have multiple cameras
cam = cv2.VideoCapture(camera_index)

if not cam.isOpened():
    print(f"Error: Camera with index {camera_index} could not be accessed.")
else:
    print("Camera is successfully opened.")

def cctv_live():
    while True:
        success, frame = cam.read()
        if not success:
            print("Error: Unable to capture video frame.")
            break
        else:
            cv2.putText(frame, "Live CCTV Feed", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Encode frame to JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                print("Error: Could not encode the frame to JPEG.")
                continue

            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/")
def index():
    return render_template("index.html")  # Ensure this file exists in the templates folder

@app.route("/video")
def video():
    return Response(cctv_live(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Cleanup: Release the camera when the application stops
@app.teardown_appcontext
def cleanup(exception=None):
    if cam.isOpened():
        cam.release()
        print("Camera resource released.")

if __name__ == "__main__":
    app.run(debug=True)
