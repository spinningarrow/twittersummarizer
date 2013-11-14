function doPoll(jobKey, callback){
	var waiting = true

	$('.loading').removeClass('hidden')

    $.get('/java_result/' + jobKey)
    	.done(function(data, textStatus, jqXHR) {

    		if (jqXHR.status === 202) {
    			waiting = true
    		}

    		else if (jqXHR.status === 200) {
    			waiting = false
        		callback(data);  // process results here
        		$('.loading').addClass('hidden')
    		}
    	})
    	.always(function () {
    		if (waiting) {
    			setTimeout(function () {
    				doPoll(jobKey, callback)
    			}, 5000)
    		}
    	})
}

$(document).ready(function () {
	// Show/hide the loading indicator on Ajax
	$(document)
		/*.ajaxStart(function () {
			$('.loading').removeClass('hidden')
		})
		.ajaxStop(function () {
			$('.loading').addClass('hidden')
		})*/

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
		}, function (data, status, xhr) {

			if (status !== "success") {
				return
			}

			var jobKey = data
			$('.loading').removeClass('hidden')

			doPoll(jobKey, function (data) {
				// Convert JSON result to a JS object
				var resultObject = $.parseJSON(data)

				// Loop through the positive and negative results and add them
				// to the HTML
				var $ul = $("#query-results-positive").find('.list').empty()

				for (var i = 0; i < resultObject.positive.length; i++) {
					$ul.append("<li>" + resultObject.positive[i] + "</li>")
				}

				$ul = $("#query-results-negative").find('.list').empty()

				for (var i = 0; i < resultObject.negative.length; i++) {
					$ul.append("<li>" + resultObject.negative[i] + "</li>")
				}

				$('.container.main').addClass('results-loaded')
				$('.query-results').hide().removeClass('hidden').fadeIn('slow')
			})
		})
	})
})