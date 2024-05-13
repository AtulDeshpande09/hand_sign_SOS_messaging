import cv2
import mediapipe as mp
import pickle
import numpy as np
from sos import SOS_message ,pop_list

model_dict = pickle.load(open('./model.p','rb'))
model = model_dict['model']

cap = cv2.VideoCapture(0)

Slow_down_count = 0
Freeze_count = 0

#SOS message is (Slow down)-(Freeze) ----> (Slow down)_count >= 10 : (Slow down) pop() ----> (Freeze)_count >= 10 : (Freeze) pop()
original_list = ['Freeze','Slow down']
pass_list = original_list
counter = 0


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode = True , min_detection_confidence = 0.3)

labels_dict = {0:'Slow down', 1:'Freeze'}

while True:
    data_aux = []

    x_ = []
    y_= []
    ret,frame = cap.read()

    H, W, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        # You can uncomment below lines to get markers on the hands
        """for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,  # image to draw
                hand_landmarks,  # model output
                mp_hands.HAND_CONNECTIONS,  # hand connections
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())"""
        
        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x)
                data_aux.append(y)
                x_.append(x)
                y_.append(y)
        
        x1 = int(min(x_)*W)
        y1 = int(min(y_)*H)

        x2 = int(max(x_)*W)
        y2 = int(max(y_)*H)

        prediction = model.predict([np.asarray(data_aux)])

        pred_char = labels_dict[int(prediction[0])]
        print(pred_char)



        cv2.rectangle(frame , (x1,y1),(x2,y2),(0,255,0),4)
        cv2.putText(frame, pred_char, (x1, y1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 3,
                    cv2.LINE_AA)
        

        Slow_down_count = Slow_down_count+1 if (pred_char == "Slow down") else Slow_down_count+0
        Freeze_count = Freeze_count+1 if (pred_char == "Freeze") else Freeze_count+0

        pop_list(pass_list , Slow_down_count , Freeze_count)

        Slow_down_count = 0 if (pred_char != "Slow down") else Slow_down_count
        Freeze_count = 0 if (pred_char != "Freeze") else Freeze_count

        print("Slow_down_count : ",Slow_down_count," Freeze_count : ",Freeze_count)
        print("LIST : ",pass_list)

        new_list = SOS_message(pass_list, ['Freeze','Slow down'])
        pass_list = new_list

        




    cv2.imshow('frame',frame)
    cv2.waitKey(20)


cap.release()
cv2.destroyAllWindows()