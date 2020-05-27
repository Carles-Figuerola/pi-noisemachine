var xhttp = new XMLHttpRequest();

function setValue() {
  rangeV.innerHTML = `<span>${range.value}</span>`;
  if (range.value != window.originalValue) {
    rangeV.style.backgroundColor = "red";
  }
  else {
    rangeV.style.backgroundColor = "green";
  }
}

document.addEventListener("DOMContentLoaded", setValue);

function show_mute() {
  document.getElementById("unmute").classList.add('hidden')
  document.getElementById("mute").classList.remove('hidden')
}

function show_unmute() {
  document.getElementById("mute").classList.add('hidden')
  document.getElementById("unmute").classList.remove('hidden')
}

document.addEventListener("DOMContentLoaded", function(event) { 
  range = document.getElementById('range'),
  rangeV = document.getElementById('rangeV'),
  range = document.getElementById('range');
  window.originalValue = range.value;
  range.addEventListener('input', setValue);
  setValue();

  document.getElementById("rangeV").addEventListener("click", function () {
    xhttp.open("GET", "/setvolume?volume=" + range.value, true);
    xhttp.send()
    show_mute()
    rangeV.style.backgroundColor = "green";
    window.originalValue = range.value;
  });
  document.getElementById("mute").addEventListener("click", function () {
    show_unmute()
    xhttp.open("GET", "/mute");
    xhttp.send()
  });
  document.getElementById("unmute").addEventListener("click", function () {
    show_mute()
    xhttp.open("GET", "/unmute");
    xhttp.send()
  });

});
