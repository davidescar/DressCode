
var form = document.getElementById("idForm");
if(form) form.onsubmit = function() {
	
	var nome=document.getElementById("nome").value;
	var cognome=document.getElementById("cognome").value;
	
	var valido=true;
	
	var fields = ["Nome","Cognome"];
	
	// controllo validità valori form
	
	valido = isNotEmpty(fields[0],nome) && valido;
	valido = isNotEmpty(fields[1],cognome) && valido;
	
	return valido;
		
}

form = document.getElementById("passForm");
if(form) form.onsubmit = function() {
	
	var passA=document.getElementById("passwordA").value;
	var pass=document.getElementById("password").value;
	var passR=document.getElementById("passwordR").value;
	
	var valido=true;
	
	var fields = ["PasswordA","Password","PasswordR"];
	
	// controllo validità valori form
	
	valido = isNotEmpty(fields[0],passA) && valido;
	valido = isNotEmpty(fields[1],pass) && valido;
	valido = isNotEmpty(fields[2],passR) && valido;
	
	return valido;
		
}

form = document.getElementById("addressForm");
if(form) form.onsubmit = function() {
	
	var indirizzo=document.getElementById("indirizzo").value;
	var citta=document.getElementById("citta").value;
	var CAP=document.getElementById("CAP").value;
	var nazione=document.getElementById("nazione").value;
	
	var valido=true;
	
	var fields = ["Indirizzo","Citta","CAP","Nazione"];
	
	// controllo validità valori form
	
	valido = isNotEmpty(fields[0],indirizzo) && valido;
	valido = isNotEmpty(fields[1],citta) && valido;
	valido = isNotEmpty(fields[2],CAP) && valido;
	if(valido) valido = isAValidCAP(CAP) && valido;
	valido = isNotEmpty(fields[3],nazione) && valido;
		
	return valido;
		
}

form = document.getElementById("cardForm");
if(form) form.onsubmit = function() {
	
	var circuit=document.getElementById("circuit").value;
	var card=document.getElementById("carta").value;
	
	var valido=true;
	
	var fields = ["Circuito","Carta"];
	
	// controllo validità valori form
	
	valido = isNotEmpty(fields[0],circuit) && valido;
	valido = isNotEmpty(fields[1],card) && valido;
	if(valido) valido = isAValidCreditCard(card) && valido;
		
	return valido;
		
}


