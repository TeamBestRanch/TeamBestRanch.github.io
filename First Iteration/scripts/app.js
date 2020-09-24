// Landing Page Background Images
var backgrounds = new Array(
            "url('First Iteration/img/pexels-engin-akyurt-1435901.jpg')"
          , "url('First Iteration/img/pexels-lukas-1352269.jpg')"
          , "url('First Iteration/img/pexels-marianna-ole-764925.jpg')"
          , "url('First Iteration/img/pexels-valeria-boltneva-1123250.jpg')"
        );


var imageUrl= "url('First Iteration/img/pexels-engin-akyurt-1435901.jpg')";
document.getElementById("home").style.backgroundImage = imageUrl;

cycle = 0;

setInterval(function() { 
	if (cycle < backgrounds.length) { 
		document.getElementById("home").style.backgroundImage = backgrounds[cycle]; 
		cycle += 1; 
	} else {  
		cycle = 0; 
	} 
}, 10000); 