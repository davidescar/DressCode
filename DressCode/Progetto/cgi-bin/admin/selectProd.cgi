#!/usr/bin/perl -w

require "../header.cgi";

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

#======= COSTRUZIONE PARSER ============
makeUserParser("../../data/utenti.xml");
makeProductParser("../../data/prodotti.xml");
makeReviewParser("../../data/recensioni.xml");

getCategories();
my @title = ("Inserimento Nuovo Prodotto","Modifica Prodotto","Eliminazione Prodotto","Eliminazione Utente");
my @action = ("inserire","modificare","eliminare","eliminare");
my @target = ("formAddProd.cgi","formModProd.cgi","function/deleteProd.cgi","function/deleteUser.cgi");
my @name = ("tipo","codice","selProd","selUser");

#========= CREAZIONE VARIABILI DI SESSIONE ======
makeSession();

#========== PRELIEVO INFO FORM ===========
my $form = param("form");

my @stack = getElements($form);

print "Content-type: text/html\n\n";
#intestazione documento
$keywords = "selezione,prodotto,utente";
my $html_string = getHTMLHeader("Selezione",$keywords);

#================== CORPO FORM SELEZIONE PRODOTTO =================	

my $subject = $form == 3 ? "utente" : "prodotto";

$html_string .= "
<h2 class='ptitle'>@title[$form]</h2>
<p class='choiceAlert'>Selezionare $subject che si desidera @action[$form]</p>
<form class='typeSelection' action='@target[$form]' method='post'>
	<ul>
		<li>
			<select class='pselect' name='@name[$form]' ".tabIndex().">";
			for my $element (@stack){ $html_string .= getOption($form,$element); }
			$html_string .= "
			</select>
		</li>
		<li><input type='submit' value='Conferma' class='psubmit' ".tabIndex()." /></li>
	</ul>
</form>";

#footer e chiusura documento
$html_string .= getFooter();

#stampa del documento
printPrettyHTML($html_string);

#riempio array con elementi per l'option in base al form selezionato
sub getElements {
	
	# recupero elenchi utenti e prodotti
	my @utenti = $docUser->findnodes("//utente");
	my @prodotti = $docProd->findnodes("//prodotto");
	
	my $form = $_[0];
	
	if($form == 0) { return @tipologie_totali; }
	if($form == 1 || $form == 2) { return @prodotti; }	
	if($form == 3) { return @utenti; }	
	
	return;
	
}

#stampo tag option con elementi necessari in base scelta form
sub getOption {
	
	my $form = $_[0];
	my $element = $_[1];
	
	if($form == 0) { return "<option value='$element'>$element</option>"; }
	if($form == 1 || $form == 2) { 
		my $codice = $element->getAttribute('codice');
		my $nome = $element->findnodes('nome/text()');
		my $tipologia = $element->findnodes('tipologia/text()');
		my $categoria = $element->findnodes('categoria/text()');
		my $info = $codice." - ".$nome." (".$tipologia." ".$categoria.")";
		return "<option value='$codice'>$info</option>";
	}
	if($form == 3) { 
		my $email = $element->findnodes('email/text()');
		my $nome = $element->findnodes('nome/text()');
		my $cognome = $element->findnodes('cognome/text()');
		return "<option value='$email'>$email".(($nome && $cognome) ? " - $nome $cognome" : "")."</option>"; 
	}
	
	return "";
	
}
