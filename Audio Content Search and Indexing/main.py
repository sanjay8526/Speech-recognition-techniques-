import os
from pydub import AudioSegment
import speech_recognition as sr

def split_audio(file_path, chunk_length_ms=10000):
    """Split audio into fixed-length chunks (default: 10 seconds)."""
    audio = AudioSegment.from_wav(file_path)
    chunks = []

    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i + chunk_length_ms]
        chunk_name = f"chunk_{i // chunk_length_ms}.wav"
        chunk.export(chunk_name, format="wav")
        chunks.append((chunk_name, i // 1000))  # store start time in seconds

    return chunks

def transcribe_chunks(chunks):
    """Transcribe each audio chunk and return (time, text) pairs."""
    recognizer = sr.Recognizer()
    results = []

    for file, start_time in chunks:
        with sr.AudioFile(file) as source:
            audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"[{start_time}s] {text}")
            results.append((start_time, text))
        except sr.UnknownValueError:
            print(f"[{start_time}s] ❌ Couldn’t understand audio")
        os.remove(file)  # clean up chunk file

    return results

def search_keyword(transcripts, keyword):
    """Search keyword in transcripts."""
    return [(t, txt) for t, txt in transcripts if keyword.lower() in txt.lower()]

def main():
    file_path = "example.wav"  # replace with your .wav file
    if not os.path.exists(file_path):
        print(f"File
