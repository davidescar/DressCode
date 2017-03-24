#!/usr/bin/perl -w

require "../header.cgi";

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

#========= CREAZIONE VARIABILI DI SESSIONE ======
makeSession();

my $error = param("error");

print "Content-type: text/html\n\n";

#intestazione documento
my $keywords = "accesso,registrazione,autenticazione";
my $html_string = getHTMLHeader("Accesso",$keywords);

#========== CORPO LOGIN ==========	

$html_string .= "
<h2 class='ptitle'>Accedi</h2>
<form id='log_form' action='function/checkLogin.cgi' method='post'>
	<fieldset>
	
		<legend>Login</legend>
		<label for='email'>Email</label>
		<input type='text' id='email' name='email' class='pinput' / ".tabIndex().">
		<p class='msgerror' id='messageEmail'>".
		(("$error" eq "1") ? "Campo email vuoto" : "").
		(("$error" eq "2") ? "Utente non trovato, email non registrata" : "")."
		</p>
		
		<label for='password'>Password</label>
		<input type='password' id='password' name='password' class='ppass' / ".tabIndex().">
		<p class='msgerror' id='messagePassword'>".
		(("$error" eq "3") ? "Password errata! Riprovare." : "")."
		</p>
		
		<input type='submit' class='psubmit' value='Conferma' / ".tabIndex().">
		<p class='success_link'>Sei un nuovo utente?&nbsp;<a href='registration.cgi' ".tabIndex().">Registrati</a>!</p>
	</fieldset>
</form>";

#footer e chiusura documento
$html_string .= "<script type='text/javascript' src='/$public_path/js/checks.js'></script>";
$html_string .= "<script type='text/javascript' src='/$public_path/js/checkFormLogin.js'></script>";
$html_string .= getFooter();

#stampa del documento
printPrettyHTML($html_string);
