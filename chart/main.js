/**
 * Flag value to set whether dummy data should be used.
 * 
 * Note that using the real data drastically increases the loading
 * time. Moreover, the dummy data is loaded and plotted while the
 * real data is loading asynchronously.
 */
window.useDummyData = false;

function createCharts() {
	let data = window.data == undefined || window.useDummyData ? window.dummy : window.data;

	var chartCtx = document.getElementById('color').getContext('2d');
	chart = new Chart(chartCtx, {
		// The type of chart we want to create
		type: 'bar',
		label: "Color",
		// The data for our dataset
		data: {
			labels: ['Gray scale', 'Colored'],
			datasets: [{
				label: 'Test',
				backgroundColor: 'rgb(34, 145, 32)',
				borderColor: 'rgb(120, 45, 149)',
				barThickness: 'flex',
				barPercentage: 1.0,
				data: data.color.test,
			}, {
				label: 'Train',
				backgroundColor: 'rgb(255, 99, 132)',
				borderColor: 'rgb(255, 99, 132)',
				barThickness: 'flex',
				barPercentage: 1.0,
				data: data.color.train,
			}]
		},
		
		// Configuration options go here
		options: {
			scales: {
				yAxes: [{
					ticks: { min: 0 }
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
			datasets: [{
				label: 'Test',
				backgroundColor: 'rgb(34, 145, 32)',
				borderColor: 'rgb(120, 45, 149)',
				barThickness: 'flex',
				barPercentage: 1.0,
				data: data.sizes.test,
			}, {
				label: 'Train',
				backgroundColor: 'rgb(255, 99, 132)',
				borderColor: 'rgb(255, 99, 132)',
				barThickness: 'flex',
				barPercentage: 1.0,
				data: data.sizes.train,
			}]
		},
		
		// Configuration options go here
		options: {
			scales: {
				yAxes: [{
					scaleLabel: {
						labelString: "Height",
						display: true
					},
					ticks: { min: 0 }
				}],
				xAxes: [{
					scaleLabel: {
						labelString: "Width",
						display: true
					},
					ticks: { min: 0 }
				}]
			}
		}
	});
};

function processClasses(csv) {

}

function processColor(csv) {
	let parsed = Papa.parse(csv[0], { header: true });

	let result = {
		test: [0, 0],
		train: [0, 0],
	};

	console.log("Parsing colors...");

	for (row of parsed.data) {
		result[row.Dataset][row.Colored === 'True' ? 1 : 0] = parseInt(row.Frequency);
	}

	return result;
}

function processSizes(csv) {
	const result = {};
	const datasetNames = ['train', 'test'];

	console.log("Parsing image sizes...");

	for (var i = 0; i < csv.length; i++) {
		let parsed = Papa.parse(csv[i], { header: true });

		result[datasetNames[i]] = []

		var maxFreq = 0;

		for (row of parsed.data) {
			let freq = parseInt(row.Frequency);
			if (!freq) continue;
		
			maxFreq = maxFreq < freq ? freq : maxFreq;

			result[datasetNames[i]].push({
				x: parseInt(row.Width),
				y: parseInt(row.Height),
				r: 2 // parseInt(row.Frequency),
			});
		}

		/**
		 * Code for rescaling proportionally to the maximum value using the rescale factor.
		 */
		// const rescaleFactor = 15;
		// for (row of result[datasetNames[i]])
		// 	row.r = parseInt(row.r * rescaleFactor / maxFreq);
	}

	return result;
}

/**
 * Asynchronously loads data from the CSV files and triggers the `callback`
 * 	when it finishes.
 *
 * @param {Function} callback 
 */
async function loadData(callback) {
	const data = {
		classes: {
			filenames: ['classes.csv'],
			process: processClasses,
		},
		color: {
			filenames: ['color.csv'],
			process: processColor,
		},
		sizes: {
			filenames: ['tuple.train.csv', 'tuple.test.csv'],
			process: processSizes,
		},
		loaded: false,
	};

	window.data = data;

	for (type in data) {
		let responses = [];
		if (!data[type].filenames) continue;

		for (file of data[type].filenames) {
			console.log("Loading " + file + "...");
			const response = await $.ajax(file).promise();
			
			data.loaded = true;
			
			responses.push(response);
		}

		window.data[type] = data[type].process(responses);
	}

	if (data.loaded)
		callback();
}

function createDummyData() {
	return {
		classes: {
			train: [],
		},
		color: {
			test: [2089, 5871],
			train: [8270, 17091],
		},
		sizes: {
			test: [
				{x: 1050, y: 700, r: 7},
				{x: 1050, y: 600, r: 3},
				{x: 1050, y: 525, r: 2},
				{x:  700, y: 500, r: 1},
				{x: 1050, y: 450, r: 3}			
			],
			train: [
				{x: 1050, y: 700, r: 18},
				{x: 1050, y: 600, r: 14},
				{x: 1050, y: 525, r: 7},
				{x:  700, y: 500, r: 3},
				{x: 1050, y: 450, r: 8}
			],
		},
	};
}

function updateCharts() {
	if (!window.dummy)
		window.dummy = createDummyData();

	if (!window.data && !window.useDummyData)
		loadData(createCharts);

	// Create charts
	createCharts();
}

function build() {
	let dummyCheckbox = document.getElementById('dummyCheckbox');
	window.useDummyData = dummyCheckbox.checked;
	dummyCheckbox.onchange = (event) => {
		window.useDummyData = event.target.checked;
		updateCharts();
	}

	updateCharts();
}

window.onload = build;
