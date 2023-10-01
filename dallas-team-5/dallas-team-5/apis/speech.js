process.env.GOOGLE_APPLICATION_CREDENTIALS = "./backend/key/key.json";
import * as textToSpeech from '@google-cloud/text-to-speech';
import * as fs from 'fs';
import * as util from 'util';

/**
 * Function: Sythesizes sample text into an .mp3 file.
 * Params: The text to be synthesized
 * Returns: None
 */
async function synthesize(text) {
    const client = new textToSpeech.TextToSpeechClient();

    const request = {
        input: { text: text },
        voice: { languageCode: 'en-US', ssmlGender: 'NEUTRAL' },
        audioConfig: { audioEncoding: 'MP3' },
    };

    const [response] = await client.synthesizeSpeech(request);
    // Write the binary audio content to a local file
    const writeFile = util.promisify(fs.writeFile);
    await writeFile('./uploads/call-summary-audio.mp3', response.audioContent, 'binary');
    console.log('Audio content written to file: call-summary-audio.mp3');
}

export default synthesize;