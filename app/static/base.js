/********************************************************************
----------------------- Responding to Invitations -------------------
********************************************************************/

async function respond_invitation(invite_id, group_id, api_token, reply, invitation) {
	data = {
		reply   : reply,
		api_token : api_token
	};
	const response = await axios.patch(`/api/invitations/${invite_id}`, data);
	console.log(response.data.status);
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
			window.location.href = '/user/home';
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
	const api_token = $(this).data('api_token');
	const invitation = $(this).parent().parent();
	respond_invitation(invite_id, group_id, api_token, 'accept', invitation);
});

$('.reject_invitation').click(function() {
	const invite_id = $(this).data('invite_id');
	const group_id = $(this).data('group_id');
	const api_token = $(this).data('api_token');
	const invitation = $(this).parent().parent();
	respond_invitation(invite_id, group_id, api_token, 'reject', invitation);
});

$('#logout_button').click(function() {
	$('#logout_form').submit();
});
