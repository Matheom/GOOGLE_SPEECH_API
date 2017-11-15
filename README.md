# GOOGLE_SPEECH_API

This repository contains an example of how to use the google speech API with a large MP3 file

This work can be done either from your own laptop, or within the Google Cloud Shell inside Google Console. I would recommend using the latter, since the speech API does not (in my experience) ingest larger files.

The first step is to download a podcast from the 702 website. This can be done from the shell using the following command (you can choose your own podcast)

wget -O 20171005.mp3 http://omnystudio.com/d/clips/5dcefa8e-00a9-4595-8ce1-a4ab0080f142/1ecba37a-6d83-4ee9-a295-a57100b7f2df/b1215d79-d875-4862-8890-a8030130aebe/audio.mp3?utm_source=Podcast&in_playlist=e3347658-6eee-44e2-bf81-a57100b92442

You can then upload it into Cloud Storage with the following command. Remember to create a bucket first, and then reference it

gsutil cp 20171005.mp3 gs://your-bucket-name/

Now you have the mp3 file in your bucket, and in your console shell.

Next, you need to enable the Google Speech API, and create a key. THe documentation suggests you should create a service acocunt key
u from your bucket into you cloud shell with the following command

gsutil cp gs://your-bucket-name/apikey.json ~/your-shell-folder

Now you should have both the apikey and the mp3 file in your shell directory. The documentation states you should write the following command to ensure the credentials are used when making the api call

export GOOGLE_APPLICATION_CREDENTIALS=apikey.json

The next step is to alter the file type - the documentation suggests changing file types to either .flac or .raw. Appparently they are cleaner than mp3 files. Who would have known?

In addition, the documentation explains that for files longer than a minute, you are required to use Asynchronous recognition (https://cloud.google.com/speech/docs/basics). I found my python script did not work, even though the length of the audio was less than 80 minutes. This may have something to do with the file being in excess of 700mbs. I got 'resource exhausted; when I tried

In this case, i divided up the mp3 file into smaller segments using ffmpeg. I tried with 58 second snippets, which worked. I then tried for a bit longer - 5 minutes, which worked. I suppose it could go longer, but for this exmaple I am going to stick with 5 minute segments. I use the following command to split the file. The 300 refers to how long eah segment will be, you can chop and change as you wish

ffmpeg -i filename.mp3 -f segment -segment_time 300 -c copy out%03d.mp3

Now that we have divided the file up into manageable chunks, let's convert one of them into a flac file

ffmpeg -i file.mp3 -c:v libx264 file.flac

I found that some of the files turned out to be 2 channels, while others were one. Not sure why the chunks came out different? I used ffmpeg again to force the flac file into 1 channel, since that is the foormat required by the google speech api

ffmpeg -i file.flac -ac 1 file_mono.flac

Finally, I export this into cloud storage

gsutil file.flac gs://your-bucket-name/

Now that all is seemingly in order, we write the python script, the easy part

