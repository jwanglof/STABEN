$(document).ready(function() {
	$('#errorMessages').hide();
	$('.no_javascript').hide();

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

	$('#register_form').validate({
		errorLabelContainer: $("#errorMessages"),
		rules: {
			// firstname: 'required',
			// lastname: 'required',
			email: {
				required: true,
				email: true
			},
			password: 'required',
			rep_password: {
				equalTo: '#password'
			},
			regCode: 'required'
		},
		messages: {
			// firstname: 'Ditt förnamn är obligatoriskt.',
			// lastname: 'Ditt efternamn är obligatoriskt.',
			email: 'Din e-mail är obligatoriskt och måste vara korrekt.',
			password: 'Ange ditt lösenord',
			rep_password: 'Lösenorden matchar inte',
			regCode: 'Din unika registreringskod måste skrivas in. Denna ska du ha fått i posten.'
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

