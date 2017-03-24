#!/usr/bin/perl -w

require "../../header.cgi";

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

# imposto il path del file dati
my $fileProdXML='../../../data/prodotti.xml';
makeProductParser($fileProdXML);

makeUserParser("../../../data/utenti.xml");

#========= CREAZIONE VARIABILI DI SESSIONE ======
makeSession();

#ricavo il contenuto del widget 'selProd'
my $codice = param('selProd');

# recupero elenco prodotti
my $query="//prodotto[\@codice='$codice']";
my $prod = $docProd->findnodes($query)->get_node(1);

my $nome = $prod->findvalue('nome');

# ricavo il valore del parametro confirmDel per sapere
# se è stata confermata la scelta di eliminare il prodotto
my $confirmDel= param('confirmDel');

print "Content-type: text/html\n\n";

#intestazione documento
$keywords = "conferma,eliminazione,prodotto";
my $html_string = getHTMLHeader("Conferma Eliminazione Prodotto",$keywords);
		
$html_string .= "
<h2 class='ptitle'>Elimina Prodotto</h2>";
			  
if(!$confirmDel){
	
$html_string .= "

<form id='confirmDel' action='deleteProd.cgi' method='post'>
<!-- input per verificare che sia stato effettuato il submit del form -->

	<fieldset>
		<p>Sei sicuro di voler eliminare il prodotto selezionato?</p>
		<p>Codice Prodotto: <span>$codice</span></p>
		<p>Nome Prodotto: <span>$nome</span></p>
		<input type='hidden' name='confirmDel' value='conferma eliminazione' />
		<input type='hidden' name='selProd' value='$codice' />
		<input class='psubmit' type='submit' value='Conferma Eliminazione'/>
	</fieldset>
	
</form>";

}
else{

	#trovo il nodo
	my $prodotto = $docProd->findnodes("//prodotto[\@codice='$codice']")->get_node(1);
	#mi sposto sul padre
	my $prodotti = $prodotto->parentNode;
	#elimino il figlio
	$prodotti->removeChild($prodotto);
	
	open(my $fo, '>', $fileProdXML) or die "Errore nell'apertura del file $fileProdXML ";
	print $fo $docProd->toString;
	close $fo;
	
	printPrettyXML($fileProdXML);
	
	$html_string .= "<p class='success_msg'>Eliminazione del prodotto avvenuta con successo!</p>";
	
}

$html_string .= "<p class='success_link'><a href='../../home.cgi' ".tabIndex().">Torna alla home</a></p>";

#footer e chiusura documento
$html_string .= getFooter();

#stampa del documento
printPrettyHTML($html_string);
