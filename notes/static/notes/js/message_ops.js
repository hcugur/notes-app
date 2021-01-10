function messageFinder() {
  let message = document.querySelectorAll("ul.messages");
  console.log('message is', message);
  if (message !== null) {
    console.log('found');
    setTimeout(function(){ 
      message.style.visibility = "hidden";
    }, 7000);
  }
  else {
    console.log('could not find');
    setInterval(messageFinder, 100);
  }
}

messageFinder();