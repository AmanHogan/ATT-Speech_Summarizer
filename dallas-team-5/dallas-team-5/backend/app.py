from flask import Flask, jsonify, request
import src.ml.create_prediction as create_prediction
import src.ml.summarize_text as summarize_text
import src.helper.get_client_data as get_client_data
import shutil
import src.loggers.logger as logger
import sys
sys.dont_write_bytecode = True


CLIENT_PRED_PATH = "./db/predictions/client-predictions.txt"
RAW_CLIENT_PRED_PATH = "./db/predictions/client-recommendation-db.csv"
CLIENT_DATA_PATH = "./db/training/client-data.csv"
UPLOAD_PATH = "../uploads/"
files = [CLIENT_PRED_PATH, RAW_CLIENT_PRED_PATH, CLIENT_DATA_PATH]

app = Flask(__name__)

@app.route('/run_python', methods=['GET'])

def run_python():
    summarize_text.summarizeText()
    get_client_data.initClientData()
    create_prediction.initializeModel()

    for f in files:
        shutil.copy(f, UPLOAD_PATH)
    
    logger.logData("Succesfully copied all files to uploads folder")

    resp = jsonify(success=True)
    return resp

if __name__ == '__main__':
    app.run(debug=True)