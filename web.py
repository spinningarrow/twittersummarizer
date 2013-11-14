from flask import Flask, json, render_template, request, Response
from subprocess import check_output
import analyser
from rq import Queue, get_current_job
from rq.job import Job
from worker import conn
from utils import get_describing_phrases

q = Queue(connection=conn)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def hello():
	return render_template("layout.html")

@app.route("/java", methods=['POST', 'GET']) # remove GET later
def java():
	query = request.form['query']
	job = q.enqueue(get_describing_phrases, query)

	return job.key

@app.route("/java_result/<job_key>", methods=['GET'])
def java_result(job_key):
	job_key = job_key.replace("rq:job:", "")
	job = Job.fetch(job_key, connection=conn)

	if(not job.is_finished):
		return "Not yet", 202
	else:
		return str(job.result), 200

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