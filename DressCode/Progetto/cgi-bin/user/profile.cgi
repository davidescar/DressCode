#!/usr/bin/perl -w

require "../header.cgi";

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

#======= COSTRUZIONE PARSER ============
makeUserParser("../../data/utenti.xml");

#========= CREAZIONE VARIABILI DI SESSIONE ======
makeSession();

my $form = param('form');

print "Content-type: text/html\n\n";

my %titolo = (
	"profile" => "Gestione Identità",
	"password" => "Modifica Password",
	"address" => "Gestione Indirizzo",
	"credit" => "Gestione Carta",
	"" => "Profilo"
);

my $page_title = $titolo{$form};

#intestazione documento
my $keywords = "gestione,profilo,modifica,identità,carta,credito,indirizzo,ordini";
my $html_string = getHTMLHeader($page_title,$keywords);

#cerco dati utente
my $query="//utente[email='$email']";
my $user=$docUser->findnodes($query)->get_node(1);
my $nome=$user->findnodes('nome/text()');
my $cognome=$user->findnodes('cognome/text()');
my $indirizzo=$user->findnodes('indirizzo/text()');
my $citta=$user->findnodes('citta/text()');
my $CAP=$user->findnodes('CAP/text()');
my $nazione=$user->findnodes('nazione/text()');
my $carta=$user->findnodes('carta/text()');
my $circ=$user->findvalue('carta/attribute::circuito');

if("$circ" eq "null") { $circ="nessuno"; }

#===== CORPO GESTIONE PROFILO UTENTE ==========
if("$form" eq "") {
	
	$html_string .= (param('op')?"<p class='success_msg'>Operazione completata!</p>":"");
	$html_string .= (param('errore')?"<p id='opError'>Impossibile eseguire l'operazione: errore nei dati inseriti!</p>":"");
	
	$html_string .= "
	<h2 id='gest_p' class='ptitle'>Gestione Profilo ".("$admin" eq "admin" ? "Admin" : "Utente")."
		<span id='lower'>".(($nome && $cognome) ? "$nome $cognome" : "$email")."</span></h2>
		
	<ul id='profileList'>".
		(("$admin" eq "user") ? "<li><a href='ordini.cgi' ".tabIndex().">Storico Ordini</a></li>" : "")."
		<li><a href='profile.cgi?form=profile' ".tabIndex().">".($nome ? "Modifica" : "Aggiungi")." Identit&agrave;</a></li>
		<li><a href='profile.cgi?form=password' ".tabIndex().">Modifica Password</a></li>".
		(("$admin" eq "user") ? "<li><a href='profile.cgi?form=address' ".tabIndex().">".($indirizzo ? "Modifica" : "Aggiungi")." Indirizzo</a></li>" : "").
		(("$admin" eq "user") ? "<li><a href='profile.cgi?form=credit' ".tabIndex().">".($carta ? "Modifica" : "Aggiungi")." Carta</a></li>" : "")."
	</ul>";
	
}

#======= FORM INSERIMENTO NOME COGNOME =========
if("$form" eq "profile") {
	
	$html_string .= "
	<h2 class='ptitle'>Modifica Identità</h2>
	<form id='idForm' action='function/modProfile.cgi' method='post' class='profile_form'>			
		<fieldset>
			<ul>
				<li>
					<label for='nome'>Email</label>
					<input type='text' id='mail' name='mail' class='pinputlock' value='$email' readonly='readonly' />
				</li>
				<li>
					<label for='nome'>Nome</label>
					<input type='text' id='nome' name='nome' class='pinput' value='".($nome ? $nome : "")."' ".tabIndex()."/>
					<p id='messageNome' class='msgerror'></p>
				<li>
					<label for='cognome'>Cognome</label>
					<input type='text' id='cognome' name='cognome' class='pinput' value='".($cognome ? $cognome : "")."' ".tabIndex()."/>
					<p id='messageCognome' class='msgerror'></p>
				</li>
			</ul>
		</fieldset>
		<p><input name='padre' type='hidden' value='".past_link()."' /></p>
		<p><input class='psubmit' type='submit' value='Conferma' ".tabIndex()."/></p>
	</form>";
}
#======= FORM MODIFICA PASSWORD =========
if("$form" eq "password") {
	
	$html_string .= "
	<h2 class='ptitle'>Modifica Password</h2>
	<form id='passForm' action='function/modPassword.cgi' method='post' class='profile_form'>			
		<fieldset>
			<ul>
				<li>
					<label for='passwordA'>Password Attuale</label>
					<input type='password' id='passwordA' name='passwordA' class='ppass' ".tabIndex()."/>
					<p id='messagePasswordA' class='msgerror'></p>
				</li>
				<li>
					<label for='password'>Password</label>
					<input type='password' id='password' name='password' class='ppass' ".tabIndex()."/>
					<p id='messagePassword' class='msgerror'></p>
				</li>
				<li>
					<label for='passwordR'>Ripeti Password</label>
					<input type='password' id='passwordR' name='passwordR' class='ppass' ".tabIndex()."/>
					<p id='messagePasswordR' class='msgerror'></p>
				</li>
			</ul>
		</fieldset>
		<p><input class='psubmit' type='submit' value='Conferma' ".tabIndex()."/></p>
	</form>";
		
}

