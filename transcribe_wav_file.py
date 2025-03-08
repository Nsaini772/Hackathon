from google.cloud import speech


import wave

with wave.open("audio_sample.wav", "rb") as wav_file:
    sample_rate = wav_file.getframerate()
    print("Sample rate: {sample_rate}")


client = speech.SpeechClient.from_service_account_file("credit.json")


def transcribe_audio(input_file):
    with open(input_file, 'rb') as audio_file: 
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz = sample_rate,
            language_code = "en-US"
        )
        response = client.recognize(config=config,audio=audio)
        for result in response.results:
            print(f'Transcript: {result.alternatives[0].transcript}')
            print(f'Confidence: {result.alternatives[0].confidence}')
    return response


transcribe_audio('audio_sample.wav')