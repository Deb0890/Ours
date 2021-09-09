const profileButton = document.getElementById("user-profile");
const dropdownMenu = document.getElementById("dropdown-menu");

const handleDropdownMenu = (e) => {
    if (dropdownMenu.style.height == '0px' || !dropdownMenu.style.height) {
        dropdownMenu.style.height = '100px'
    } else {
        dropdownMenu.style.height = '0'
    }
}

profileButton.addEventListener('click', handleDropdownMenu)