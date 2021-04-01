$countryForm = $('#country_form');
$countrySelect = $('#country_select');
$countryId = $('#country_id');
$addCountryBtn = $('#add_country_btn');
$updateCountryBtn = $('#update_country_btn');
$deleteCountryBtn = $('#delete_country_btn');

$countrySelect.on('change',function(){
    if ($countrySelect.val()=='add_new_country'){
        window.location.href='/eurovision/manage/countries'
    }else{
        window.location.href=`/eurovision/manage/countries/${$countrySelect.val()}`
    }
})

$addCountryBtn.on('click',function(){
    $countryForm.attr('action','/eurovision/manage/country/new')
    $countryForm.submit()
})

$updateCountryBtn.on('click',function(){
    $countryId.prop('disabled',false)
    $countryForm.attr('action',`/eurovision/manage/countries/${$countrySelect.val()}/update`)
    $countryForm.submit()
})

$deleteCountryBtn.on('click',function(){
    $countryId.prop('disabled',false)
    $countryForm.attr('action',`/eurovision/manage/countries/${$countrySelect.val()}/delete`)
    $countryForm.submit()
})



