
document.getElementById("regForm").onsubmit = function() {
	
	var email = document.getElementById("email").value;
	var password = document.getElementById("password").value;
	var passwordR = document.getElementById("passwordR").value;
		
	var valido = true;
	
	var fields = ["Email","Password","PasswordR"];
	
	// controllo validità valori form
	
	valido = isNotEmpty(fields[0],email) && valido;
	if(valido) valido = isAnEmail(email) && valido;
	
	valido = isCorrectPsw(password) && valido;
	if(valido) valido = passwordCompare(password,passwordR) && valido;
		
	return valido;
	
}









