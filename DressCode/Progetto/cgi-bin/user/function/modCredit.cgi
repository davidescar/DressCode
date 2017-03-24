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
	return 0;	
}

#======== PRELIEVO VALORI FORM =========

#recupero input registrazione
my $circuit = param("circuit");
my $card = param('carta');

my $parent = param("padre");
$parent =~ s/\?.*//;

# Controlli campi
my $formErr = checkError($circuit,$card);

# ==== CONTROLLO CAP ======
if(!looks_like_number($card)
	|| length($card)<16){ $formErr += 2; }

print "Content-type: text/html\n\n";
if($formErr > 0){
	print "<meta http-equiv='refresh' content='0; url=../profile.cgi?errore=$formErr'/>";
}
else {
# =========== MODIFICA/AGGIUNTA NOME E COGNOME =========
	
	# recupero elemento radice
	my $rootUtenti=$docUser->getDocumentElement;
		
	#trovo il nodo nome
	my $userCard = $rootUtenti->findnodes("//utente[email='$email']/carta")->get_node(1);
	$userCard->removeChildNodes();
	$userCard->appendText($card);
	$userCard->setAttribute("circuito",$circuit); #inserisco circuito selezionato
	
	open(my $fo, '>', $fileUserXML) or die "Errore nell'apertura del file $fileUserXML ";
	print $fo $docUser->toString;
	close $fo;
	
	if("$parent" eq "carrello.cgi") {
		print "<meta http-equiv='refresh' content='0; url=../carrello.cgi' />";
	}else {
		print "<meta http-equiv='refresh' content='0; url=../profile.cgi?op=ok' />";
	}

}
