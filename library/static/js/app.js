function filterChange( e ){
	var l={}; $.each( $(e.target).val(), function(i,v){
		var z=v.split('/'); if(l[z[0]]){l[z[0]].push(z[1]);}else{l[z[0]]=[z[1]];}
	}); window.videosearch.filters=l; console.log( window.videosearch.filters );
	doSearch();
}

function doSearch(){
	$.ajax({
		type: "POST", url: '/library/search', contentType: "application/json",
		beforeSend: function(r){ r.setRequestHeader("X-CSRFToken", getCookie('csrftoken')); },
		data: JSON.stringify( window.videosearch ),
		success: function(r){
			console.log( r );
		}
	});
}

function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1)); break;
			}
		}
	}
	return cookieValue;
}

$(document).ready(function(){
	window.videosearch = { filters: {}, terms: [] };
	$("#search").select2({
		width: 'resolve',
		allowClear: true,
		minimumInputLength: 3,
		placeholder: 'Filter by...',
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
			dataType: 'json', delay: 250, url: '/library/search',
			data: function(data){ return { q: data.term }; },
			processResults: function(data,params){
				$.each( data.items, function(i,v){ v.id=data.article+'/'+v._id; v.text=v.name; });
				return { results: data.items };
			}
		},
	}).on('change',filterChange);
});
