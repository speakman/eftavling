$(document).ready(function() {
    $('a[rel=external]').each(function(index) { 
	this.target = "_blank";
    });

    $('#choices > li.dummy').remove();

    $("ul").sortable({
	connectWith: 'ul'
    });
    
    $('#choices').bind('sortreceive', function(event, ui) {
	/* The list seem to temporary contain one additional 
	   item at this stage */
	if ($('#choices > li').length >= 4) {
	    $(ui.sender).sortable('cancel');
	    alert("Du kan bara rösta på tre bidrag.");
	    return;
	}

	$(ui.item).effect('highlight', {}, 1000);
    });
    
    $("#choices, #entries").disableSelection();

    $('#next').click(function() {
	if ($('#choices > li').length != 3) {
	    alert("Du måste lägga exakt tre röster.");
	    return;
	}

	var votes = [];
	$('#choices > li').each(function(index) {
	    votes.push($(this).attr('id'));
	});

	$('input[name=votes]').val(votes.join('&'));
	$('#voteform').submit();
    });
});
