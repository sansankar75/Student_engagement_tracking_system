# Face detection using DeepFace package 
"""
import cv2
from deepface import DeepFace
import time
from database_connection import emotion_in_real_time

cap = cv2.VideoCapture(0)

emotions_list=[]

print("[INFO] Starting webcam. Press 'q' to quit...")

def Face_detect(resized_frame):
    try:
        result = DeepFace.analyze(resized_frame, actions=['emotion'], enforce_detection=False)
        return result[0]['dominant_emotion']
    except Exception as e:
        return "No Face"

    
def Cam():
    last_detection_time=0
    detection_interval=5
    emotion=""
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        resized_frame = cv2.resize(frame, (640, 480))

        current_time = time.time()
        if current_time - last_detection_time >= detection_interval:
            emotion = Face_detect(resized_frame)
            last_detection_time = current_time
            print(emotion)
            emotions_list.append(emotion)

        cv2.putText(frame, f"Emotion: {emotion}", (20, 50),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("DeepFace Emotion Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


Cam()

emotion_in_real_time(emotions_list)
cap.release()
cv2.destroyAllWindows()
"""

import cv2
from deepface import DeepFace
import time
import concurrent.futures
import threading

from database_connection import store_class_notes

from database_connection import emotion_in_real_time

#from database_connection import students_emotions

# Thread-safe results list
results_lock = threading.Lock()
results = []

def Face_detect(resized_frame):
    try:
        result = DeepFace.analyze(resized_frame, actions=['emotion'], enforce_detection=False)
        return result[0]['dominant_emotion']
    except Exception:
        return "No Face"

def process_video(video_path, name, class_):
    cap = cv2.VideoCapture(video_path)
    last_detection_time = 0
    detection_interval = 5  # seconds
    emotion = ""

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        resized_frame = cv2.resize(frame, (640, 480))
        current_time = time.time()

        if current_time - last_detection_time >= detection_interval:
            emotion = Face_detect(resized_frame)
            last_detection_time = current_time

            # Save detection result with metadata in a thread-safe way
            with results_lock:
                results.append([name,class_,current_time,emotion])

            #print(results)
            print(f"[{name} - {class_}] Detected emotion: {emotion}")

    cap.release()

def main():
    # List of videos and metadata, replace with your actual data source
    video_list = [
        ('video1.mp4', 'Alice', 'Class A'),
        ('video2.mp4', 'Bob', 'Class B'),
        ('video3.mp4', 'Charlie', 'Class C'),
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_video, v, n, c) for v, n, c in video_list]

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing video: {e}")

    # After all processing finished, 'results' contains all detections
    print("All detection results:")
    for r in results:
        print(r)


main() 

emotion_in_real_time(results)
#store_class_notes()

#students_emotions(results)