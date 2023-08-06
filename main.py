import cv2
import serial
from simple_facerec import SimpleFacerec

# Encode faces from a folder
sfr = SimpleFacerec()
sfr.load_encoding_images("C:/Users/PRITHIJIT/Downloads/face/source code/images")

ser = serial.Serial('COM5', 9600)

# Load Camera
cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()

    # Detect Faces
    face_locations, face_names = sfr.detect_known_faces(frame);
    for face_loc, name in zip(face_locations, face_names):
        print(face_names)
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

        name_bytes = face_names[0].encode('utf-8')
        # Break the main loop
        if len(face_names) > 0:
            break

    cv2.imshow("Frame", frame)
    cv2.waitKey(5000)

    if len(face_names) > 0:
        name_str = name_bytes.decode('utf-8')
        print(name_str)
        ser.write(name_bytes)
        break

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
