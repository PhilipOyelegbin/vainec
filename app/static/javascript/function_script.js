// Toggle between hiding and showing the menu content by clicking on the button
function menu(){
  document.getElementById("contents").classList.toggle("show");
}

// Automatic image slide show
var home = ["/static/images/Vote.png", "/static/images/Coat of Arm.png",
"/static/images/Independence.png"];
var hm_start = 0;
var hm_slider = document.getElementById("transition");
var hm_auto = setInterval(swipe, 3000);

function swipe() {
  hm_start++;
  if (hm_start >= home.length) {
    hm_start = 0;
  }
  hm_slider.src = home[hm_start];
}

// Toggle between hiding and showing the state list by clicking on the button
function governorship_vote_center(){
  document.getElementById("state").classList.toggle("view");
}
