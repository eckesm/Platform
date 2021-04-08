/********************************************************************
----------------------- Responding to Invitations -------------------
********************************************************************/

async function respond_invitation(invite_id, group_id, reply, invitation) {
	headers = {
		Authorization : 'Bearer ' + localStorage.getItem('access_token')
	};
	data = {
		reply   : reply
	};
	const response = await axios.patch(`/api/invitations/${invite_id}`, data, { headers: headers });
	const status = response.data.status;
	const message = response.data.message;

	if (status === 'successful') {
		invitation.remove();
		adjust_invitation_dropdown();
	}
	alert(message);

	if (reply === 'accept') {
		const new_group = `/groups/${group_id}`;
		window.location.href = new_group;
	}
	if (reply === 'reject') {
		const check_current_location = `/groups/${group_id}`;
		if (window.location.pathname === check_current_location) {
			window.location.href = '/home';
		}
	}
}

function adjust_invitation_dropdown() {
	let $invitations = $('.invitation_item');
	let invitationsCount = $invitations.length;
	if (invitationsCount === 0) {
		$('#invitations_dropdown').remove();
	}
	else {
		$('#invitations_badge').text(invitationsCount);
	}
}

/********************************************************************
-------------------------- When DOM Loads ---------------------------
********************************************************************/

$('.accept_invitation').click(function() {
	const invite_id = $(this).data('invite_id');
	const group_id = $(this).data('group_id');
	const invitation = $(this).parent().parent();
	respond_invitation(invite_id, group_id, 'accept', invitation);
});

$('.reject_invitation').click(function() {
	const invite_id = $(this).data('invite_id');
	const group_id = $(this).data('group_id');
	const invitation = $(this).parent().parent();
	respond_invitation(invite_id, group_id, 'reject', invitation);
});

$('#logout_button').click(function(e) {
	e.preventDefault()
	localStorage.removeItem('access_token')
	$('#logout_form').submit();
});
