import io

from alexa_client import AlexaClient
import pyaudio
import datetime
import uuid
from audioplayer import AudioPlayer

write = True
buffer = io.BytesIO()


def callback(in_data, frame_count, time_info, status):
    buffer.write(in_data)
    return in_data, pyaudio.paContinue


p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    stream_callback=callback,
)

client = AlexaClient(
    client_id='',
    secret='',
    refresh_token='',
)

try:
    stream.start_stream()

    client.connect()
    while True:
        print('listening. Press CTRL + C to exit, enter to proceed')
        result = input()
        print('sending and waiting for answer...')
        for i, directive in enumerate(client.send_audio_file(buffer)):
            print(directive.name + ' ' + str(datetime.datetime.now()))
            if directive.name in ['Speak', 'Play']:
                buffer = io.BytesIO()
                name = uuid.uuid4()
                f = open(f'./output_{name}.mp3', 'wb')
                f.write(directive.audio_attachment)
                f.close()

                try:
                    print('playing...\n')
                    player = AudioPlayer(f'./output_{name}.mp3')
                    player.play(block=True)
                    player.close()
                except:
                    pass

finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
