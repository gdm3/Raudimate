from flask import Flask, render_template, request, flash, send_file
import os

def get_elapsed(): # Get elapsed time out of 100, 100 = done
    return 100

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        print(request.form['title'])
        print(request.form['body'])
        
        files = request.files['file']    
        files.save('utils/title.png')
        
        with open('utils/com.txt', 'w') as file:
            file.write(request.form['title'] + '\n')
            file.write(request.form['body'])
            
        os.system('python3 main.py -a')
        return 'submitted'

@app.route('/download-file/', methods=['GET'])
def download_files():
    if get_elapsed() == 100:
        return send_file('videos/truncate.mp4')
    return get_elapsed()
app.run('0.0.0.0')