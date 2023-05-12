console.log('js file');

$(document).on("click",".js-toggle-modal", function(e){
    e.preventDefault()
    console.log('i was clicked')
    $('.js-modal').toggleClass("hidden");
})
.on("click",".js-submit", function (e) {
    e.preventDefault();
    console.log('submit me')
    const text = $('.js-post-text').val().trim();
    const $btn = $(this)


    if(!text.length){
        return false
    }
    $('.js-modal').addClass("hidden");
    $('.js-post-text').val('');
    
    $btn.prop("disabled",true).text('Posting!..');
    $.ajax({
        type: "POST",
        url: $('.js-post-text').data("post-url"),
        data: {text:text},
        success: function (response) {
            $('.js-modal').addClass("hidden");
            $('#posts-container').prepend(response);
            $btn.prop("disabled",false).text('New Post');
            $('.js-post-text').val('');
        },
        error:(error)=>{
            console.warn(error)
            $btn.prop("disabled",false).text('!!Error!!');
        }
    });
})
.on("click", ".js-follow", function(e){
    e.preventDefault();
    const act = $(this).attr('action');
    console.log(act)
    $.ajax({
        type: "POST",
        url: $(this).data('url'),
        data: {
            action:act,
            username:$(this).data('username'),
        },
        
        success: (data)=>{
            $('.js-follow-text').text(data.wording);
            // if( action == 'follow'){
            //     $(this).attr('data-action','unfollow');
            // }
            // else{
            //     $(this).attr('data-action','follow');              
            // }

            
        },
        error:(error)=>{
            console.warn(error.message)    
        }
    });
})



//caching cookies 
$.ajaxSetup({
    beforeSend: function beforeSend(xhr, settings) {
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');

                for (let i = 0; i < cookies.length; i += 1) {
                    const cookie = jQuery.trim(cookies[i]);

                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (`${name}=`)) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }

            return cookieValue;
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        }
    },
});

