import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import face_recognition
from PIL import Image


# Selfie Segmentation
mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation

#Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

st.subheader("Face recognition project")

st.write("""
\nSubmited by: Lakshmipriya.S""")

add_selectbox = st.sidebar.selectbox(
    "How would you like to edit your image?",
    ("Project features", "Background Changer", "Face Detection", "Face Recognition")
)

if add_selectbox == "Project features":
   
    st.write("1. Background Changer \n2. Face Detection \n3. Face Recognition")

# Background Changer
elif add_selectbox == "Background Changer": 
    with mp_selfie_segmentation.SelfieSegmentation(model_selection=0) as selfie_segmentation:
        fg_image = st.sidebar.file_uploader("Upload a FOREGROUND IMAGE")
        st.sidebar.write("Here, you can change the background of the image that you upload")

        if fg_image is not None:
            fimage = np.array(Image.open(fg_image))
            st.sidebar.image(fimage)
            results = selfie_segmentation.process(fimage)
            condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1

            add_bg = st.sidebar.selectbox(
                "Change your Background as follows?",
                ("Image of your choice", "Inbuilt Image", "Colors")
            )
            if add_bg == "Image of your choice":
                bg_image = st.sidebar.file_uploader("Upload a BACKGROUND IMAGE")
                if bg_image is not None:
                    bimage = np.array(Image.open(bg_image))
                    st.sidebar.image(bimage)
                    bimage = cv2.resize(bimage, (fimage.shape[1], fimage.shape[0]))
                    output_image = np.where(condition, fimage, bimage)
                    st.image(output_image)

            elif add_bg == "Inbuilt Image":
                add_ib_bg = st.sidebar.selectbox(
                    "Which defaukt background do you prefer?",
                    ("Strawberry","pika","bts","au")
                )
                if add_ib_bg == "Strawberry":
                    bg_image = cv2.imread("/Users/lakshmipriya/Desktop/Face_recognition_image/images/strawberry.jpg")
                    bg_image = cv2.cvtColor(bg_image, cv2.COLOR_RGB2BGR)
                    if bg_image is not None: 
                        st.sidebar.image(bg_image)
                        bimage = cv2.resize(bg_image, (fimage.shape[1], fimage.shape[0]))
                        output_image = np.where(condition, fimage, bimage)
                        st.image(output_image) 

                elif add_ib_bg == "pika":
                    bg_image = cv2.imread("/Users/lakshmipriya/Desktop/Face_recognition_image/images/pika.jpg")
                    bg_image = cv2.cvtColor(bg_image, cv2.COLOR_RGB2BGR)
                    if bg_image is not None: 
                        st.sidebar.image(bg_image)
                        bimage = cv2.resize(bg_image, (fimage.shape[1], fimage.shape[0]))
                        output_image = np.where(condition, fimage, bimage)
                        st.image(output_image)

                elif add_ib_bg == "bts":
                    bg_image = cv2.imread("/Users/lakshmipriya/Desktop/Face_recognition_image/images/bts.jpg")
                    bg_image = cv2.cvtColor(bg_image, cv2.COLOR_RGB2BGR)
                    if bg_image is not None: 
                        st.sidebar.image(bg_image)
                        bimage = cv2.resize(bg_image, (fimage.shape[1], fimage.shape[0]))
                        output_image = np.where(condition, fimage, bimage)
                        st.image(output_image)   

                elif add_ib_bg == "au":
                    bg_image = cv2.imread("/Users/lakshmipriya/Desktop/Face_recognition_image/images/au.jpg")
                    bg_image = cv2.cvtColor(bg_image, cv2.COLOR_RGB2BGR)
                    if bg_image is not None: 
                        st.sidebar.image(bg_image)
                        bimage = cv2.resize(bg_image, (fimage.shape[1], fimage.shape[0]))
                        output_image = np.where(condition, fimage, bimage)
                        st.image(output_image)
                else:
                    st.write("Choose some other option")

            elif add_bg == "Colors":
                    add_c_bg = st.sidebar.seceltbox(
                        "Choose a color as a background",
                        ("Red","Green","Blue","Gray")
                    )
                    if add_c_bg == "Red":
                        BG_COLOR = (255,0,0)
                        bg_image = np.zeros(fimage.shape, dtype=np.uint8)
                        bg_image[:] = BG_COLOR
                        output_image = np.where(condition, fimage, bg_image)
                        st.image(output_image)
                    elif add_c_bg == "Green":
                        BG_COLOR = (0,255,0)
                        bg_image = np.zeros(fimage.shape, dtype=np.uint8)
                        bg_image[:] = BG_COLOR
                        output_image = np.where(condition, fimage, bg_image)
                        st.image(output_image)
                    elif add_c_bg == "Blue":
                        BG_COLOR = (0,0,255)
                        bg_image = np.zeros(fimage.shape, dtype=np.uint8)
                        bg_image[:] = BG_COLOR
                        output_image = np.where(condition, fimage, bg_image)
                        st.image(output_image)
                    elif add_c_bg == "Gray":
                        BG_COLOR = (192,192,192)
                        bg_image = np.zeros(fimage.shape, dtype=np.uint8)
                        bg_image[:] = BG_COLOR
                        output_image = np.where(condition, fimage, bg_image)
                        st.image(output_image)

# Face Detection
elif add_selectbox == "Face Detection":
    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.6) as face_detection:
        fd_image = st.sidebar.file_uploader("Upload a FOREGROUND IMAGE")
        if fd_image is not None:
            fdimage = np.array(Image.open(fd_image))
            st.sidebar.image(fdimage)
            results = face_detection.process(fdimage)
            for landmark in results.detections:
                mp_drawing.draw_detection(fdimage, landmark)
            st.image(fdimage)

# Face Recognition
elif add_selectbox == "Face Recognition":
    st.write("Upload TWO IMAGES")
    image = st.sidebar.file_uploader("Upload the first image")
    if image is not None:
        train_image = np.array(Image.open(image))
        st.sidebar.image(train_image)
        image_train = face_recognition.load_image_file(image)
        image_encodings_train = face_recognition.face_encodings(image_train)[0]
        image_location_train = face_recognition.face_locations(image_train)

        detect_image = st.sidebar.file_uploader("Upload the second image")
        if detect_image is not None:
            test_image = np.array(Image.open(detect_image))
            st.sidebar.image(test_image)
            image_test = face_recognition.load_image_file(detect_image)
            image_encodings_test = face_recognition.face_encodings(image_test)[0]
            image_location_test = face_recognition.face_locations(image_test)

            results = face_recognition.compare_faces([image_encodings_test], image_encodings_train)[0]
            dst = face_recognition.face_distance([image_encodings_test], image_encodings_train)

            if results:
                for (top, right, bottom, left) in image_location_test:
                    output_image1 = cv2.rectangle(test_image, (left, top), (right, bottom), (0, 0, 255), 2)
                for (top, right, bottom, left) in image_location_train:
                    output_image2 = cv2.rectangle(train_image, (left, top), (right, bottom), (0, 0, 255), 2)
                st.image(output_image1)
                st.image(output_image2)
                
                st.write("Both the faces are same")
            else:
                st.write("Both faces doesn't match")
        else:
            st.write("Upload a pic")
    


else:
    st.write("Choose any of the given options")