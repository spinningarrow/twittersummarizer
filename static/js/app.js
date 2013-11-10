$(document).ready(function () {
	$('#form-main').submit(function (event) {
		// Don't actually submit the form
		event.preventDefault()

		// Get the user's query
		var query = $('#query').val()

		if (!query) {
			return
		}

		// Send the query to the Java method
		$.post('/java', {
			query: query
		}, function (data) {
			$('#query-results').html(data);
		})
	})
})