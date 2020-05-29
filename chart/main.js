window.onload = function() {

    var chartCtx = document.getElementById('forChart').getContext('2d');
    chart = new Chart(chartCtx, {
	// The type of chart we want to create
	type: 'bar',
	label: "Color",
	// The data for our dataset
	data: {
	    labels: ['Gray scale', 'Colored'],
	    datasets: [
		{
		    label: 'Train',
		    backgroundColor: 'rgb(255, 99, 132)',
		    borderColor: 'rgb(255, 99, 132)',
		    barThickness: 'flex',
		    barPercentage: 1.0,
		    data: [8270, 17091]
		},
		{
		    label: 'Test',
		    backgroundColor: 'rgb(34, 145, 32)',
		    borderColor: 'rgb(120, 45, 149)',
		    barThickness: 'flex',
		    barPercentage: 1.0,
		    data: [2089, 5871]
		}]
	},
	
	// Configuration options go here
	options: {
	    scales: {
		yAxes: [{
		    ticks: {
			min: 0
		    }
		}]
	    }
	}
    });
};
