


const dayLabels = document.querySelectorAll('li label')
const dayLabelsArr = Array.from(dayLabels)


const handleDayClick = (e) => {
    e.target.style.background = (e.target.style.background === 'rgb(221, 118, 118)') ? 'unset' : 'rgb(221, 118, 118)'
}

dayLabelsArr.forEach(label => {
    label.addEventListener('click', handleDayClick)
});