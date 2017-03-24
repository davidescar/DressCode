#!/usr/bin/perl -w

require "../../header.cgi";

use XML::LibXML;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

#======= COSTRUZIONE PARSER ============
my $fileUserXML='../../../data/utenti.xml';
makeUserParser($fileUserXML);

# recupero elemento radice
my $rootUser=$docUser->getDocumentElement;

#ricavo il contenuto del widget 'selUser'
my $email= param('selUser');

print "Content-type: text/html\n\n";

#trovo il nodo
my $utente = $docUser->findnodes("//utente[email='$email']")->get_node(1);
#mi sposto sul padre
my $utenti = $utente->parentNode;
#elimino il figlio
$utenti->removeChild($utente);

open(my $fo, '>', $fileUserXML) or die "Errore nell'apertura del file $fileUserXML ";
print $fo $docUser->toString;
close $fo;

printPrettyXML($fileUserXML);

print "<html><head><meta http-equiv='refresh' content='0; url=../formDelUser.cgi?ins=ok' /></head></html>"; 
