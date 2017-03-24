
document.getElementById("log_form").onsubmit = function() {
	
	var email = document.getElementById("email").value;
	var password = document.getElementById("password").value;
		
	var valido = true;
	
	var fields = ["Email","Password"];
	
	// controllo validità valori form
	
	valido = isNotEmpty(fields[0],email) && valido;
	if(valido) valido = isAnEmail(email) && valido;
	
	valido = isNotEmpty(fields[1],password) && valido;
		
	return valido;
	
}


