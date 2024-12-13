
let currentPage = 1;
const perPage = 10;

async function getRestaurantById(restaurantId) {
    try {
        
        const response = await fetch(`http://127.0.0.1:80/restaurant/${restaurantId}`);
        const data = await response.json();
        
        displayRestaurantDetails(data);
    } catch (error) {
        console.error('Error fetching restaurant details:', error);
        alert('Error fetching restaurant details');
    }
}

async function getRestaurantByCountry(page = 1) {
    const Country = document.getElementById('restaurantCountryInput').value;
    const Rating = document.getElementById('restaurantRatingInput').value;

    if (!Country && !Rating) {
        getRestaurantList(currentPage);
        return;
    }

    try {
        
        const response = await fetch(`http://127.0.0.1:80/country?country=${Country}&page=${page}&rating=${Rating}`);
        const data = await response.json();
        
        displayRestaurantList(data.restaurants);
        updatePagination(data.page, data.total_pages);
    } catch (error) {
        console.error('Error fetching restaurant list by Country:', error);
        alert('Error fetching restaurant list by Country');
    }
}

async function displayRestaurantDetails(data) {
    const detailsDiv = document.getElementById('restaurantDetails');
    if (data.error) {
        detailsDiv.innerHTML = `<p>${data.error}</p>`;
    } else {
        detailsDiv.innerHTML = `
            <h3>${data["Restaurant Name"]}</h3>
            <p><strong>Restaurant ID:</strong> ${data["Restaurant ID"]}</p>
            <p><strong>Address:</strong> ${data.Address}</p>
            <p><strong>Country:</strong> ${data.Country}</p>
            <p><strong>Cuisines:</strong> ${data.Cuisines}</p>
            <p><strong>Average Cost for two:</strong> ${data["Average Cost for two"]}</p>
            <p><strong>Has Table booking:</strong> ${data["Has Table booking"]}</p>
            <p><strong>Has Online delivery:</strong> ${data["Has Online Delivery"]}</p>
            <p><strong>Aggregate rating:</strong> ${data["Aggregate rating"]}</p>
            <p><strong>Rating:</strong> ${data["Rating text"]}</p>
            <p><strong>Votes:</strong> ${data.Votes}</p>
            <div class="star-rating" id="starRating">
                ${[1, 2, 3, 4, 5].map(star => `
                    <input type="radio" id="star${star}" name="rating" value="${star}"/>
                    <label for="star${star}">&#9733;</label>
                `).join('')}
            </div>

        `;

        document.querySelectorAll('.star-rating input').forEach(input => {
            input.addEventListener('change', () => {
                selectedRating = document.querySelector('.star-rating input:checked').value;
                console.log(`Selected rating: ${selectedRating}`);
                
                try {
        
                    const response = fetch(`http://127.0.0.1:80/update_rating?selected_rating=${selectedRating}&restaurant_id=${data["Restaurant ID"]}`);
                    // alert('hmm');
                    
                } catch (error) {
                    console.error('Error fetching restaurant list by Country:', error);
                    alert('Error fetching restaurant list by Country');
                }


            });
        });

        

    }
}

async function getRestaurantList(page = 1) {
    try {
        const response = await fetch(`http://127.0.0.1:80/restaurants?page=${page}`);
        const data = await response.json();
        displayRestaurantList(data.restaurants);
        updatePagination(data.page, data.total_pages);
    } catch (error) {
        console.error('Error fetching restaurant list:', error);
        alert('Error fetching restaurant list');
    }
}

function displayRestaurantList(restaurants) {
    // console.log("displayRestaurantList");
    const listDiv = document.getElementById('restaurantList');
    listDiv.innerHTML = '';
    if (restaurants.length === 0) {
        listDiv.innerHTML = '<p>No restaurants found.</p>';
    } else {
        restaurants.forEach(restaurant => {
            // alert(restaurant["Restaurant ID"]);

            // <div class="restaurant-item" onclick="getRestaurantById(${restaurant["Restaurant ID"]})">
            // <a href="details.html?id=${restaurant["Restaurant ID"]}"
            listDiv.innerHTML += `
                <div class="restaurant-item">
                    <a href="details.html?id=${restaurant["Restaurant ID"]}">
                        <h3>${restaurant["Restaurant Name"]}</h3>
                        <p><strong>Address:</strong> ${restaurant.Address}</p>
                        <p><strong>Country:</strong> ${restaurant.Country}</p>
                        <p><strong>Cuisines:</strong> ${restaurant.Cuisines}</p>
                    </a>
                </div>
                <hr>
            `;
        });
    }
}

function updatePagination(page, totalPages) {
    const pageInfo = document.getElementById('pageInfo');
    pageInfo.innerText = `Page ${page} of ${totalPages}`;
    currentPage = page;
}

function nextPage() {
    getRestaurantList(currentPage + 1);
}

function previousPage() {
    if (currentPage > 1) {
        getRestaurantList(currentPage - 1);
    }
}


// Initialize with the first page of restaurants
// getRestaurantList(currentPage);