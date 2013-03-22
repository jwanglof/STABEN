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
});

