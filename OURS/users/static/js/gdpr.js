console.log('hey');

const confirmButton = document.getElementById('confirm');
const submitButton = document.getElementById('submitButton');
const gdprCheckbox = document.getElementById('gdprConfirm');
const closeModalButton = document.getElementById('closeModal');
const modal = document.querySelector('.modal');

console.log(modal);


const togelModal = () => {
    if (modal.style.display == "none" || !modal.style.display) {
        modal.style.display = "flex"
    } else {
        modal.style.display = "none"
    }
}

const handleCheckbox = (e) => {
    if (e.target.checked) {
        submitButton.disabled = false
        submitButton.classList.toggle('disabled')
    } else {
        submitButton.disabled = true
        submitButton.classList.toggle('disabled')
    }
}


confirmButton.addEventListener('click', togelModal)
closeModalButton.addEventListener('click', togelModal)
gdprCheckbox.addEventListener('change', handleCheckbox)