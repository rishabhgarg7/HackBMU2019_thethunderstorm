import pyttsx3
data='hey alok how are you'
print(data)
engine = pyttsx3.init()
engine.say(data)
engine.setProperty('rate',120)
engine.setProperty('volume', 0.9)
engine.runAndWait()