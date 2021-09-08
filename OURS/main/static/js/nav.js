const profileButton = document.getElementById("user-profile");
const dropdownMenu = document.getElementById("dropdown-menu");

const handleDropdownMenu = (e) => {
    if (dropdownMenu.style.display != 'none') {
        dropdownMenu.style.display = 'none'
    } else {
        dropdownMenu.style.display = 'block'
    }
}

profileButton.addEventListener('click', handleDropdownMenu)