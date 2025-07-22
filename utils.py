# Updated utils.py
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import cvlib as cv

# Load model once
model = load_model("emotion_model.h5")
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

def detect_emotion(image):
    # Convert to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect faces using cvlib
    faces, confidences = cv.detect_face(image)

    for face in faces:
        (startX, startY) = face[0], face[1]
        (endX, endY) = face[2], face[3]

        # Crop and preprocess face
        face_crop = image[startY:endY, startX:endX]
        if face_crop.shape[0] == 0 or face_crop.shape[1] == 0:
            continue

        gray = cv2.cvtColor(face_crop, cv2.COLOR_RGB2GRAY)
        resized = cv2.resize(gray, (48, 48))
        normed = resized.astype("float32") / 255.0
        reshaped = np.reshape(normed, (1, 48, 48, 1))

        prediction = model.predict(reshaped)[0]
        print("Probabilities:", dict(zip(emotion_labels, prediction)))  # Debug print

        # Always return the most probable emotion
        label = emotion_labels[np.argmax(prediction)]
        return label

    return "No Face Detected"
