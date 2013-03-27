$(document).ready(function() {
	$('#profile_edit').validate({
		rules: {
			firstname: 'required',
			lastname: 'required'

		},
		messages: {
			firstname: 'Skriv ditt förnamn',
			lastname: 'Skriv ditt efternamn'
		},
		submitHandler: function(form) {
			form.submit()
		}
	});

	$('.school_mate').click(function() {
		var id = $(this).attr('id');
		var div = $('#' + id + '.school_mate_info');
		if ($(div).is(":visible")) {
			$(div).hide();
			$('#collapsed' + id).text('Tryck för mer info');
		}
		else {
			$(div).show();
			$('#collapsed' + id).text('Tryck för att dölja info');
		}
	});
});

