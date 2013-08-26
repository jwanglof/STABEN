$(document).ready(function() {
	$('#errorMessages').hide();
	$('.no_javascript').hide();
	$('#blog_comments').hide();
	$('#blog_pictures').hide();

	$('#blog_show_pictures').click(function() {
		$('#blog_comments').hide();
		if ($('#blog_pictures').is(':visible')) {
			$('#blog_pictures').hide();
			$('#blog_show_pictures').text('Visa bilderna');
		}
		else {
			$('#blog_comments').hide();
			$('#blog_pictures').show(100);
			$('#blog_show_pictures').text('Göm bilderna');
		}
	});

	$('#blog_show_comments').click(function() {
		$('#blog_pictures').hide();
		if ($('#blog_comments').is(':visible')) {
			$('#blog_comments').hide();
			$('#blog_show_comments').text('Visa kommentarer');
		}
		else {
			$('#blog_pictures').hide();
			$('#blog_comments').show(100);
			$('#blog_show_comments').text('Göm kommentarer');
		}
	});

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

	$('#school_program').ready(function() {show_school_class();});
	$('#school_program').change(function() {show_school_class();});

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

    $(function() {
        var elem = $("#chars_upload");
        $("#description_upload").limiter(200, elem);
    });

    $(function() {
        var elem = $("#chars_album_info");
        $("#description_album_info").limiter(50, elem);
    });

    $('#datepicker').datetimepicker({
        weekStart: 1,
        pickTime: false
    });
});

function show_school_class() {
	var chosen_school_program = $('#school_program').children(':selected').val();
	var select_objects = new Array();
	var selected;

	$('#school_class').children('option').each(function() {
		var school_class_program = $(this).val().split('|')[1];

		// if ($(this).is(':selected') && school_class_program == chosen_school_program) {
		// 	selected = $(this);
		// }

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

	// If the array has more than 1 element it will selected the correct option
	if (select_objects.length > 1) {
		for (var i = 0; i < select_objects.length; i++)
			if ($(select_objects[i]).val() == $('#default_class').val())
				$(select_objects[i]).prop('selected', true);
	}
	else {
		// Select the first HTML object in the array
		$(select_objects[0]).prop('selected', true);
	}
}