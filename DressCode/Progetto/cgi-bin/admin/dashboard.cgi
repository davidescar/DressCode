#!/usr/bin/perl -w

require "../header.cgi";

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

#======= COSTRUZIONE PARSER ============
makeUserParser("../../data/utenti.xml");

#========= CREAZIONE VARIABILI DI SESSIONE ======
makeSession();

print "Content-type: text/html\n\n";

#intestazione documento
$keywords = "gestione,amministratore,aggiunta,rimozione,modifica";
my $html_string = getHTMLHeader("Dashboard",$keywords);

#============ CORPO DASHBOARD ADMIN ==============
$html_string .="
<h2 class='ptitle'>Seleziona Attivit&agrave;</h2>
<ul id='dashList'>
	<li><a href='viewProducts.cgi' ".tabIndex().">Visualizza Elenco Prodotti</a></li>
	<li><a href='selectProd.cgi?form=0' ".tabIndex().">Aggiungi Nuovo Prodotto</a></li>
	<li><a href='selectProd.cgi?form=1' ".tabIndex().">Modifica Prodotto</a></li>
	<li><a href='selectProd.cgi?form=2' ".tabIndex().">Elimina Prodotto</a></li>
	<li><a href='selectProd.cgi?form=3' ".tabIndex().">Elimina Utente</a></li>
</ul>";

#footer e chiusura documento
$html_string .= getFooter();

#stampa del documento
printPrettyHTML($html_string);

