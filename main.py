from flask import Flask, request, send_file, render_template_string
import requests
from deep_translator import GoogleTranslator

app = Flask(__name__, template_folder='.')

def fetch_voice(text, id=176, format='mp3', lang='ja'):
    translated_text = GoogleTranslator(source='auto', target=lang).translate(text)
    api_url = f'https://keilasenpai-smple-api.hf.space/voice/vits?text={translated_text}&id={id}&format={format}&lang={lang}'
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.content
    else:
        response.raise_for_status()

@app.route('/')
def index():
    return render_template_string('''
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Text to Voice</title>
    </head>
    <body>
      <h1>Text to Voice Converter</h1>
      <form action="/hutao" method="post">
        <label for="text">Enter text:</label><br><br>
        <textarea id="text" name="text" rows="4" cols="50"></textarea><br><br>
        <input type="submit" value="Submit">
      </form>
    </body>
    </html>
    ''')

@app.route('/hutao', methods=['POST'])
def fetch_voice_route():
    text = request.form['text']
    voice_data = fetch_voice(text)
    return send_file(
        io.BytesIO(voice_data),
        mimetype='audio/mpeg',
        as_attachment=True,
        download_name='output.mp3'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
