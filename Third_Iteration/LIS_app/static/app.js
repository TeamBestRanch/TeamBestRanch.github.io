// Landing Page Background Images
var backgrounds = new Array(
  "url('../static/img/pexels-engin-akyurt-1435901.jpg')",
  "url('../static/img/pexels-lukas-1352269.jpg')",
  "url('../static/img/pexels-marianna-ole-764925.jpg')",
  "url('../static/img/pexels-valeria-boltneva-1123250.jpg')"
);

var imageUrl = "url('../static/img/pexels-engin-akyurt-1435901.jpg')";
document.getElementById("home").style.backgroundImage = imageUrl;

idx = 0;

setInterval(function () {
  if (idx < backgrounds.length) {
    document.getElementById("home").style.backgroundImage = backgrounds[idx];
    idx += 1;
  } else {
    idx = 0;
  }
}, 5000);


