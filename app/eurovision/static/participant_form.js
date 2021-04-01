$participantForm = $('#participant_form');
$participantSelect = $('#participant_select');
$addParticipantBtn = $('#add_participant_btn');
$updateParticipantBtn = $('#update_participant_btn');
$deleteParticipantBtn = $('#delete_participant_btn');

$participantSelect.on('change',function(){
    if ($participantSelect.val()=='add_new_participant'){
        window.location.href='/eurovision/manage/participants'
    }else{
        window.location.href=`/eurovision/manage/participants/${$participantSelect.val()}`
    }
})

$addParticipantBtn.on('click',function(){
    $participantForm.attr('action','/eurovision/manage/participant/new')
    $participantForm.submit()
})

$updateParticipantBtn.on('click',function(){
    $participantForm.attr('action',`/eurovision/manage/participants/${$participantSelect.val()}/update`)
    $participantForm.submit()
})

$deleteParticipantBtn.on('click',function(){
    $participantForm.attr('action',`/eurovision/manage/participants/${$participantSelect.val()}/delete`)
    $participantForm.submit()
})



