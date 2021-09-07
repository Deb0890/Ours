const labels = document.querySelectorAll('label')

for (let i = 0; i < labels.length; i++) {
    if (labels[i].textContent == "Clear") {
        labels[i].style.display = 'none'
    }
}

const form = document.querySelector('form')
const links = form.querySelector('a')
const imageLink = document.getElementById("profileImage").src

links.innerHTML = `<img class="profile" src="${imageLink}">`

const imageUploader = document.getElementById("id_profile_img")
