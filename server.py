from flask import Flask, render_template, request, flash, send_file
import os, subprocess

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
            
        #subprocess.call('python3 main.py -a', shell=True)
        return send_file('videos/truncate.mp4', as_attachment=True)

app.run('0.0.0.0')