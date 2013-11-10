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
		$.post('/javamock', {
			query: query
		}, function (data, status, xhr) {

			if (status !== "success") {
				return
			}

			// Convert JSON result to a JS object
			var resultObject = $.parseJSON(data)

			// Loop through the positive and negative results and add them
			// to the HTML
			var $ul = $("#query-results-positive").find('.list')

			for (var i = 0; i < resultObject.positive.length; i++) {
				$ul.append("<li>" + resultObject.positive[i] + "</li>")
			}

			$ul = $("#query-results-negative").find('.list')

			for (var i = 0; i < resultObject.negative.length; i++) {
				$ul.append("<li>" + resultObject.negative[i] + "</li>")
			}

			// $('#query-results-positive').html(data);
		})
	})
})