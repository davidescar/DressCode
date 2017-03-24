#!/usr/bin/perl -w

require "../../header.cgi";

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

#======= COSTRUZIONE PARSER ============
# imposto il path del file dati
my $fileProdXML='../../../data/prodotti.xml';
makeProductParser($fileProdXML);

print "Content-type: text/html\n\n";

my $codice = param('codice');
my $promo = param('promo');
my $sconto = param('sconto');

#definisco un’espressione xpath
my $query = "//prodotto[\@codice = '$codice']/prezzo/attribute::sconto";
#recupero il nodo
my $node = $docProd->findnodes($query)->get_node(1);

#modifica
if("$promo" eq "aggiungi"){
	if("$sconto" ne "" && $sconto > 0 && $sconto < 100){
		$node->setValue($sconto);
		#serializzazione e salvataggio
		open(my $fo, '>', $fileProdXML) or die "Errore nell'apertura del file $fileProdXML ";
		print $fo $docProd->toString;
		close $fo;
		print "<meta http-equiv='refresh' content='0; url=/$cgi_path/user/schedaProd.cgi?codice=$codice' />";
	}else{
		print "<meta http-equiv='refresh' content='0; url=/$cgi_path/user/schedaProd.cgi?codice=$codice&amp;err_prom=1' />";
	}
}
else{ #rimuovo lo sconto dal prodotto
	$node->setValue(0);
	open(my $fo, '>', $fileProdXML) or die "Errore nell'apertura del file $fileProdXML ";
	print $fo $docProd->toString;
	close $fo;
	print "<meta http-equiv='refresh' content='0; url=/$cgi_path/user/schedaProd.cgi?codice=$codice' />";
}
