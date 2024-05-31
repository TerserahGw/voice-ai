import io
from flask import Flask, request, send_file
import requests
from deep_translator import GoogleTranslator

app = Flask(__name__)

def fetch_voice(text, id, lang='ja', format='mp3', length=1, noise=0.25, noisew=0.4, max=75, streaming='true'):
    translated_text = GoogleTranslator(source='auto', target=lang).translate(text)
    api_url = (
        f'https://artrajz-vits-simple-api.hf.space/voice/vits?text={translated_text}&id={id}&format={format}&lang={lang}'
        f'&length={length}&noise={noise}&noisew={noisew}&max={max}&streaming={streaming}'
    )
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.content
    else:
        response.raise_for_status()

@app.route('/hutao', methods=['GET'])
def fetch_hutao_voice_route():
    text = request.args.get('text')
    if text:
        voice_data = fetch_voice(text, id=176)
        voice_bytes_io = io.BytesIO(voice_data)
        voice_bytes_io.seek(0)
        return send_file(
            voice_bytes_io,
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name='output.mp3'
        )
    else:
        return "Text parameter is missing.", 400

@app.route('/raiden', methods=['GET'])
def fetch_raiden_voice_route():
    text = request.args.get('text')
    if text:
        voice_data = fetch_voice(text, id=182)
        voice_bytes_io = io.BytesIO(voice_data)
        voice_bytes_io.seek(0)
        return send_file(
            voice_bytes_io,
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name='output.mp3'
        )
    else:
        return "Text parameter is missing.", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
