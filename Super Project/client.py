from picamera import PiCamera
import pygame
import pyaudio
import boto3
import wave
import RPi.GPIO as GPIO
import threading
from tempfile import gettempdir
from contextlib import closing
import subprocess
import os
import sys
import time

__author__  = "Satya Mehta"
__copyright__ = "Copyright (C) 2019 by Satya Mehta"

sampling_rate = 48000
chunk = 2 
device = 2 
audio = pyaudio.PyAudio()
frames = []



def capture_image():
    """
    capture_image: Captures an image using Picamera
    """
    camera.capture('image.jpg')
    
def upload_to_s3(filename= None):
    """
    upload_to_s3: Uploads an image 
    """
    s3 = boto3.client("s3")
    s3.upload_file("/home/pi/Desktop/EID/Final_Project/image.jpg", "my-wand-project", "image.jpg")
    

def detect_labels():
    """
    detect_labels: Fetches images from the s3 bucket and provides AWS Reko to recognize image
    return: Returns label name.
    """
    reko = boto3.client('rekognition', region_name = "us-east-1")
    response = reko.detect_labels(Image={'S3Object':{'Bucket':"my-wand-project",'Name':"image.jpg"}},
        MaxLabels=10)
    for label in response['Labels']:
        print("Labels : " + label['Name'])
        print("Confidence" + str(label['Confidence']))
        if int(label['Confidence']) >= 50:
            return label['Name']

def text_to_speech(text):
    """
    text_to_speech: Uses AWS Polly service to convert text to speech and saves it into speech.mp3 file
    Uses pymixer to play the audio
    """
    session = boto3.Session(region_name = "us-east-1")
    polly = session.client("polly", region_name = "us-east-1")
    try:
        response = polly.synthesize_speech(Text=text, OutputFormat="mp3",
                                        VoiceId="Joanna")
    except (BotoCoreError, ClientError) as error:
        print(error)
        sys.exit(-1)
    
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output = "speech.mp3"

            try:
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                print(error)
                sys.exit(-1)
    else:
        print("Could not stream audio")
        sys.exit(-1)
      
    #subprocess.call(['xdg-open', output])
    pygame.mixer.music.load("speech.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

def record():
    """
    record: Records an Audio, uses PyAudio to record the audio. 
    """
    print("Record")
    print("Starting record")
    stream = audio.open(format = pyaudio.paInt16,rate = sampling_rate ,channels = 1, \
                    input_device_index = device,input = True, \
                    frames_per_buffer=chunk)
  
    for i in range(0,int((sampling_rate/chunk)*3)):
        data = stream.read(chunk,exception_on_overflow=False)
        if i % 3 == 0:
           frames.append(data)
    print("finished recording")
    stream.stop_stream()
    stream.close()
    
def queue_send(message_body, value="default", name = "Voice"):
    """
    queue_send: Sends the message on to the SQS Queue.
    """
    sqs = boto3.client("sqs", region_name = "us-east-1")
    queue_url = "https://sqs.us-east-1.amazonaws.com/996000685317/wand_queue"
    message_attrib =  {name : {'DataType' : 'String', 'StringValue':value}}
    response = sqs.send_message(QueueUrl = queue_url, MessageBody =
                                str(message_body), MessageAttributes = message_attrib, DelaySeconds = 1)
    print(response['MessageId'])
   
#Using transcribe   
def speech_to_text():
    """
    speech_to_text: Converts speech to text. Uses AWS transcribe service
    """
    link = "https://s3.us-east-1.amazonaws.com/my-wand-project/test1.wav"
    trans = boto3.client("transcribe", region_name="us-east-1")
    try:
        response = trans.delete_transcription_job(TranscriptionJobName="output")
    except:
        pass
    response = trans.start_transcription_job(
        TranscriptionJobName="output",
        LanguageCode='en-US',
        MediaFormat='wav',
        MediaSampleRateHertz = 44100,
        Media={
            'MediaFileUri': link
        },
        Settings={
            'ShowSpeakerLabels': True,
            'MaxSpeakerLabels': 8
        }
    )
    print(response)
    
def aws_lex():
    """
    aws_lex: Used to convert speech to text using AWS lex service
    """
    lex = boto3.client('lex-models', region_name = "us-east-1")
    response = lex.get_bot(name = "mybot", versionOrAlias="satya")
    lex_run = boto3.client('lex-runtime', region_name = "us-east-1")
    wavefile = wave.open('test1.wav')
    response = lex_run.post_content(botName = "mybot", botAlias = "satya", contentType = "audio/l16;rate=16000; channels=1", \
                                    accept = "text/plain; charset=utf-8",\
                                    inputStream = wavefile.readframes(96044), userId = "satya")
    return response['ResponseMetadata']['HTTPHeaders']['x-amz-lex-message']

def create_wav_file(wave_file_name):
    """
    create_wav_file: Creates .wav file with 16000 sampling rate
    """
    wavefile = wave.open(wave_file_name,'wb')
    wavefile.setnchannels(1)
    wavefile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wavefile.setframerate(16000)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()

def gpio_callback(channel,shutdown):
    """
    gpio_callback: Thread which is invoked and works after GPIO event detection.
    
    """
    while True:
        if GPIO.event_detected(channel):
            GPIO.remove_event_detect(channel)
            record()
            create_wav_file("test1.wav")
            text = aws_lex()
            print(text)
            if text == "identify":
                queue_send(message_body="voice", value = "1", name = "name")
                capture_image()
                upload_to_s3()
                new_label = detect_labels()
                if new_label is not None:
                    text_to_speech(new_label+ "!!")
                    queue_send(message_body=new_label, value = "1", name = "name")
                    print("Correct or wrong? recording will start in 3 seconds")
                    time.sleep(3)
                    record()
                    create_wav_file("test2.wav")
                    new_text = aws_lex()
                    if new_text == "correct":
                        queue_send(message_body="voice", value = "1", name = "name")
                    elif new_text == "wrong":
                        queue_send(message_body = "voice", value = "1", name = "name")
                    else:
                        queue_send(message_body = "voice", value = "0", name = "name")
            else:
                queue_send(message_body="voice", value = "0", name = "name")
            GPIO.add_event_detect(channel, GPIO.FALLING)
        if GPIO.event_detected(shutdown):
            print("Safe Shutdown")
            break

        
channel = 4
shutdown = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(shutdown, GPIO.IN, pull_up_down=GPIO.PUD_UP)
print("GPIO",GPIO.input(channel))
GPIO.add_event_detect(channel, GPIO.FALLING)
GPIO.add_event_detect(shutdown, GPIO.FALLING)
camera = PiCamera()
pygame.mixer.init()
t1 = threading.Thread(target = gpio_callback, args = (channel,shutdown, ))
t1.start()
t1.join()   