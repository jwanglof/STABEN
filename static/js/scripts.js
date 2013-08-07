$(document).ready(function() {
	$('#errorMessages').hide();
	$('.no_javascript').hide();

	$('#profile_edit').validate({
		errorLabelContainer: $("#errorMessages"),
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

	$('#school_program').change(function() {
		var chosen_school_program = $('#school_program').children(':selected').val();
		var select_objects = new Array();

		$('#school_class').children('option').each(function() {
			var school_class_program = $(this).val().split('|')[1];

			// Hide all options
			$(this).hide();
			if (school_class_program == chosen_school_program) {
				// Show the correct school class option(s)
				$(this).show();
				
				// Add all HTML objects to the array
				// If there are more than one class for a program
				// the select-list will always choose the first one
				select_objects.push(this);
			}
		});

		// Select the first HTML object in the array
		$(select_objects[0]).prop('selected', true);
	});

	$('#school_class').change(function() {
		$('#school_class option:selected').each(function() {
			var school_program_id = $(this).val().split('|')[1]
			// Hide all IDs that are not chosen
			// $('#school_class option').hide()
		});
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

	$('.admin_student_poll_show_hide').click(function() {
		if ($('.admin_student_poll_q_w_a_content').is(':visible')) {
			$('.admin_student_poll_q_w_a_content').hide();
			$('.admin_student_poll_show_hide').text('Press to uncollapse!')
		}
		else {
			$('.admin_student_poll_q_w_a_content').show();
			$('.admin_student_poll_show_hide').text('Press to collapse!')
		}
	});
});