#!/usr/bin/perl -w

require "../../header.cgi";

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use Scalar::Util qw(looks_like_number);

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
	if("$_[3]" eq ""){ return 1; }
	return 0;	
}

#======== PRELIEVO VALORI FORM =========

#recupero input registrazione
my $indirizzo=param('indirizzo');
my $citta=param('citta');
my $CAP=param('CAP');
my $nazione=param('nazione');

my $parent = param("padre");
$parent =~ s/\?.*//;

# Controlli campi
my $formErr = checkError($indirizzo,$citta,$CAP,$nazione);

# ==== CONTROLLO CAP ======
if(!looks_like_number($CAP)
	|| length($CAP)<5){ $formErr += 2; }

print "Content-type: text/html\n\n";
if($formErr > 0){
	print "<meta http-equiv='refresh' content='0; url=../profile.cgi?errore=$formErr'/>";
}
else {
# =========== MODIFICA/AGGIUNTA NOME E COGNOME =========
	
	# recupero elemento radice
	my $rootUtenti=$docUser->getDocumentElement;
	
	#trovo il nodo nome
	my $userAdd = $rootUtenti->findnodes("//utente[email='$email']/indirizzo")->get_node(1);
	$userAdd->removeChildNodes();
	$userAdd->appendText($indirizzo);
	#trovo il nodo nome
	my $userTown = $rootUtenti->findnodes("//utente[email='$email']/citta")->get_node(1);
	$userTown->removeChildNodes();
	$userTown->appendText($citta);
	#trovo il nodo nome
	my $userCAP = $rootUtenti->findnodes("//utente[email='$email']/CAP")->get_node(1);
	$userCAP->removeChildNodes();
	$userCAP->appendText($CAP);
	#trovo il nodo nome
	my $userNat = $rootUtenti->findnodes("//utente[email='$email']/nazione")->get_node(1);
	$userNat->removeChildNodes();
	$userNat->appendText($nazione);
	
	open(my $fo, '>', $fileUserXML) or die "Errore nell'apertura del file $fileUserXML ";
	print $fo $docUser->toString;
	close $fo;
	
	if("$parent" eq "carrello.cgi") {
		print "<meta http-equiv='refresh' content='0; url=../carrello.cgi' />";
	}else {
		print "<meta http-equiv='refresh' content='0; url=../profile.cgi?op=ok' />";
	}

}
