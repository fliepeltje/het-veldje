document.querySelectorAll(".dog-item").forEach(item => {
    item.addEventListener("click", event => {
        const modal_target = `dog-modal-${item.dataset.target}`
        document.getElementById(modal_target).style.display = "block"
    })
})

document.querySelectorAll(".close-modal").forEach(item => {
    item.addEventListener("click", event => {
        const modal_target = `dog-modal-${item.dataset.target}`
        document.getElementById(modal_target).style.display = "none"
    })
})
window.addEventListener("click", event => {
    document.querySelectorAll(".dog-modal").forEach(item => {
        if (event.target == item) {
            item.style.display = "none"
        }
    })
})