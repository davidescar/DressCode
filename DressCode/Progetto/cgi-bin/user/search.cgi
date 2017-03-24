#!/usr/bin/perl -w

require '../header.cgi';

use CGI;
use XML::LibXML;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

#======= COSTRUZIONE PARSER ============
makeUserParser("../../data/utenti.xml");
makeProductParser("../../data/prodotti.xml");
makeReviewParser("../../data/recensioni.xml");

#========= CREAZIONE VARIABILI DI SESSIONE ======
makeSession();

#======= PRELIEVO QUERY ========
my $query=param('query');
$query=lc $query; #trasformo in minuscolo la stringa query
$query=~ s/(\w+)/\u$1/g; #metto maiuscola la prima lettera

print "Content-type: text/html\n\n";

#intestazione documento
my $keywords = "risultati,ricerca,interrogazione,$query";
my $html_string = getHTMLHeader("Risultati Ricerca",$keywords);

#================= CORPO RICERCA =====================

$html_string .= "
<h2 id='search_title'><span id='listsearch'></span>Risultati ricerca per <span id='lower'>$query</span></h2>";	

@products=$docProd->findnodes("//prodotto[./nome[contains(.,'$query')] or ./tipologia[contains(.,'$query')]]");
$products=@products; #numero elementi array
if(!$products || "$query" eq ""){ #se vuoto oppure query di ricerca non specificata
	$html_string .= "<p class='no_results'>La ricerca non ha prodotto alcun risultato!</p>";
}else{
		
	$html_string .= "
	<ul id='search_list'>
		<li><p>La ricerca ha prodotto $products risultati!</p></li>";
		
		for $prod(@products){
		
			$printed_items++;
			my $codice = $prod->findnodes('attribute::codice');
			my $nome = $prod->findvalue('nome');
			my $prezzo = $prod->findvalue('prezzo');
			my $sconto = $prod->findvalue('prezzo/attribute::sconto');
			my $descrizione = $prod->findvalue('descrizione');
			my $tipologia = $prod->findvalue('tipologia');
			my $categoria = $prod->findvalue('categoria');
			my $immagine = $prod->findnodes('immaginiProdotto/immagine[1]/text()');
			my $prezScont = $prezzo-(($prezzo*$sconto)/100);

			$prezzo =~ s/\./,/;     # rimpiazza il punto con la virgola
			$prezScont=sprintf("%.2f",$prezScont);
			$prezScont =~ s/\./,/;     # rimpiazza il punto con la virgola
				
			$html_string .= "
			<li>
				<ul>
					<li class='p_img'>
						<span class='hid'>Immagine: </span>
						<a href='schedaProd.cgi?codice=$codice'>
							<img src='/$public_path/images/prodotti/$immagine' alt='foto $nome'/>
						</a>
					</li>
					<li class='p_name'>
						<a href='schedaProd.cgi?codice=$codice' ".tabIndex().">
							<span class='hid'>Nome: </span> $nome
						</a>
					</li>
					<li class='p_type'><span class='hid'>Tipologia: </span> $tipologia </li>
					<li class='p_price'><span class='hid'>Prezzo: </span>";
					if($sconto){
						my $sale_price = $prezzo - (($prezzo*$sconto)/100);
						$sale_price=sprintf("%.2f",$sale_price);
						$sale_price =~ s/\./,/; # rimpiazza il punto con la virgola
						$prezzo =~ s/\./,/; # rimpiazza il punto con la virgola
						$html_string .= "	<span class='sales'>$prezzo &euro;</span>$sale_price";
					}else{
						$prezzo =~ s/\./,/; # rimpiazza il punto con la virgola
						$html_string .= "$prezzo";
					}
					$html_string .= " &euro;
					</li>
					<li class='p_categ'><span class='hid'>Categoria: </span>$categoria</li>
				</ul>
			</li>";
			
			}	
			$html_string .= "</ul><a id='topAnchor' href='#title' ".tabIndex().">Torna su</a>";
}
		
#footer e chiusura documento
$html_string .= getFooter();

#stampa del documento
printPrettyHTML($html_string);
