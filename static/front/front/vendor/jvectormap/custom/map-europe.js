// Europe
$(function(){
	$('#mapEurope').vectorMap({
		map: 'europe_mill',
		zoomOnScroll: false,
		series: {
			regions: [{
				values: gdpData,
				scale: ['#4266b2', '#e5e8f2'],
				normalizeFunction: 'polynomial'
			}]
		},
		backgroundColor: '#f0f4f9',
	});
});