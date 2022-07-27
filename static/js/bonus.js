var url = "http://localhost:27017/covid_db";


d3.csv(
	url,
	function(err, rows) {
		function unpack(rows, key) {
			return rows.map(function(row) {
				return row[key];
			});
		}

		var data = [
			{
				type: "scattermapbox",
				text: unpack(rows, "Confirmed"),
				lon: unpack(rows, "Long"),
				lat: unpack(rows, "Lat"),
				marker: { color: "fuchsia", size: 4 }
			}
		];

		var layout = {
			dragmode: "zoom",
			mapbox: { style: "open-street-map", center: { lat: 38, lon: -90 }, zoom: 3 },
			margin: { r: 0, t: 0, b: 0, l: 0 }
		};

		Plotly.newPlot("myDiv", data, layout);
	}
);


init();