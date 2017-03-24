#!/usr/bin/perl -w

require "../header.cgi";
require "filters.cgi";

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

#======= COSTRUZIONE PARSER ============
makeUserParser("../../data/utenti.xml");
makeProductParser("../../data/prodotti.xml","../../data/recensioni.xml");

#========= CREAZIONE VARIABILI DI SESSIONE ======
makeSession();

#========== ARRAYs CATEGORIE =====
getCategories();

#======= VARIABILI FILTRI ===========
bindsReader();

print "Content-type: text/html\n\n";

#intestazione documento
my $keywords = "tutti,prodotti,lista,".lc(join(", ", @categorie)).",".lc(join(", ", @tipologie_totali));
my $html_string = getHTMLHeader("Lista Prodotti",$keywords);

#============= CORPO LISTA COMPLETA =============

$html_string .= "
<h2 class='ptitle'>Prodotti ". 
	(("$tipo" ne "/") ? "$tipo" : ""). 
	(("$prom" eq "yes") ? "in promozione" : "").
	"</h2>";

				
#============= FILTRI ==================
$html_string .= filtersPrinting();		
		
#============== RICERCA & INSERIMENTO PRODOTTI ==================

my $query = filtersQuery();
@products = $docProd->findnodes($query); #ricerca nel xml prodotti
my $numP = @products;
my $limI = ($lInf ? $lInf : 0); #limite inferiore visualizzazione prodotti
my $limS = ($lSup ? $lSup : 9); #limite superiore 

if($numP>0){ 
	
	$html_string .= limitsPrint($limI,$limS,$numP);

	#================ STAMPA PRODOTTI SELEZIONATI ===============
	
	$html_string .= "
	<h3>Lista Prodotti</h3>
	
	<ul id='productsList'>";
	for ($i=$limI; $i < $limS && $i < $numP; $i++){
		
		my $p = @products[$i];
		my $codice = $p->findvalue('attribute::codice');
		my $nome = $p->findvalue('nome');
		my $prezzo = $p->findvalue('prezzo');
		my $sconto = $p->findvalue('prezzo/attribute::sconto');
		my $tipologia = $p->findvalue('tipologia');
		my $categoria = $p->findvalue('categoria');
		my $immagine = $p->findnodes('immaginiProdotto/immagine[1]/text()');
		#stampa attributi nodi Prodotto selezionati
		
		#immagine prodotto
		$html_string .= "
		<li>
			<ul>
				<li class='p_img'>
					<span class='hid'>Immagine: </span>
					<a href='schedaProd.cgi?codice=$codice'>
					<img src='/$public_path/images/prodotti/$immagine' alt='foto $nome'/>
					</a>
				</li>
		
				<!-- nome prodotto -->
				<li class='p_name'>
					<a href='schedaProd.cgi?codice=$codice' ".tabIndex()."><span class='hid'>Nome: </span> $nome </a>
				</li>
		
				<!-- tipologia prodotto -->
				<li class='p_type'><span class='hid'>Tipologia: </span> $tipologia </li>
		
				<!-- prezzo -->
				<li class='p_price'><span class='hid'>Prezzo: </span>";		
				if($sconto){
					my $sale_price = $prezzo - (($prezzo*$sconto)/100);
					$sale_price=sprintf("%.2f",$sale_price);
					$sale_price =~ s/\./,/; # rimpiazza il punto con la virgola
					$prezzo =~ s/\./,/; # rimpiazza il punto con la virgola
					$html_string .= "<span class='sales'>$prezzo &euro;</span>$sale_price";
				}else{
					$prezzo =~ s/\./,/; # rimpiazza il punto con la virgola
					$html_string .= "$prezzo";
				}
				$html_string .= " &euro;</li>";
		
				#categoria
				$html_string .= (!$tipo ? "<li class='p_categ'><span class='hid'>Categoria: </span>$categoria</li>\n" : "");
		
			$html_string .= "
			</ul>
		</li>";
		
	}
	$html_string .= "</ul>";
	$html_string .= limitsPrint($limI,$limS,$numP);
	$html_string .= "<p id='topAnchor'><a href='#title' ".tabIndex().">Torna su</a></p>";
	
}#chiusura if prodotti non vuoti

else{ $html_string .= "<p>Non ci sono prodotti da visualizzare per questa categoria.</p>"; }

$html_string .= "<script type='text/javascript' src='/$public_path/js/toggleFilters.js'></script>";

#footer e chiusura documento
$html_string .= getFooter();

#stampa del documento
printPrettyHTML($html_string);

