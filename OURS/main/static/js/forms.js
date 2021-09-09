
console.log('hey');

const dayLabels = document.querySelectorAll('li label')
const dayLabelsArr = Array.from(dayLabels)


const handleDayClick = (e) => {
    e.target.style.background = (e.target.style.background === 'rgb(221, 118, 118)') ? 'unset' : 'rgb(221, 118, 118)'
}

dayLabelsArr.forEach(label => {
    input = label.querySelector('input')
    if (input.checked) {
        label.style.background = 'rgb(221, 118, 118)'
    }
    if (!input.disabled) {
        label.addEventListener('click', handleDayClick)
    }
});