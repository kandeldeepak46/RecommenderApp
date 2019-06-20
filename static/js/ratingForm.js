

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


    $("input[name='stars']").change(function(event){
        // Do something interesting here
        event.preventDefault();
        console.log("hey");
        post_rating();
    });

      function post_rating() {
        console.log("create post is working!") // sanity check
        
        //console.log($("input[name='stars']:checked").val());

        $.ajax({
            url : `/example/detail/${isbn}`, // the endpoint
            type : "POST", // http method
            data : { rating : 5 }, // data sent with the post request
    
            // handle a successful response
            success : function(json) {
                // console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check
                $('#changeOnRating').replaceWith(function() {
                    return '<h4>' + 'Thankyou for rating.' + '</h4>';
                });
            },
    
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                // $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                //     " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };

 });

 