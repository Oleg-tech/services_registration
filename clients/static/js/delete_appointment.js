$(document).ready(function(){
    $(".like-form").submit(function(e){
        e.preventDefault()
        const post_id = $(this).attr('id')
        console.log($('input[name=csrfmiddlewaretoken]').val())
        console.log(post_id)

        $.ajax({
            type:'POST',
            url: '/panel/delete_appointment/',
            dataType: 'json',
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'post_id': post_id,
            },
            success: function(){
                $("#appointment_"+post_id).remove();
            },
            error: function(response){
                console.log('error');
            }
        });
    });
});