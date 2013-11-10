from flask import Flask, render_template, json
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

# Return mock data for styling web app properly
@app.route("/javamock", methods=['POST'])
def javamock():
	result = {
		"positive": [
			"I love it",
			"It's amazing",
			"Awesome!",
			"So thin!",
			"So light!",
			"Perfect!"
		],
		"negative": [
			"Where's the bezel?",
			"So expensive",
			"Google is better",
			"I hate it"
		]
	}
	return json.dumps(result)

if __name__ == "__main__":
	app.run()