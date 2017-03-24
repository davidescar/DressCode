#!/usr/bin/perl -w

require "../../header.cgi";

use Digest::SHA1 qw(sha1_hex);
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

#==== FUNZIONE CONTROLLO VALORI INSERITI ======
sub checkError {	
	if("$_[1]" eq ""){ return 1; }
	if("$_[2]" eq ""){ return 2; }
	if(!("$_[0]" =~ "[a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}")){ return 3; }
	return 0;	
}

#======== PRELIEVO VALORI FORM =========

#recupero input registrazione
my $email=param('email');
my $password=param('password');
my $passwordR=param('passwordR');

# Controlli campi
my $formErr = checkError($email,$password,$passwordR);

#creazione parser utenti
my $fileUtentiXML = "../../../data/utenti.xml";
makeUserParser($fileUtentiXML);

# ==== RICERCA SE EMAIL GIà PRESENTE ======
my $utente = $docUser->findnodes("//utente[email='$email']")->get_node(1);
if($utente){ $formErr = 4; }

# ===== CONTROLLO PASSWORD INSERITA =====
if("$password" ne "$passwordR"){ $formErr = 5; }
if( length($password) < 5 ){ $formErr = 6; }

print "Content-type: text/html\n\n";
if($formErr > 0){
	 print "<meta http-equiv='refresh' content='0; url=../registration.cgi?errore=$formErr' />";
}
else{
	
	#cerco il nodo a cui inserire un figlio
	my $padre = $docUser->findnodes("//so:utentiRegistrati")->get_node(1);
		
	# hash della password
	my $hashPassword = sha1_hex($password);
	
	#costruisco il frammento per il nodo utente
	my $utente = $docUser->createElement("utente");
	$utente->setAttribute("admin","0");
	
	my @info = ("email","password","nome","cognome","indirizzo","citta","CAP","nazione","carta");
	foreach my $i(@info) { $utente->appendChild($docUser->createElement($i)); }
	$utente->findnodes("carta")->get_node(1)->setAttribute("circuito","null"); 
	
	#inserisco i nuovi valori
	$utente->findnodes("email")->get_node(1)->appendText($email);
	$utente->findnodes("password")->get_node(1)->appendText($hashPassword);
	
	#aggiungo il nodo
	my $nodo = $parserUser->parse_balanced_chunk($utente)
			|| die('frammento non ben formato');
	$padre->appendChild($utente);
	
	open(my $fo, '>', $fileUtentiXML) or die "Errore nell'apertura del file ".$fileUtentiXML.".";
	print $fo $docUser->toString;
	close $fo;
	
	printPrettyXML($fileUtentiXML);
	
	print "<meta http-equiv='refresh' content='0; url=../registration.cgi?ins=ok' />";
	
}
