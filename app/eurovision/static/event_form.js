$eventForm = $('#event_form');
$eventSelect = $('#event_select');
$addEventBtn = $('#add_event_btn');
$updateEventBtn = $('#update_event_btn');
$deleteEventBtn = $('#delete_event_btn');

$eventSelect.on('change',function(){
    if ($eventSelect.val()=='add_new_event'){
        window.location.href='/eurovision/manage/events'
    }else{
        window.location.href=`/eurovision/manage/events/${$eventSelect.val()}`
    }
})

$addEventBtn.on('click',function(){
    $eventForm.attr('action','/eurovision/manage/event/new')
    $eventForm.submit()
})

$updateEventBtn.on('click',function(){
    $eventForm.attr('action',`/eurovision/manage/events/${$eventSelect.val()}/update`)
    $eventForm.submit()
})

$deleteEventBtn.on('click',function(){
    $eventForm.attr('action',`/eurovision/manage/events/${$eventSelect.val()}/delete`)
    $eventForm.submit()
})



