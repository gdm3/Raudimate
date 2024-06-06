from flask import Flask, render_template, request, flash
import os

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
        return 'Submitted'

app.run('0.0.0.0')