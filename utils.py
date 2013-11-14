from subprocess import check_output
from flask import json
import analyser

def get_describing_phrases(query):
	result = check_output(["java", "-jar", "TwitterNLP.jar", "data/database.db", query])
	result_list = result.split("\n")

	# app.logger.debug('Finished Java work, moving on to sentiment analysis...')
	classifications = analyser.getClassifiedDictionary(result_list)

	# app.logger.debug('Finished sentiment analysis.')

	return json.dumps(classifications)