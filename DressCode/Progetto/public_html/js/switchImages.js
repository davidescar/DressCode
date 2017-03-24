
document.getElementById("smallImg1").onclick = function() {
	var widthMin=480;
	
	var s_src = document.getElementById("smallImg1").src;
	
	if(window.innerWidth>widthMin){
		document.getElementById("smallImg1").src = document.getElementById("bigImg").src;
		document.getElementById("bigImg").src = s_src;
	}//if
	
}

document.getElementById("smallImg2").onclick = function() {
	var widthMin=480;
	
	var s_src = document.getElementById("smallImg2").src;
	
	if(window.innerWidth>widthMin){
		document.getElementById("smallImg2").src = document.getElementById("bigImg").src;
		document.getElementById("bigImg").src = s_src;
	}//if
}
