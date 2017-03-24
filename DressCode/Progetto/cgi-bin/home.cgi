#!/usr/bin/perl -w

require "header.cgi";

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

#======= COSTRUZIONE PARSER ============
makeUserParser("../data/utenti.xml");
makeProductParser("../data/prodotti.xml");

#========= CREAZIONE VARIABILI DI SESSIONE ======
makeSession();

print "Content-type: text/html\n\n";

#intestazione documento
my $keywords = "home,promozioni,offerte,occasioni,sconti";
my $html_string = getHTMLHeader("Home",$keywords);

# ========== CORPO HOME ==========
$html_string .= "
<h2 id='prom_title'>Offerte da non perdere</h2>
	<ul id='prom_list'>";

my @promo = $docProd->findnodes("//prodotto[prezzo/attribute::sconto > 0]");
@promo = sort{$b->findvalue("prezzo/attribute::sconto") <=> $a->findvalue("prezzo/attribute::sconto")} @promo;
my $numProd = @promo; #numero di prodotti in promozione con lo sconto maggiore

if(!$numProd){ #non ci sono prodotti in promozione
	$html_string .= "<li id='no_products'>Nessun prodotto in promozione!</li>";
}else{ #visualizzo i primi tre prodotti in promozione con lo sconto maggiore
	
	for (my $i=0; $i<3 && $i<$numProd; $i++){
			
		my $prod = @promo[$i];
		my $codice = $prod->findnodes('attribute::codice');
		my $nome = $prod->findvalue('nome');
		my $prezzo = $prod->findvalue('prezzo');
		my $sconto = $prod->findvalue('prezzo/attribute::sconto');
		my $descrizione = $prod->findvalue('descrizione');
		my $categoria = $prod->findvalue('categoria');
		my $immagine = $prod->findnodes('immaginiProdotto/immagine[1]/text()');
		my $prezScont = $prezzo-(($prezzo*$sconto)/100);

		$prezzo =~ s/\./,/;     # rimpiazza il punto con la virgola
		$prezScont=sprintf("%.2f",$prezScont);
		$prezScont =~ s/\./,/;     # rimpiazza il punto con la virgola

		$html_string .= "		
		<li>
			<dl>
				<dt>Articolo ".($i+1)."</dt>
				<dd class='art_images'>
					<a href='user/schedaProd.cgi?codice=$codice'>
					<img src='/$public_path/images/prodotti/$immagine' alt='$nome immagine' />
					</a>
				</dd>
				<dd class='art_titles'>
					<a href='user/schedaProd.cgi?codice=$codice' ".tabIndex().">$nome</a>
				</dd>
				<dd class='art_descrs'>$descrizione</dd>
				<dd class='art_categ'>$categoria</dd>
				<dd class='art_price'><span class='sales'>$prezzo &euro;</span>$prezScont &euro;</dd>
			</dl>
		</li>";

	}
}
$html_string .= "</ul>";

#footer e chiusura documento
$html_string .= getFooter();

#stampa del documento
printPrettyHTML($html_string);
