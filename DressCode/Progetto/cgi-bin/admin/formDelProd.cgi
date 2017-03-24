#!/usr/bin/perl -w

require "../header.cgi";

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

#======= COSTRUZIONE PARSER ============
makeUserParser("../../data/utenti.xml");
makeProductParser("../../data/prodotti.xml");
makeReviewParser("../../data/recensioni.xml");

# recupero elemento radice
my $rootProd=$docProd->getDocumentElement;

# recupero elenco prodotti
my $query='//prodotto';
my @prodotti=$docProd->findnodes($query);

#========= CREAZIONE VARIABILI DI SESSIONE ======
makeSession();

if(param('ins')) {

	print "Content-type: text/html\n\n";

	#intestazione documento
	$keywords = "eliminazione,rimozione,prodotto";
	my $html_string = getHTMLHeader("Eliminazione Prodotto",$keywords);

	$html_string .= "<h2 class='ptitle'>Eliminazione prodotto</h2>";
	$html_string .= "<p class='success_msg'>Eliminazione avvenuta con successo!</p>";
	
	#footer e chiusura documento
	$html_string .= getFooter();

	#stampa del documento
	printPrettyHTML($html_string);

}
else{

	#redirect alla pagina di selezione utente
	my $query=new CGI;
	print $query->redirect('selectProd.cgi?form=2');
	
}
