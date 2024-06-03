from flask import Flask, render_template, request, flash

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
        return 'Submitted'

app.run('0.0.0.0')