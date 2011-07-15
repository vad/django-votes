$(function(){
    load();
    
    function load(){
        $('.updownvotes').each(function(){
            var id = $(this).attr('x:id');
            var model_name = $(this).attr('x:model-name');
            var result_url = $(this).attr('x:url');
        
            $(this).find('.vote-up').live('click', function(){
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
                $('.updownvotes').replaceWith(data);
                $('.vote-results').slideDown();
                load();
            }
        });
    }    
    
    $('.rating').each(function(){    
        $(this).find('.star').each(function(){
            $(this).click(function(){
                var parent = $(this).parent();
                var static_url = parent.attr('x:static-url');                
                var index = $(this).attr('x:index');                
                var gray = static_url + 'django_votes/img/gray_star.png';
                var yellow = static_url + 'django_votes/img/star.png';
                
                parent.find('.star').each(function(){
                    var idx = $(this).attr('x:index');
                    if (idx <= index)
                    {
                        $(this).attr('src', yellow);
                    }      
                    else
                    {
                        $(this).attr('src', gray);
                    }              
                });                
                                                            
                return false;
            });
        });           
    });
});