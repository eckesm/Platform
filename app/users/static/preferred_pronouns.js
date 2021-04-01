function update_pronoun_inputs(subject, object) {
	$subject.val(subject);
	$object.val(object);
}

function select_pronoun_radio() {
	if ($subject.val() === 'he' && $object.val() === 'him') {
		$('input:radio[name=pronouns]')[0].checked = true;
	}
	else if ($subject.val() === 'she' && $object.val() === 'her') {
		$('input:radio[name=pronouns]')[1].checked = true;
	}
	else if ($subject.val() === 'they' && $object.val() === 'them') {
		$('input:radio[name=pronouns]')[2].checked = true;
	}
	else {
		$('input:radio[name=pronouns]')[3].checked = true;
	}
}

/********************************************************************
-------------------------- When DOM Loads ---------------------------
********************************************************************/

const $pronouns0 = $('#pronouns-0');
const $pronouns1 = $('#pronouns-1');
const $pronouns2 = $('#pronouns-2');
const $pronouns3 = $('#pronouns-3');
const $subject = $('#subject_pronoun');
const $object = $('#object_pronoun');

$pronouns0.click(function() {
	update_pronoun_inputs('he', 'him');
});
$pronouns1.click(function() {
	update_pronoun_inputs('she', 'her');
});
$pronouns2.click(function() {
	update_pronoun_inputs('they', 'them');
});
// $pronouns3.click(function(){
//     update_pronoun_inputs('','')
// })
$subject.keydown(function() {
	$('input:radio[name=pronouns]')[3].checked = true;
});
$object.keydown(function() {
	$('input:radio[name=pronouns]')[3].checked = true;
});

window.addEventListener('load', event => {
	select_pronoun_radio();
});


