$entryForm = $('#entry_form');
$entrySelect = $('#entry_select');
$addEntryBtn = $('#add_entry_btn');
$updateEntryBtn = $('#update_entry_btn');
$deleteEntryBtn = $('#delete_entry_btn');

$entrySelect.on('change',function(){
    if ($entrySelect.val()=='add_new_entry'){
        window.location.href='/eurovision/manage/entries'
    }else{
        window.location.href=`/eurovision/manage/entries/${$entrySelect.val()}`
    }
})

$addEntryBtn.on('click',function(){
    $entryForm.attr('action','/eurovision/manage/entry/new')
    $entryForm.submit()
})

$updateEntryBtn.on('click',function(){
    $entryForm.attr('action',`/eurovision/manage/entries/${$entrySelect.val()}/update`)
    $entryForm.submit()
})

$deleteEntryBtn.on('click',function(){
    $entryForm.attr('action',`/eurovision/manage/entries/${$entrySelect.val()}/delete`)
    $entryForm.submit()
})



