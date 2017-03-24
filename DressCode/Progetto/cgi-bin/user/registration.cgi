#!/usr/bin/perl -w

require "../header.cgi";

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

#========= CREAZIONE VARIABILI DI SESSIONE ======
makeSession();

#controlla se è stato individuato un errore
my $errore = param('errore');

print "Content-type: text/html\n\n";

#intestazione documento
my $keywords = "accesso,registrazione,autenticazione";
my $html_string = getHTMLHeader("Registrazione",$keywords);
		
#========= CORPO REGISTRAZIONE ========
$html_string .= "<h2 class='ptitle'>Nuovo account</h2>";

if(param('ins')){
	$html_string .= "<p class='success_msg'>Registrazione effettuata con successo!</p>
	<p class='success_link'>Effettua il&nbsp;<a href='login.cgi'>login</a>.</p>";
}
else{

	$html_string .= "
	<form id='regForm' action='function/addUser.cgi' method='post'>		
		<fieldset>
			
			<label for='email'>Email</label>
			<input type='text' id='email' name='email' class='pinput' / ".tabIndex().">
			<p class='msgerror' id='messageEmail'>".
			(("$errore" eq "1") ? "Campo email vuoto!" : "").
			(("$errore" eq "3") ? "Errore nell'email digitata!" : "").
			(("$errore" eq "4") ? "Email gi&agrave; presente!" : "")."
			</p>
			
			<label for='password'>Password</label>
			<input type='password' id='password' name='password' class='ppass' / ".tabIndex().">
			<p class='msgerror' id='messagePassword'>".
			(("$errore" eq "2") ? "Campo password vuoto!" : "").
			(("$errore" eq "6") ? "La password deve contenere almeno 5 caratteri." : "")."
			</p>
			
			<label for='passwordR'>Ripeti Password</label>
			<input type='password' id='passwordR' name='passwordR' class='ppass' / ".tabIndex().">
			<p class='msgerror' id='messagePasswordR'>".
			(("$errore" eq "5") ? "Le due password non corrispondono." : "")."
			</p>
		
			<input id='confirm' class='psubmit' type='submit' value='Registrati'/ ".tabIndex().">
		</fieldset>
	</form>";	
		
}#else	

#footer e chiusura documento
$html_string .= "<script type='text/javascript' src='/$public_path/js/checks.js'></script>";
$html_string .= "<script type='text/javascript' src='/$public_path/js/checkFormReg.js'></script>";
$html_string .= getFooter();

#stampa del documento
printPrettyHTML($html_string);
