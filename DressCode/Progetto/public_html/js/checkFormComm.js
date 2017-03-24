document.getElementById('form_rec').onsubmit = function(){
	
	var textComment=document.getElementById("textcomment").value;
	var stars=document.getElementsByName("rating-input-1");
	
	var textMsg=document.getElementById("messageTextComm");
	var starMsg=document.getElementById("messageStarComm");
	
	var starCheck=false;
	
	for (var i = 0; i < stars.length; i++) {
        if (stars[i].checked) starCheck=true;
    }	
		
	var valido=true;
	
	// controllo validità valori form
	
	if(textComment.length<10){
		valido=false;
		textMsg.innerHTML="<p class='msgerror'>Il testo della recensione non pu&ograve; "
				+"essere vuoto e deve contenere almeno 10 caratteri!</p>";
	}
	else textMsg.innerHTML="";
	
	if(starCheck!=true){
		valido=false;
		starMsg.innerHTML="<p class='msgerror'>Valutazione prodotto non selezionata!</p>";
	}
	else starMsg.innerHTML="";
		
	return valido;
	
}