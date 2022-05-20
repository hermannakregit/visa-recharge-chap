// World Map GDP
$(function(){
	$('#world-map-gdp').vectorMap({
		map: 'world_mill_en',
		zoomOnScroll: false,
		series: {
			regions: [{
				values: gdpData,
				scale: ['#4266b2', '#e5e8f2'],
				normalizeFunction: 'polynomial'
			}]
		},
		backgroundColor: '#f0f4f9',
		onRegionTipShow: function(e, el, code){
			el.html(el.html()+' (GDP - '+gdpData[code]+')');
		}
	});
});