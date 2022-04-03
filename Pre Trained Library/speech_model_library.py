import speech_commands as sp
from ubinascii import a2b_base64, b2a_base64

data = a2b_base64('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')
sp.init(data)
labels = ["Right","LightOn","LightOff","[OTHER]"]
feature = bytearray(732)

def predict(audio):
    result = sp.predict(audio, 0, 0)
    return (labels[result // 1000], result % 1000)

def snapshot():
    global feature
    sp.export_mfcc(feature)

def save(label):
    with open('samples.txt', 'ab') as f:
        f.write(b'{"label": "')
        f.write(label.encode())
        f.write(b'", "mfcc": "')
        f.write(b2a_base64(feature)[:-1])
        f.write(b'"},\n')
