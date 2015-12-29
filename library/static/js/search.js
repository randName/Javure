function search() {
		if ( this.value.length < 3 ) { return; }
		$.ajax({
				url: 'http://pxy.randna.me:8080/ajax?q=' + this.value,
				dataType: 'jsonp', success: function(r) {
						$('#results').empty();
						for (var i = 0; i < r.length; i++) {
								var option = document.createElement('option');
								option.id = r[i][0]; option.value = r[i][1];
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
