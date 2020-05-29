window.onload = function() {

    var chartCtx = document.getElementById('color').getContext('2d');
    chart = new Chart(chartCtx, {
	// The type of chart we want to create
	type: 'bar',
	label: "Color",
	// The data for our dataset
	data: {
	    labels: ['Gray scale', 'Colored'],
	    datasets: [
		{
		    label: 'Test',
		    backgroundColor: 'rgb(34, 145, 32)',
		    borderColor: 'rgb(120, 45, 149)',
		    barThickness: 'flex',
		    barPercentage: 1.0,
		    data: [2089, 5871]
		}
		,
		{
		    label: 'Train',
		    backgroundColor: 'rgb(255, 99, 132)',
		    borderColor: 'rgb(255, 99, 132)',
		    barThickness: 'flex',
		    barPercentage: 1.0,
		    data: [8270, 17091]
		}
	    ]
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

    var chartCtx = document.getElementById('size').getContext('2d');
    chart = new Chart(chartCtx, {
	// The type of chart we want to create
	type: 'bubble',
	label: "Image Size",
	// The data for our dataset
	data: {
	    datasets: [
	    	{
		    label: 'Test',
		    backgroundColor: 'rgb(34, 145, 32)',
		    borderColor: 'rgb(120, 45, 149)',
		    barThickness: 'flex',
		    barPercentage: 1.0,
		    data: [
			{x: 1050, y: 700, r: 7},
			{x: 1050, y: 600, r: 3},
			{x: 1050, y: 525, r: 2},
			{x:  700, y: 500, r: 1},
			{x: 1050, y: 450, r: 3}			
		    ]
		}
		,
		{
		    label: 'Train',
		    backgroundColor: 'rgb(255, 99, 132)',
		    borderColor: 'rgb(255, 99, 132)',
		    barThickness: 'flex',
		    barPercentage: 1.0,
		    data: [
			{x: 1050, y: 700, r: 18},
			{x: 1050, y: 600, r: 14},
			{x: 1050, y: 525, r: 7},
			{x:  700, y: 500, r: 3},
			{x: 1050, y: 450, r: 8}
		    ]
		}
	    ]
	},
	
	// Configuration options go here
	options: {
	    scales: {
		yAxes: [{
		    scaleLabel: {
			labelString: "Height",
			display: true}
		    ,
		    ticks: {
			min: 0
		    }
		}],
		xAxes: [{
		    scaleLabel: {
			labelString: "Width",
			display: true}
		    ,
		    ticks: {
			min: 0
		    }
		}]
	    }
	}
    });
};
