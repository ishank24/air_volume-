from flask import Flask, render_template_string, request
import subprocess

app = Flask(__name__)

HTML_CODE = '''
<!DOCTYPE html>
<html>
  <head>
    <title>GESTURE CONTROL SYSTEM</title>
    <style>
      body {
        background-color: #2c3e50;
        font-family: Arial, sans-serif;
        color: #ffffff;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
      }
      .button-container {
        background-color: #ecf0f1;
        padding: 20px;
        border-radius: 5px;
        margin-bottom: 20px;
      }
      button {
        background-color: #e67e22;
        color: #ffffff;
        border: none;
        padding: 10px 20px;
        font-size: 14px;
        cursor: pointer;
        margin: 0 10px;
      }
      #camera-feed {
        width: 640px;
        height: 480px;
        background-color: #000000;
        display: none;
      }
    </style>
  </head>
  <body>
    <div class="button-container">
      <button onclick="runFile('BrightnessControl.py')">Control Brightness</button>
      <button onclick="runFile('Volcontrol.py')">Control Volume</button>
    </div>
    <video id="camera-feed" autoplay></video>
    <script>
      function runFile(fileName) {
        fetch('/run_file', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ file_name: fileName })
        })
        .then(response => response.text())
        .then(data => {
          console.log(data);
          startCamera();
        })
        .catch(error => console.error(error));
      }

      function startCamera() {
        navigator.mediaDevices.getUserMedia({ video: true })
          .then(stream => {
            const videoElement = document.getElementById('camera-feed');
            videoElement.srcObject = stream;
            videoElement.style.display = 'block';
          })
          .catch(error => console.error('Error accessing camera:', error));
      }
    </script>
  </body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_CODE)

@app.route('/run_file', methods=['POST'])
def run_file():
    file_name = request.get_json()['file_name']
    try:
        subprocess.Popen(["python", file_name])
        return f"Running {file_name}"
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)