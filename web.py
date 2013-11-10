from flask import Flask, render_template
from subprocess import check_output
app = Flask(__name__)

@app.route("/")
def hello():
	return render_template("layout.html")

@app.route("/java", methods=['POST'])
def java():
	result = check_output(["java", "-cp", "'*'", "-jar", "TwitterNLP.jar", "data/SampleSet1_POS.txt", "models/SerializedModel4"])
	# return Response(dumps(result), status=200, mimetype='application/json')
	return result

if __name__ == "__main__":
	app.run()