#======= FORM INSERIMENTO INDIRIZZO =========
if("$form" eq "address") {
	
	$html_string .= "
	<h2 class='ptitle'>Inserimento Indirizzo</h2>
	<form id='addressForm' action='function/modAddress.cgi' method='post' class='profile_form'>			
		<fieldset>
			<ul>
				<li>
					<label for='indirizzo'>Indirizzo</label>
					<input type='text' id='indirizzo' name='indirizzo' class='pinput' value='".($indirizzo?$indirizzo:"")."' ".tabIndex()."/>
					<p id='messageIndirizzo' class='msgerror'></p>
				</li>
				<li>
					<label for='citta'>Citt&agrave;</label>
					<input type='text' id='citta' name='citta' class='pinput' value='".($citta?$citta:"")."' ".tabIndex()."/>
					<p id='messageCitta' class='msgerror'></p>
				</li>
				<li>
					<label for='CAP'>CAP</label>
					<input type='text' id='CAP' name='CAP' class='pinput' size='5' maxlength='5' value='".($CAP?$CAP:"")."' ".tabIndex()."/>
					<p id='messageCAP' class='msgerror'></p>
				</li>
				<li>
					<label for='nazione'>Nazione</label>
					<input type='text' id='nazione' name='nazione' class='pinput' value='".($nazione?$nazione:"")."' ".tabIndex()."/>
					<p id='messageNazione' class='msgerror'></p>
				</li>
			</ul>
		</fieldset>
		<p><input name='padre' type='hidden' value='".past_link()."' /></p>
		<p><input class='psubmit' type='submit' value='Conferma' ".tabIndex()."/></p>
	</form>";
		
}
#======= FORM INSERIMENTO CARTA =========
if("$form" eq "credit") {
	
	$html_string .= "
	<h2 class='ptitle'>Inserimento Carta</h2>
	<form id='cardForm' action='function/modCredit.cgi' method='post' class='profile_form'>			
		<fieldset>
			<ul>
				<li>
					<label for='old_circ'>Circuito Carta Attuale</label>
					<input type='text' name='old_circ' id='old_circ' class='pinputlock' readonly='readonly' value='$circ' />
				</li>
				<li>
					<label for='circuit'>Seleziona Circuito Nuova Carta</label>
					<select class='pselect' id='circuit' name='circuit' ".tabIndex().">
						<option>American Express</option>
						<option>Master Card</option>
						<option>PayPal</option>
						<option>Visa</option>
						<option>PostePay</option>
					</select>
					<p id='messageCircuito' class='msgerror'></p>
				</li>
				<li>
					<label for='carta'>Numero Carta</label>
					<input type='text' id='carta' name='carta' class='pinput' value='".($carta ? $carta : "")."' size='16' maxlength='16' ".tabIndex()."/>
					<p id='messageCarta' class='msgerror'></p>
				</li>
			</ul>
		</fieldset>
		<p><input name='padre' type='hidden' value='".past_link()."' /></p>
		<p><input class='psubmit' type='submit' value='Conferma' ".tabIndex()."/></p>
	</form>";
	
}

#footer e chiusura documento
$html_string .= "<script type='text/javascript' src='/$public_path/js/checks.js'></script>";
$html_string .= "<script type='text/javascript' src='/$public_path/js/checkFormProfile.js'></script>";
$html_string .= getFooter();

#stampa del documento
printPrettyHTML($html_string);
