#!/usr/bin/perl -w

require "../../header.cgi";

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

#======= COSTRUZIONE PARSER ============
my $fileRecXML="../../../data/recensioni.xml";
makeReviewParser($fileRecXML);

# recupero elemento radice
my $rootRec = $docRec->getDocumentElement;

#ricavo il contenuto del widget 'selUser' e 'selProd'
my $username= param('selUser');
my $codice= param('selProd');

print "Content-type: text/html\n\n";

#trovo il nodo
my $recensione = $docRec->findnodes("//rec[attribute::autore='$username' and attribute::codice='$codice']")->get_node(1);
#mi sposto sul padre
my $recensioni = $recensione->parentNode;
#elimino il figlio
$recensioni->removeChild($recensione);

open(my $fo, '>', $fileRecXML) or die "Errore nell'apertura del file $fileRecXML ";
print $fo $docRec->toString;
close $fo;

printPrettyXML($fileRecXML);

print "<html><head><meta http-equiv='refresh' content='0; url=../../user/schedaProd.cgi?codice=$codice' /></head></html>";
