document.querySelector('button').addEventListener('click', toggle)

function toggle(event) {
  if (document.getElementById('spoiler').style.display == 'none') {
    event.target.innerText = 'Hide'
    document.getElementById('spoiler').style.display = ''
  } else {
    event.target.innerText = 'Show All'
    document.getElementById('spoiler').style.display = 'none'
  }
}