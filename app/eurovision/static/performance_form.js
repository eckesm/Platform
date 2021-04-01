$performanceForm = $('#performance_form');
$performanceSelect = $('#performance_select');
$addPerformanceBtn = $('#add_performance_btn');
$updatePerformanceBtn = $('#update_performance_btn');
$deletePerformanceBtn = $('#delete_performance_btn');

$performanceSelect.on('change',function(){
    if ($performanceSelect.val()=='add_new_performance'){
        window.location.href='/eurovision/manage/performances'
    }else{
        window.location.href=`/eurovision/manage/performances/${$performanceSelect.val()}`
    }
})

$addPerformanceBtn.on('click',function(){
    $performanceForm.attr('action','/eurovision/manage/performance/new')
    $performanceForm.submit()
})

$updatePerformanceBtn.on('click',function(){
    $performanceForm.attr('action',`/eurovision/manage/performances/${$performanceSelect.val()}/update`)
    $performanceForm.submit()
})

$deletePerformanceBtn.on('click',function(){
    $performanceForm.attr('action',`/eurovision/manage/performances/${$performanceSelect.val()}/delete`)
    $performanceForm.submit()
})



