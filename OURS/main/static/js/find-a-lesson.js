console.log("hey");

let entries = document.querySelectorAll('.data');
entries = Array.from(entries);

const linkToAdvert = (e) => {
    const id = e.target.closest("tr").id;
    

}

entries.forEach(advert => {
    advert.addEventListener("click", linkToAdvert)
});

