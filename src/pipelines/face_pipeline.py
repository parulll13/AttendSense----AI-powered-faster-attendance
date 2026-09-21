import streamlit as st
import numpy as np
import dlib
import face_recognition_models
from sklearn.svm import SVC
from src.database.db import get_all_students


#Loading dlib models
@st.cache_resource
def load_dlib_models():
    #1st : For face detector
    detector = dlib.get_frontal_face_detector()

    #2nd: For Landmarks detector
    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    #3rd: For converting into embeddings
    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location())

    return detector, sp, facerec

def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()

    # Detect all faces present in the image
    faces = detector(image_np, 1) #1 means the image is upsampled once to detect faces 
    encodings = []

    for face in faces:
        shape = sp(image_np, face)  # Detect facial landmarks for the face in an image
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)  # Generate a 128-dimensional face embedding using the image and facial landmarks
        encodings.append(np.array(face_descriptor))   #adding embeddings in a form of array in a list

    return encodings 


@st.cache_resource
#Trained the model which finds if student is present in the image and its location using SVC model
def get_trained_model():
    X =[]
    y =[]
    student_db = get_all_students()
    if not student_db:
        return None
    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding:
            X.append(np.array(embedding))
            y.append(student.get('student_id'))

    if len(X)==0:
        return 0
    #create SVC classifier, its job is to predict which student_id is belongs to which face_embedding
    clf = SVC(kernel = 'linear', probability=True, class_weight='balanced')

    try:
        #train the classifier on X and y values
        clf.fit(X,y)
    except ValueError:
        pass
    return {'clf':clf , 'X':X , 'y':y} 


#this fn uses when a new student comes in 
#clears Streamlit's cached resources, trains/loads the classifier, and then tells you whether a model was successfully obtained
def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)

def predict_attendance(class_image_np):

    # Get face embeddings for every face detected in the classroom image
    encodings = get_face_embeddings(class_image_np)

    # Dictionary to store students detected/present
    detected_student = {}

    # Get the trained face-recognition model and training data
    model_data = get_trained_model()

    if not model_data:
        return detected_student,[], len(encodings)       # [] = no. of students 

    # Get the trained classifier (SVM)
    clf = model_data['clf']
    # Get stored face embeddings used for training
    X_train = model_data['X']
    # Get student IDs corresponding to X_train
    y_train = model_data['y']

    # Get unique student IDs from the training labels
    all_students = sorted(list(set(y_train)))

    # Process each face detected in the classroom image
    for encoding in encodings:
        if len(all_students)==1:
            predicted_id = int(all_students[0])
        else:
            # Ask the trained classifier which student this face belongs to
            predicted_id= int(clf.predict([encoding])[0])

        #Find the stored face embedding of the predicted student
        student_embedding = X_train[y_train.index(predicted_id)]
        # Calculate distance between stored face and detected face
        best_match_score = np.linalg.norm(student_embedding-encoding)
        
        resemblance_threshold = 0.6
        if best_match_score <= resemblance_threshold:
            detected_student[predicted_id] = True
            print("face detected")
        else:
            print('not detetcted')

    # Return:students detected as present, all registered students, number of faces detected in image
    return detected_student, all_students, len(encodings)








