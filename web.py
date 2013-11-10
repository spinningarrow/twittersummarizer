from flask import Flask
from subprocess import check_output
app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello world!"

@app.route("/java")
def java():
	result = check_output(["java", "-cp", "'*'", "-jar", "TwitterNLP.jar", "data/SampleSet1_POS.txt", "models/SerializedModel4"])
	# return Response(dumps(result), status=200, mimetype='application/json')
	return result

if __name__ == "__main__":
	app.run()