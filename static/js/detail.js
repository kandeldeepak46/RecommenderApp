
// send click flag on detail page load

  $(document).ready(function() {
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
    
    // setTimeout(fetch("detail_url", {
    //   method: "POST", 
    //   credentials: "same-origin",
    //   headers: {
    //       "X-CSRFToken": getCookie("csrftoken"),
    //       "Accept": "application/json",
    //       "Content-Type": "application/json",
    //       'X-Requested-With': 'XMLHttpRequest'
    //   },
    //   body: JSON.stringify({clicked: 'clicked'})
    // }).then(res => {
    //   console.log("Request complete! response:", res);
    // }), 10000);

    setTimeout(function(){ 
      console.log(detail_url)
      fetch("detail_url", {
        method: "POST", 
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept": "application/json",
            "Content-Type": "application/json",
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({clicked: 'clicked', ISBN: isbn})
      }).then(res => {
        console.log("Request complete! response:", res);
      })

     }, 8000);
    
});



// For converting number into rating

var djangoData = $('#my-data').data();

// Initial Ratings
const ratings = {
    rating: djangoData.name,
  }

  // Total Stars
  const starsTotal = 5;

  // Run getRatings when DOM loads
  // document.addEventListener('DOMContentLoaded', getRatings);

  // Get ratings
 
    for (let rating in ratings) {
      // Get percentage
      const starPercentage = (ratings[rating]/ starsTotal) * 100;

      // Round to nearest 10
      const starPercentageRounded = `${Math.round(starPercentage / 10) * 10}%`;

      // Set width of stars-inner to percentage
      document.querySelector(`.${rating} .stars-inner`).style.width = starPercentageRounded ;
  
      // Add number rating
      // document.querySelector(`.${rating} .number-rating`).innerHTML = ratings[rating];
    }


    function sendReadIt(){
      console.log(isbn);
      fetch("detail_url", {
        method: "POST", 
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept": "application/json",
            "Content-Type": "application/json",
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({readIt: 'read', clicked: 'clicked'})
      }).then(res => {
        console.log("Request complete! response:", res);
      })
    }

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