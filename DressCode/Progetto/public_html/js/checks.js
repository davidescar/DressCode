
function isNotEmpty(name,field) {
	
	if(field.length < 1) {	
		var name_string = name;
		if(name == "Descr") name_string = "Descrizione"; 
		if(name == "Immagine0" || name == "Immagine1" || name == "Immagine2") name_string = "Immagine";
		document.getElementById("message"+name).innerHTML = "Il campo " + name_string + " non pu&ograve; essere vuoto.";
		return false;
	}
	
	document.getElementById("message"+name).innerHTML = "";
	return true;
	
}

function isAnEmail(field) {
	
	var patternEmail=/[a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}/;
	
	if(field.search(patternEmail) == -1) {
		document.getElementById("messageEmail").innerHTML = "Il campo email non è corretto.";
		return false;
	}
	
	document.getElementById("messageEmail").innerHTML = "";
	return true;
	
}

function isCorrectPsw(pass) {	
	if(pass.length < 5) {
		document.getElementById("messagePassword").innerHTML = "La password deve contenere almeno 5 caratteri.";
		return false;
	}
	
	document.getElementById("messagePassword").innerHTML = "";
	return true;
}

function passwordCompare(pass1,pass2) {
	
	if(pass1.localeCompare(pass2)){
		document.getElementById("messagePasswordR").innerHTML = "Le due password non corrispondono.";
		return false;
	}
	
	document.getElementById("messagePasswordR").innerHTML = "";
	return true;
	
}

function isAPrice(field) {
	
	var patternPrezzo=/^([1-9][0-9]*|0)((,|.)[0-9]{2})?$/;
	
	if(field.search(patternPrezzo) == -1){
		document.getElementById("messagePrezzo").innerHTML = "Il campo prezzo non è valido.";
		return false;
	}
	
	document.getElementById("messagePrezzo").innerHTML = "";
	return true;
	
}

function isAPicture(index,field) {
		
	var patternImmagini=/^.+\.(jpeg|jpg|png|gif|bmp)$/;

	if(field.search(patternImmagini) == -1){
		document.getElementById("messageImmagine"+index).innerHTML = "Formato campo immagine non valido (formati accettati: JPG, PNG, GIF e BMP).";
		return false;
	} 
	
	document.getElementById("messageImmagine"+index).innerHTML = "";
	return true;
		
}

function isCheckboxSelect(name,check) {
	
	var selected = false;
	
	for (i = 0; i < check.length && !selected ; i++) {
		if (check[i].checked)
			selected = true;
	}
	
	var msg;
	if(name == "Taglie") msg = "Nessuna taglia selezionata";
	else msg = "Nessun colore selezionato";
	
	if(!selected){
		document.getElementById("message"+name).innerHTML = msg;
		return false;
	}
	
	document.getElementById("message"+name).innerHTML = "";
	return true;
		
}

function isAValidCAP(value) {
	
	if(isNaN(value)){
		document.getElementById("messageCAP").innerHTML="Il campo CAP deve essere di sole cifre.";
		return false;
	}
	
	if(value.length<5){
		document.getElementById("messageCAP").innerHTML="Il campo CAP deve essere di 5 cifre.";
		return false;
	}
	
	document.getElementById("messageCAP").innerHTML = ""; 
	return true;
	
}

function isAValidCreditCard(value) {
	
	if(isNaN(value)){
		document.getElementById("messageCarta").innerHTML="Il campo carta deve essere di sole cifre.";
		return false;
	}
	
	if(value.length < 16){
		document.getElementById("messageCarta").innerHTML="Il campo carta deve essere di 16 cifre.";
		return false;
	}
	
	document.getElementById("messageCarta").innerHTML = ""; 
	return true;
	
}
