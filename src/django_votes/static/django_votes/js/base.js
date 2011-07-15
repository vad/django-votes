$(function(){
    load();
    
    function load(){
        $('.django-votes').each(function(){
            var id = $(this).attr('x:id');
            var model_name = $(this).attr('x:model-name');
            var result_url = $(this).attr('x:url');
        
            $(this).find('.vote-up').live('click', function(){
                alert('ok');
                var url = $(this).attr('x:url');
        
                $.ajax({type:'POST',
                        url: url,
                        data: {'model': model_name, 'object_id': id},
                        success : loadResults});
        
                return false;
            });
            $(this).find('.vote-down').live('click', function(){
                var url = $(this).attr('x:url');
        
                $.ajax({type:'POST',
                        url: url,
                        data: {'model': model_name, 'object_id': id},
                        success : loadResults});
        
                return false;
            });
            
            function loadResults(data) {
                $('.django-votes').replaceWith(data);
                $('.vote-results').slideDown();
                load();
            }
        });
    }    
})();