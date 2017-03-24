#!/usr/bin/perl -w

require "../../header.cgi";

use Digest::SHA1 qw(sha1_hex);
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

#======= COSTRUZIONE PARSER ============
my $fileUserXML = "../../../data/utenti.xml";
makeUserParser($fileUserXML);

#========= CREAZIONE VARIABILI DI SESSIONE ======
makeSession();

#==== FUNZIONE CONTROLLO VALORI INSERITI ======
sub checkError {	
	if("$_[0]" eq ""){ return 1; }
	if("$_[1]" eq ""){ return 1; }
	if("$_[2]" eq ""){ return 1; }
	return 0;	
}

#======== PRELIEVO VALORI FORM =========

#recupero input registrazione
my $passA=param('passwordA');
my $pass=param('password');
my $passR=param('passwordR');

# Controlli campi
my $formErr = checkError($passA,$pass,$passR);

# ==== RICERCA SE PASSWORD ATTUALE CORRETTA ======
my $password = $docUser->findvalue("//utente[email='$email']/password");
my $criptPass = sha1_hex($passA);
if("$password" ne "$criptPass"){ $formErr += 2; }

# ===== CONTROLLO PASSWORD INSERITA =====
if("$pass" ne "$passR"){ $formErr += 2; }

print "Content-type: text/html\n\n";
if($formErr > 0){
	print "<meta http-equiv='refresh' content='0; url=../profile.cgi?errore=$formErr'/>";
}
else {
# =========== MODIFICA/AGGIUNTA NOME E COGNOME =========

	# hash della password
	my $hashPassword = sha1_hex($pass);
	
	# recupero elemento radice
	my $rootUtenti=$docUser->getDocumentElement;
	
	#trovo il nodo nome
	my $userPass = $rootUtenti->findnodes("//utente[email='$email']/password")->get_node(1);
	$userPass->removeChildNodes();
	$userPass->appendText($hashPassword);
	
	open(my $fo, '>', $fileUserXML) or die "Errore nell'apertura del file $fileUserXML ";
	print $fo $docUser->toString;
	close $fo;
	
	print "<meta http-equiv='refresh' content='0; url=../profile.cgi?op=ok' />";

}
