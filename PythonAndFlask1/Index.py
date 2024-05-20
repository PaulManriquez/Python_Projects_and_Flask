from flask import Flask, render_template
'''
app = Flask(__name__)
@app.route('/')
def principal():
    return "HelloThere 22"

@app.route('/Contact')
def Contact():
    return "This is my contact"

'''
app = Flask(__name__)

@app.route('/')
def principal():
    return render_template('index.html')

@app.route('/Contact')
def Contact():
    return render_template('contact.html')

@app.route('/languages')
def Languages():
    MyLanguages = ("C","C++","Python","Linux")
    return render_template('languages.html',languages=MyLanguages)

if __name__ == '__main__':
    app.run(debug=True,port=8080) #debug=True is to re load each change to the file in real time