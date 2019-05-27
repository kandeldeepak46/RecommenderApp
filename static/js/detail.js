
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
