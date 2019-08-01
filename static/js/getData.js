
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
    // console.log("undercover agent");
    // str=$("#id_book_cover").val;
    var str="http";
    if(str.match(/http/gi).length>0)
    {
        $("#id_book_cover").prop('required',false);
    }
    else
    {
        $("#id_book_cover").prop('required',true);
    }
    getData();
    });

  
    $('#id_book_cover').change(function(){
        // $('#book_image_src').attr("src",this.files[0].mozFullPath);  
        // alert($(this).val());
        var reader = new FileReader();

            reader.onload = function (e) {
                $('#book_image_src')
                    .attr('src', e.target.result)                    
            };
            reader.readAsDataURL(this.files[0]);
        alert(this.files[0].size);
    });

    function getData() {
        // console.log("create post is working!: sanity check here hello guyz") // sanity check
        console.log('we are here')
        $.ajax({
            url : '/example/getData', // the endpoint
            type : "POST", // http method
            // handle a successful response
            success: function(response) { // on success..
                console.log("after pressing the button");
                console.log(response.bookTitle);
                $("#bookTitle").val(response.bookTitle);
                $("#bookAuthor").val(response.bookAuthor);
                $("#ISBN").val(response.ISBN);
                $("#description").val(response.description);
                $('#genre').val(response.genre);
                $('#imageURL').val(response.imageURL);
                $('#book_image_src').attr("src",response.imageURL);                     
                // $('#book_image_src').attr("src","https://upload.wikimedia.org/wikipedia/en/d/dc/A_Song_of_Ice_and_Fire_book_collection_box_set_cover.jpg");
                $('#request_message').text(response.request_message);
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