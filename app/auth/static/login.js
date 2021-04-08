async function login(email_address, password) {
	data = {
		email_address : email_address,
		password      : password
	};
	const response = await axios.post('/login', data);

	status = response['data']['status'];
	message = response['data']['message'];
	if (status == 'success') {
		access_token = response['data']['access_token'];
		localStorage.setItem('access_token', access_token);
		
        redirect_url=$('#next').val()
        if (redirect_url){
		    window.location.href = redirect_url;
        } else {
		    window.location.href = '/home';
        }
	}
	else {
		// Submit form in order to trigger form validation responses.
		$('#login_form').submit();
	}
}

/** Check for saved user information in localStorage.
 * - If user information exists, populate login form with saved username of last user.
 * - Will need to make async function once API and database are used for logging in.
 */
function checkForRememberedUser() {
	const email = localStorage.getItem('email_address');
	if (!email) return false;

	document.querySelector('#email_address').value = email;
}

/** Save email address used to log in to localStorage
 */
function saveUserCredentialsInLocalStorage() {
	email = document.querySelector('#email_address').value;
	localStorage.setItem('email_address', email);
}

/********************************************************************
-------------------------- When DOM Loads ---------------------------
********************************************************************/

checkForRememberedUser();

$('#login_submit').on('click', function(e) {
	e.preventDefault();
	saveUserCredentialsInLocalStorage();
	login($('#email_address').val(), $('#password').val());
});
