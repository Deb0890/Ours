console.log('hey');

const confirmButton = document.getElementById('confirm');
const submitButton = document.getElementById('submitButton');
const gdprCheckbox = document.getElementById('gdprConfirm');
const closeModalButton = document.getElementById('closeModal');
const modal = document.querySelector('.modal');

const form = document.querySelector("form")
let inputs = form.querySelectorAll('input')
inputs = Array.from(inputs)
console.log(inputs);

console.log(modal);


const togelModal = () => {
    if (modal.style.display == "none" || !modal.style.display) {

        for (let i = 0; i < inputs.length; i++) {
            if (!inputs[i].value) {
                return
            }
            
        }

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