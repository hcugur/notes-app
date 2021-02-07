// Use local storage to store clicked note's scrollTop value and in each click on
// note scroll the note container to that exact position

document.addEventListener("DOMContentLoaded", function(event) { 
  document.getElementById("note-list").addEventListener("click", function(e) {
    if (e.target && e.target.matches("li .card .card-body a.note-link")) {
      //console.log('Success')
      targetElem = document.querySelector('.note-sidebar');
      localStorage.setItem('scrollT', targetElem.scrollTop);
    }
  });  
});


document.addEventListener("DOMContentLoaded", function(event) {
  if (localStorage.getItem("scrollT") !== null) {
    let targetElem = document.querySelector('.note-sidebar');
    targetElem.scrollTop = localStorage.getItem("scrollT");
  }
});