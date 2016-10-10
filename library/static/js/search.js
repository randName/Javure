function textChange(){
	if ( this.value == window.videosearch.text ) return;
	window.videosearch.text = this.value;
	setTimeout( doSearch, 50 );
}

function filterChange( e ){
	var l={}; $.each( $(e.target).val(), function(i,v){
		var z=v.split('/'); if(l[z[0]]){l[z[0]].push(z[1]);}else{l[z[0]]=[z[1]];}
	}); window.videosearch.filters = l;
	setTimeout( doSearch, 50 );
}

function actsChange( e ){
	window.videosearch.advanced.min_acts = e[0];
	window.videosearch.advanced.max_acts = e[1];
	setTimeout( doSearch, 50 );
}

function dursChange( e ){
	window.videosearch.advanced.min_runtime = e[0];
	window.videosearch.advanced.max_runtime = e[1];
	setTimeout( doSearch, 50 );
}

function advChange(){
	var mtm = window.videosearch.advanced.m2m_or;
	if( ! mtm ){ mtm = {}; }
	mtm[this.value] = $(this).is(':checked');
	window.videosearch.advanced.m2m_or = mtm;
	setTimeout( doSearch, 50 );
}

function dateChange( sd, ed )
{
	if( !sd && !ed ){
		delete window.videosearch.advanced.max_date;
		delete window.videosearch.advanced.min_date;
	} else {
		window.videosearch.advanced.min_date = [ sd.year(), sd.month()+1, sd.date() ];
		window.videosearch.advanced.max_date = [ ed.year(), ed.month()+1, ed.date() ];
	}
	setTimeout( doSearch, 50 );
}

function doSearch(){
	if ( ! window.videosearch.text && $.isEmptyObject(window.videosearch.filters) ) return;
	$('#results').html(''); window.videosearch.page = 0; fetchResults();
}

function fetchResults(){
	var vs = window.videosearch;
	if( vs.per_page != window.display.per_page ){
		window.videosearch.per_page = window.display.per_page;
		$('#results').html(''); window.videosearch.page = 1;
	} else if( window.resultcount && vs.page*vs.per_page >= window.resultcount ){
		return 0;
	} else {
		window.videosearch.page += 1;
	}
	$.ajax({
		type: "POST", url: SEARCH_URL, contentType: "application/json",
		beforeSend: function(r){ r.setRequestHeader("X-CSRFToken", CSRFTOKEN); },
		data: JSON.stringify( window.videosearch ),
		success: function(r){ window.resultcount=r.count; displayResults(r.items); }
	});
	return window.videosearch.page;
}

function shorten( l, s ){
	if ( s.length > l ) return s.substring(0,l) + '...';
	return s;
}

function renderItem( v ){
	var title, link = VIDEO_URL+v.name;
	var i = $('<div class="grid-item"/>');

	if ( window.display.layout == 'masonry' ){
		title = shorten( 30, v.title );
		var t = $('<a/>').attr('href',link).attr('title',title);
		if( window.darken ){ t.addClass('darken'); }
		t.append($('<img class="img-responsive"/>').attr('src',MEDIA_URL+'?v='+v.pk+'&s=ps'));
		$('<div class="text-center"/>').text(v.name).appendTo(t);
		return i.html(t);
	} else {
		title = shorten( 40, v.title );
		return i.html($('<a/>').attr('href',link).text(title));
	}
}

function displayResults( r ){
	$('#results').isotope({
		itemSelector: '.grid-item',
		layoutMode: window.display.layout,
		masonry: { columnWidth: 150 }
	}).imagesLoaded().progress( function() { $('#results').isotope('layout'); });

	$.each( r, function(i,v){ $('#results').append(renderItem( v )) });
	$(window).on( 'scroll', scrollLoad );
	return r.length;
}

function flat(v){ return v; }

function scrollLoad(){
	if( $(window).scrollTop() + $(window).height() > $(document).height()-10 ){
		$(window).off('scroll'); setTimeout( fetchResults, 500 );
	}
}

$(document).ready(function(){
	window.display = { layout: 'masonry', per_page: 24 }
	window.videosearch = { advanced: {},  filters: {}, text: '' };
	$('#search').on('keyup',textChange);
	$("#filter").select2({
		width: 'resolve',
		allowClear: true,
		minimumInputLength: 2,
		placeholder: '  Filter by...',
		escapeMarkup: function(markup){ return markup; },
		templateSelection: function(item){ return item.name || item.id  },
		templateResult: function(data){
			if (data.loading) return data.text;
			var rt = $("<div/>").text(data.name+' ');
			if (data.count) $("<span class='badge'/>").html(data.count).appendTo(rt);
			if (data.alias) $("<span class='a_alias'/>").text(data.alias).prepend(' ').appendTo(rt);
			return rt;
		},
		ajax: {
			dataType: 'json', delay: 250, url: SEARCH_URL,
			data: function(data){ return { term: data.term }; },
			processResults: function(data,params){
				$.each( data.items, function(i,v){ v.id=v.article+'/'+v._id; v.text=v.name; });
				return { results: data.items };
			}
		},
	}).on('change',filterChange);

	$(document).on( 'change', ':checkbox', advChange );

	var acts_slide = document.getElementById('acts');
	noUiSlider.create( acts_slide, {
		range:{ 'min': 0, 'max': 20 },
		start: [ 0, 20 ], step: 1, connect: true,
		format: { to: flat, from: flat },
		pips: { mode: 'count', values: 5, density: 4 }
	});
	acts_slide.noUiSlider.on('change', actsChange );

	var durs_slide = document.getElementById('durs');
	noUiSlider.create( durs_slide, {
		range:{ 'min': 0, '12.5%': 60, '50%': 240, '75%': 480, 'max': 960, },
		start: [ 0, 960 ], step: 1, connect: true,
		format: { to: flat, from: flat },
		pips: { mode: 'count', values: 9, density: 3 }
	});
	durs_slide.noUiSlider.on('change', dursChange );

	$('#daterange').daterangepicker({
		opens: "left",
		autoUpdateInput: false,
		linkedCalendars: false,
		alwaysShowCalendars: true,
		locale: { format: 'DD/MM/YYYY' },
		ranges: {
			'Recent': [moment().subtract(6,'days'), moment().endOf('year')],
			'This Month': [moment().startOf('month'), moment().endOf('month')],
			'This Year': [moment().startOf('year'), moment().endOf('year')],
			'Post-2010': [moment([2010,0,1]), moment().endOf('year')],
		}
	}, dateChange);
	$('#daterange').on('cancel.daterangepicker',function(e,p){$(this).val('');dateChange(0,0);});
	$('#daterange').on('apply.daterangepicker',function(e,p){
		$(this).val(p.startDate.format('D/M/YY')+' to '+p.endDate.format('D/M/YY'));
	});

	window.darken = true;
	$(document).ready(function(){
		$('#darken').click(function(){
			$(this).toggleClass('active');
			$('a').toggleClass('darken');
			window.darken = ! window.darken;
		});
	});
});
