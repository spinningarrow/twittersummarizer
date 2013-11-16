from flask import Flask, json, render_template, request, Response
from subprocess import check_output
import analyser

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def hello():
	return render_template("layout.html")

@app.route("/java", methods=['POST', 'GET']) # remove GET later
def java():
	query = request.form['query']
	result = check_output(["java", "-jar", "TwitterNLP.jar", "data/database.db", query])
	# return Response(dumps(result), status=200, mimetype='application/json')
	app.logger.debug('Finished Java work, moving on to sentiment analysis...')

	result_list = result.split("\n")
	classifications = analyser.getClassifiedDictionary(result_list)
	# classifications = {
	# 	'positive': result_list[:10],
	# 	'negative': result_list[10:20]
	# }

	app.logger.debug('Finished sentiment analysis.')

	return json.dumps(classifications)

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