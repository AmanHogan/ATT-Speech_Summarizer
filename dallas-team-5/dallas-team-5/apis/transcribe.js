process.env.GOOGLE_APPLICATION_CREDENTIALS = "./key/key.json";
import * as speech from '@google-cloud/speech';
import * as fs from 'fs';

// Function: Sends API call to Google services to transcribe first audio found in upload folder.
// Params: None
// Returns: String value of transcribed audio
async function transcribeAudio()
{
    // Get path of audio file
    const filename = './uploads/' + fs.readdirSync('./uploads/')[0];
    console.log('Uploaded file to be transcribed: ' + filename);

    const client = new speech.SpeechClient();
    const file = fs.readFileSync(filename);
    const audioBytes = file.toString('base64');

    // Configure request
    const audio = {
        content: audioBytes
    };

    const config = {
        encoding: 'LINEAR16',
        languageCode: 'en-US',
        enableAutomaticPunctuation: true,
    };

    const request = {
        audio: audio,
        config: config
    };

    // Retrieve first transciption in response
    const [response] = await client.recognize(request);
    const transcription = response.results.map(result => result.alternatives[0].transcript).join('\n');
    
    return transcription;
}
export default transcribeAudio;
