/********************************************************************
------------------------ Check Email Address ------------------------
********************************************************************/

async function checkEnteredEmailAddressAvailable(email) {
	if (!preliminaryValidateEmailAddress(email)) {
		updateEmailLabelBadgeClear();
		return;
	}
	const response = await checkServerForEmailAddress(email);
	if (response.valid === false) {
		updateEmailLabelBadgeInvalid();
	}
	else if (response.available === false && email !== current_email) {
		updateEmailLabelBadgeUnavailable();
	}
	else {
		updateEmailLabelBadgeAvailable();
	}
}

function preliminaryValidateEmailAddress(email) {
	const validateAt = email.indexOf('@') >= 1;
	const validatePeriod = email.indexOf('.', email.indexOf('@')) > email.indexOf('@');
	const validateSuffix = email.length > email.indexOf('.', email.indexOf('@')) + 2;
	return validateAt && validatePeriod && validateSuffix;
}

async function checkServerForEmailAddress(email) {
	const response = await axios.get('/api/check-email', { params: { email_address: email } });
	return response.data;
}

function updateEmailLabelBadgeAvailable() {
	const $emailAddressAvailable = $('#email_address_available');
	$emailAddressAvailable.text('Available');
	$emailAddressAvailable.addClass('bg-success');
	$emailAddressAvailable.removeClass('bg-danger');
}

function updateEmailLabelBadgeUnavailable() {
	const $emailAddressAvailable = $('#email_address_available');
	$emailAddressAvailable.text('Unavailable');
	$emailAddressAvailable.removeClass('bg-success');
	$emailAddressAvailable.addClass('bg-danger');
}

function updateEmailLabelBadgeInvalid() {
	const $emailAddressAvailable = $('#email_address_available');
	$emailAddressAvailable.text('Invalid');
	$emailAddressAvailable.removeClass('bg-success');
	$emailAddressAvailable.addClass('bg-danger');
}

function updateEmailLabelBadgeClear() {
	const $emailAddressAvailable = $('#email_address_available');
	$emailAddressAvailable.text('');
	$emailAddressAvailable.removeClass('bg-success');
	$emailAddressAvailable.removeClass('bg-danger');
}

/********************************************************************
------------------------ Check Username ------------------------
********************************************************************/

async function checkEnteredUsernameAvailable(username) {
	if (!validateUsername(username)) {
		updateUsernameLabelBadgeClear();
		return;
	}
	const response = await checkServerForUsername(username);
	if (!response && username !== current_username) {
		updateUsernameLabelBadgeUnavailable();
	}
	else {
		updateUsernameLabelBadgeAvailable();
	}
}

function validateUsername(username) {
	const validateLength = username.length >= 6 && username.length <= 25;
	return validateLength;
}

async function checkServerForUsername(username) {
	const response = await axios.get('/api/check-username', { params: { username: username } });
	return response.data.available;
}

function updateUsernameLabelBadgeAvailable() {
	const $usernameAvailable = $('#username_available');
	$usernameAvailable.text('Available');
	$usernameAvailable.addClass('bg-success');
	$usernameAvailable.removeClass('bg-danger');
}

function updateUsernameLabelBadgeUnavailable() {
	const $usernameAvailable = $('#username_available');
	$usernameAvailable.text('Unavailable');
	$usernameAvailable.removeClass('bg-success');
	$usernameAvailable.addClass('bg-danger');
}

function updateUsernameLabelBadgeClear() {
	const $usernameAvailable = $('#username_available');
	$usernameAvailable.text('');
	$usernameAvailable.removeClass('bg-success');
	$usernameAvailable.removeClass('bg-danger');
}

/********************************************************************
-------------------------- When DOM Loads ---------------------------
********************************************************************/

const current_email = $('#current_email').val();
const current_username = $('#current_username').val();

const $emailAddress = $('#email_address');
$emailAddress.keyup(function() {
	checkEnteredEmailAddressAvailable($emailAddress.val());
});

const $username = $('#username');
$username.keyup(function() {
	checkEnteredUsernameAvailable($username.val());
});
