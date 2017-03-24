#!/usr/bin/perl -w

require "../../header.cgi";

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
	return 0;	
}

#======== PRELIEVO VALORI FORM =========

#recupero input registrazione
my $nome=param('nome');
my $cognome=param('cognome');

my $parent = param("padre");
$parent =~ s/\?.*//;

# Controlli campi
my $formErr = checkError($nome,$cognome);

print "Content-type: text/html\n\n";
if($formErr > 0){
	print "<meta http-equiv='refresh' content='0; url=../profile.cgi?errore=$formErr' />";
}
else {
# =========== MODIFICA/AGGIUNTA NOME E COGNOME =========

	# recupero elemento radice
	my $rootUtenti=$docUser->getDocumentElement;
	
	#trovo il nodo nome
	my $userName = $rootUtenti->findnodes("//utente[email='$email']/nome")->get_node(1);
	$userName->removeChildNodes();
	$userName->appendText($nome);
	#trovo il nodo cognome
	my $userCogn = $rootUtenti->findnodes("//utente[email='$email']/cognome")->get_node(1);
	$userCogn->removeChildNodes();
	$userCogn->appendText($cognome);
	
	open(my $fo, '>', $fileUserXML) or die "Errore nell'apertura del file $fileUserXML ";
	print $fo $docUser->toString;
	close $fo;
	
	if("$parent" eq "carrello.cgi") {
		print "<meta http-equiv='refresh' content='0; url=../carrello.cgi' />";
	}else {
		print "<meta http-equiv='refresh' content='0; url=../profile.cgi?op=ok' />";
	}

}

