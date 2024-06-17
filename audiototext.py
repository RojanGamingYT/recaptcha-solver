import speech_recognition as sr
from pydub import AudioSegment
from colorama import Fore, init
import os

def convert():
    try:
        mp3_file_path = "audio.wav"
        print(Fore.CYAN +"Converting Audio to WAV...")
        audio = AudioSegment.from_file(mp3_file_path, format="mp3")
        wav_file_path = mp3_file_path.replace('.mp3', '.wav')
        audio.export(wav_file_path, format="wav")
        print(Fore.CYAN +f"Converted to WAV: {wav_file_path}")
 
        import os
        if not os.path.exists(wav_file_path):
            raise Exception("WAV file was not created successfully.")

        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_file_path) as source:
            print(f"{Fore.YELLOW}Reading WAV file...{Fore.RESET}")
            audio_data = recognizer.record(source)
            print(f"{Fore.YELLOW}Recognizing text...{Fore.RESET}")
            text = recognizer.recognize_google(audio_data)
            print(f"{Fore.YELLOW}Text recognized. {Fore.RESET}{Fore.GREEN}({text}){Fore.RESET}")
            result = text
            return result

    except sr.UnknownValueError:
        print(Fore.RED +"Error: Unknown audio format or corrupted file.")
    except sr.RequestError as e:
        print(Fore.RED +"Error: Could not request results from Google Speech Recognition service; {0}".format(e))
    except Exception as e:
        print(Fore.RED +"Error: {0}".format(e))