
$(document).ready(function() {

    $.ajaxSetup({ 
        beforeSend: function(xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        } 
   });

   $('#getForm').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    getData();
    });



    function getData() {
        console.log("create post is working!: sanity check here") // sanity check

        $.ajax({
            url : '/example/', // the endpoint
            type : "POST", // http method
            // handle a successful response
            success: function(response) { // on success..
                console.log("after pressing the button");
                console.log(response.bookTitle);
                
                $("#bookTitle").val(response.bookTitle);
                $("#bookAuthor").val(response.bookAuthor);
                $("#ISBN").val(response.ISBN);
                $("#description").val(response.description);
                $('#genre').val(response.genre)
                // $('#sth').html(response); // update the DIV 
            },
            // success : function(json) {
            //     console.log("success: another sanity check"); // 
            //     $('#sth').replaceWith(function(){
            //         return '<h1>' + title + '</h1>'
            //     });
            //     $('#getDataResponse').replaceWith(function() {
            //         return '<h4>' + 'Here' + '</h4>';
            //     });
            // },
    
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                // $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                //     " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };

 });
