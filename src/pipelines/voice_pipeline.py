import librosa  #Loads and processes the recorded audio
#preprocess_wav(): prepare the audio before giving it to the voice model. It performs the preprocessing needed by Resemblyzer so the voice encoder can work properly
#VoiceEncoder(): The model takes the processed voice and converts it into a 256-number voice embedding.
from resemblyzer import VoiceEncoder, preprocess_wav   
import numpy as np
import io       #treats your audio_bytes as a file without actually saving it to disk.
import streamlit as st

#PIPELINE : Student speaks --> Audio recording --> audio_bytes --> librosa (load + convert audio to 16 kHz) 
# --> preprocess_wav() (clean/normalize audio) --> Resemblyzer --> Voice embedding (256 numbers) --> 
# Compare with registered students --> Similarity score --> Threshold ≥ 0.65 ? --> Student identified 
# --> Attendance marked


@st.cache_resource
def load_voice_encoder():
    #VoiceEncoder: model that converts speech of the speaker's voice. into a numerical representation.
    return VoiceEncoder()  

def get_voice_embedding(audio_bytes):
    try:

        encoder = load_voice_encoder()

        #audio_bytes Contains the recorded audio in bytes.But librosa needs something it can read as audio. Therefore io.BytesIO(audio_bytes) Converts the bytes into a file-like object in memory.
        #Librosa reads the audio & returns two things: audio = Contains the actual audio waveform as a NumPy array and sr = the audio resampled 16,000 samples per second (16 kHz)
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr =16000)   #sr = sample rate

        #preprocess_wav(): It prepares the audio for the voice encoder (Raw audio --> clean waveform)
        wav = preprocess_wav(audio)

        #entering processed audio into encoder which contains VoiceEncoder() model and convert it into voice embedding
        embedding = encoder.embed_utterance(wav)

        #embedding is a NumPy array. Converts it into a normal Python list
        return embedding.tolist()
    
    except Exception as e:
        st.error('Voice recognization error')
        return None


#Now we identify the speaker: This function answers: "Whose voice is this?"
#It takes three things: new_embedding - The embedding of the new recording.
#                       candidates_dict - The stored embeddings of registered students.
#                       threshold=0.65 - Minimum similarity score required to accept a match.
#this fn returns student id that best match with new embedding & best score

def identify_speaker(new_embedding, candidates_dict, threshold = 0.65):
    if new_embedding is None or not candidates_dict:
        return None, 0.0 

    best_sid = None       #sid means student ID. Initially we don't know who the speaker is.
    best_score = -1.0     #it keeps the track of the highest similarity score. Take it -1 bcoz every other is greater than this

    for sid , stored_embedding in candidates_dict.items():
        if stored_embedding:
            similarity = np.dot(new_embedding, stored_embedding)
            if similarity > best_score:
                best_score = similarity
                best_sid = sid

    if best_score >= threshold:
        return best_sid, best_score 

    return None, best_score

 
# Now this function is slightly different. Imagine the teacher records: ["Yes ma'am, I am Rahul.", "Yes ma'am, I am Priya.", "Yes ma'am, I am Aman."] all in one long recording. 
# You need to separate the recording into speech segments. That's what this function does.
def process_bulk_audio(audio_bytes, candidates_dict, threshold = 0.65):

    try:
        encoder = load_voice_encoder()   #convert into voice embedding same as before
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr = 16000)  #Load audio same as before

        # librosa.effects.split() tries to identify portions of the audio containing sound and separates them from silent sections.
        #like we know after one student speaks there's gap before other student speaks  
        #Each segment contains: (start, end) which are positions in the audio array.
        segments = librosa.effects.split(audio, top_db=30)  #top_db=30 = the silence detection sensitivity used to separate speech from quiet portions of the recording.

        identified_results = {}  #This will eventually contain recognized students and their best scores.

        for start, end in segments:
            if(end-start)<sr*0.5:   #If the segment is shorter than 0.5 seconds, ignore it.
                continue
            segment_audio = audio[start:end]          #This takes only that particular speech section
            wav = preprocess_wav(segment_audio)       #Preprocess the segment
            embedding = encoder.embed_utterance(wav)  #Create embedding

            sid,score = identify_speaker(embedding, candidates_dict, threshold)  #Now you send the new voice embedding to your previous function.

            if sid :      #if sid is not None
                if sid not in identified_results or score > identified_results[sid]:
                    identified_results[sid] = score  #add sid and its score in dict 

        return identified_results
    
    except Exception as e:
        st.error('Bulk process error')
        return {}