$().ready(function() {
    
    $('form.toggle_form').bind('submit', function() {
        var form = $(this);
        $.post(form.attr('action'), form.serialize(), function(data) {
            var fulfilled = form.find('input.fulfilled').val();0
            form.find('button').toggleClass('fulfilled');
            form.find('button span').html((fulfilled == 'true') ? 'Show Post' : 'Hide Post');
            form.find('input.fulfilled').val((fulfilled == 'true') ? 'false' : 'true');
        });
        return false;
    });
    
});