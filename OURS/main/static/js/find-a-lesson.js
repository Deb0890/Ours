console.log("hey");

let entries = document.querySelectorAll('.data');
entries = Array.from(entries);

const linkToAdvert = (e) => {
    const id = e.target.closest("tr").id;
    

}

entries.forEach(advert => {
    advert.addEventListener("click", linkToAdvert)
});

const filterBtn = document.getElementById("filter-btn")
const resetBtn = document.getElementById("reset-filter-btn")
const filter = document.getElementById("filter")

const filterText = document.getElementById("filter-text")
const queryString = window.location.search;
let newQueryString = '';

filter.addEventListener("change", function() {
    filterText.placeholder = `Enter ${filter.value} to filter on...`
})

filterBtn.addEventListener("click", function() {
    if(filter.value !== ''  && filterText.value !== ''){
        updateUrl(filter.value,filterText.value,queryString)
    }
})

window.addEventListener("keydown", function(e) {
    if(e.code === 'Enter'){
        if(filter.value !== ''  && filterText.value !== ''){
            updateUrl(filter.value,filterText.value,queryString)
        }
    }
})

resetBtn.addEventListener("click", function() {
    window.location = window.location.pathname
})

function updateUrl(filter,value,url) {
    newQueryString += '?filter=' + filter + '&value=' + value
    window.location = newQueryString
}


