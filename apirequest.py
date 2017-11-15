#make sure you have install the speech package. You can use sudo pip install googe-cloud-speech

from google.cloud import speech

client = speech.SpeechClient()

#note the hertz - raw files require different rates. YOu can check the rate by viewing the header of your audio file

operation = client.long_running_recognize(
audio=speech.types.RecognitionAudio(uri='gs://your-bucket-name/file.flac',),config=speech.types.RecognitionConfig(encoding='FLAC',language_code='en-US',sample_rate_hertz=44100,),)
op_result = operation.result()
for result in op_result.results:
    for alternative in result.alternatives:
         print('='*20)
         print(alternative.transcript)
         print(alternative.confidence)
