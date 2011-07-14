$(this).find('.django-votes').each(function(){
    var id = $(this).attr('x:id');
    var model_name = $(this).attr('x:model-name');
    var result_url = $(this).attr('x:url');

    $(this).find('.vote-up').live('click', function(){
        var url = $(this).attr('x:url');

        $.ajax({type:'POST',
                url: url,
                data: {'model': model_name, 'object_id': id},
                success : function() {
                    $('.vote-results').load(result_url);
                    $('.vote-results').slideDown();
                }});

        return false;
    });
    $(this).find('.vote-down').live('click', function(){
        var url = $(this).attr('x:url');

        $.ajax({type:'POST',
                url: url,
                data: {'model': model_name, 'object_id': id},
                success : function() {
                    $('.vote-results').load(result_url);
                    $('.vote-results').slideDown();
                }});

        return false;
    });
});