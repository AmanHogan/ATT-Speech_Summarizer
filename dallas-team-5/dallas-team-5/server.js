
import express from 'express';
import multer from 'multer';
import path from 'path';
import fs, { readFile } from 'fs';
import transcribeAudio  from './apis/transcribe.js';
import synthesize from './apis/speech.js';
import fetch from 'node-fetch'

// =============== CONSTANTS =============== //
const app = express();
const PORT_NUMBER = 3000;

// =============== LOCAL STORAGE =============== //
var storage = multer.diskStorage({
        destination: './uploads/',
        filename: function ( req, file, cb ) {cb( null, "client" + "-" + file.originalname);}
    }
);

// =============== APP CONFIG =============== //
const upload = multer( { storage: storage } );
app.use(express.static('public'));
app.use('/downloads', express.static('uploads'));
app.set('view engine', 'ejs');
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
globalThis.fetch = fetch

// =============================== ROUTES =============================== //

// =============== FRONT END =============== //
app.get('/user', (req, res) => { res.render("user") });
app.get('/drive-mode', (req, res) => { res.render('drive-mode') });
app.get('/client', (req, res) => { res.render('client') });
app.get('/jobs', (req, res) => 
{
    var summarizedText;
    var transcribedText;
    var clientPredictionText;
    var clientRecommendationText

    fs.readdir('uploads/', (err, files) => 
    {
        if (err) { res.status(500).send('Error reading files'); return; }
        for (var i = 0; i < files.length; i++)
        {
            if(String(files[i]).includes("call-summary-text.txt")){summarizedText = fs.readFileSync('uploads/'+ files[i], 'utf8');}
            if(String(files[i]).includes("call-transcription.txt")){transcribedText = fs.readFileSync('uploads/'+ files[i], 'utf8');}
            if(String(files[i]).includes("client-predictions.txt")){clientPredictionText = fs.readFileSync('uploads/'+ files[i], 'utf8');}
            if(String(files[i]).includes("client-recommendation.txt")){clientRecommendationText = fs.readFileSync('uploads/'+ files[i], 'utf8');}
        }
        res.render('jobs', {summarizedText: summarizedText, clientRecommendationText: clientRecommendationText});
    });
});
app.get('/admin', (req, res) => 
{
    var summarizedText;
    var transcribedText;
    var clientPredictionText;
    var clientRecommendationText

    fs.readdir('uploads/', (err, files) => 
    {
        if (err) {res.status(500).send('Error reading files');return;}
        for (var i = 0; i < files.length; i++)
        {
            if(String(files[i]).includes("call-summary-text.txt")) {summarizedText = fs.readFileSync('uploads/'+ files[i], 'utf8');}
            if(String(files[i]).includes("call-transcription.txt")){transcribedText = fs.readFileSync('uploads/'+ files[i], 'utf8');}
            if(String(files[i]).includes("client-predictions.txt")){clientPredictionText = fs.readFileSync('uploads/'+ files[i], 'utf8');}
            if(String(files[i]).includes("client-recommendation.txt")){clientRecommendationText = fs.readFileSync('uploads/'+ files[i], 'utf8');}
        }
        res.render('admin', { files: files , summarizedText: summarizedText, transcribedText:transcribedText, clientPredictionText:clientPredictionText, clientRecommendationText: clientRecommendationText});
    });
});

// =============================== UPLOAD ENDPOINT =============================== //
app.post("/upload_files", upload.array("files"), async (req, res) => {
   
    req.files[0].filename = req.files[0].originalname;
    req.files[0].path = req.files[0].destination + req.files[0].filename;

    // Speech to Text  API call //
    const transcribedText = await transcribeAudio().catch(console.error);;
    console.log(`The transcribed text: ${transcribedText}`);
    fs.writeFile('./uploads/call-transcription.txt', transcribedText, (err) => {if (err) throw err;})

    // Python Backend //
    try { const callPythonScripts = await callPython(); res.status(200).send('Success'); } 
    catch (error) { console.error('Error calling Python function:', error); res.status(500).send('Error occurred while calling Python function');}

    // Text to Speech API call //
    let summarizedText = "";
    fs.readdir('uploads/', (err, files) => 
    {
        if (err) {res.status(500).send('Error reading files');return;}
        for (var i = 0; i < files.length; i++)
        {
            if(String(files[i]).includes("call-summary-text.txt")) {summarizedText = fs.readFileSync('uploads/'+ files[i], 'utf8');}
        }
        synthesize(summarizedText);
    });
});

// =============== BACK END  =============== //
async function callPython() {
    const response = await fetch('http://localhost:5000/run_python');
    if (response.ok) { console.log('Successfully ran python code'); } 
    else { throw new Error(`Error calling Python function: ${response.statusText}`); }
}

app.listen(PORT_NUMBER);