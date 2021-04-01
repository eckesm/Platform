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
    email=document.querySelector('#email_address').value
    localStorage.setItem('email_address',email)
}

/********************************************************************
-------------------------- When DOM Loads ---------------------------
********************************************************************/

checkForRememberedUser()

const form = document.querySelector('#login_form');
form.addEventListener('submit',()=>{
    saveUserCredentialsInLocalStorage()
})