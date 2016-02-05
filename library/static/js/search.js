function search() {
		if ( this.value.length < 3 ) { return; }
		$.ajax({
				url: SEARCH_URL + '?q=' + this.value,
				dataType: 'jsonp', success: function(r) {
						$('#results').empty();
						for (var i = 0; i < r.length; i++) {
								var option = document.createElement('option');
								option.id = r[i]; option.value = r[i];
								$('#results').append(option);
						}
				}
		});
}

function get_id(){ return $('#results').find('option[value="'+$('#search').val()+'"]').attr('id'); }

$(document).ready(function() {
		$('#search').on('keyup',search);
		$('#search').change(function() { $('#search').val(get_id()); });
});
