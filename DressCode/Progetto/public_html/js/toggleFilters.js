
document.body.onload = function (){
	
	var toggles = ["togglemat","toggletip","togglecol","toggleprice"];
	for (i=0; i < toggles.length; i++) 
		document.getElementById(toggles[i]).className = "cloackLists";
		
	toggles = document.getElementsByClassName("cloackLists");
	for (i=0; i < toggles.length; i++)
		toggles[i].style.display = "none";

}

document.getElementById("displaymat").onclick = function() {
	
	var ele = document.getElementById("togglemat");
	var filter = document.getElementById("displaymat");
	if(ele.style.display == "block") {
    	ele.style.display = "none";
    	filter.className = "filterClosed";
  	}
	else {
		ele.style.display = "block";
		filter.className = "filterOpened";
	}
	
} 

document.getElementById("displaytip").onclick = function() {
	
	var ele = document.getElementById("toggletip");
	var filter = document.getElementById("displaytip");
	if(ele.style.display == "block") {
    	ele.style.display = "none";
    	filter.className = "filterClosed";
  	}
	else {
		ele.style.display = "block";
		filter.className = "filterOpened";
	}
	
} 

document.getElementById("displaycol").onclick = function() {
	
	var ele = document.getElementById("togglecol");
	var filter = document.getElementById("displaycol");
	if(ele.style.display == "block") {
    	ele.style.display = "none";
    	filter.className = "filterClosed";
  	}
	else {
		ele.style.display = "block";
		filter.className = "filterOpened";
	}
	
} 

document.getElementById("displayprice").onclick = function() {
	
	var ele = document.getElementById("toggleprice");
	var filter = document.getElementById("displayprice");
	if(ele.style.display == "block") {
    	ele.style.display = "none";
    	filter.className = "filterClosed";
  	}
	else {
		ele.style.display = "block";
		filter.className = "filterOpened";
	}
	
} 

document.getElementById("activate_fil").onclick = function(){
	var ele = document.getElementById("filtersList");
	if (ele.style.display == "block"){
		ele.style.display = "none";
	}
	else{
		ele.style.display = "block";
	}
}
