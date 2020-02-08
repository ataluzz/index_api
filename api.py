from flask import Flask, abort, render_template, request, send_file
import defs

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
@app.route('/statsapi', methods=['GET', 'POST'])
def path_input_page():
	return render_template('home.html')

@app.route('/result', methods=['POST'])
def show_result():
	path = request.form['path']
	extensions = request.form['extensions'].split(", ")
	word = request.form['word']
	result = defs.whole_stats(path, *extensions, word=word)
	return render_template('result.html', result=result)

app.run()
