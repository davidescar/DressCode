#!/usr/bin/perl -w

require "../header.cgi";

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

#======= COSTRUZIONE PARSER ============
makeUserParser("../../data/utenti.xml");
makeProductParser("../../data/prodotti.xml");

#========= CREAZIONE VARIABILI DI SESSIONE ======
makeSession();

print "Content-type: text/html\n\n";

#intestazione documento
$keywords = "tutti,prodotti,lista,completa,totale";
my $html_string = getHTMLHeader("Lista Completa Prodotti",$keywords);

#============= CORPO LISTA COMPLETA =============

my $lower = (param("lower") ? param("lower") : 0);
my $upper = (param("upper") ? param("upper") : 10);

my @products = $docProd->findnodes("//prodotto"); #ricerca di tutti i prodotti in prodotti.xml
my $numP = @products; #numero di prodotti da visualizzare

if($upper > $numP){ $upper = $numP; }

$html_string .= "
<h2 class='ptitle'>Elenco Completo Prodotti</h2>
<p>Nel database sono presenti $numP prodotti</p>
<p>".($lower ? "<a class='aprev' href='viewProducts.cgi?lower=".($lower-10)."&amp;upper=".($lower)."' ".tabIndex().">Precedenti </a>" : "").
	(($upper != $numP)  ? "<a class='anext' href='viewProducts.cgi?lower=".($upper)."&amp;upper=".($upper+10)."' ".tabIndex().">Successivi</a> " : "")."</p>
<ul id='lista_prodotti'>";
	
for (my $i = $lower; $i < $upper; $i++){
	
	my $p = @products[$i];
	
	my $codice = $p->findvalue('attribute::codice');
	my $nome = $p->findvalue('nome');
	my $materiale= $p->findvalue('materiale');
	my $prezzo = $p->findvalue('prezzo');
	my $sconto = $p->findvalue('prezzo/attribute::sconto');
	my $tipologia = $p->findvalue('tipologia');
	my $categoria = $p->findvalue('categoria');
	my $immagine = $p->findvalue('immaginiProdotto/immagine[1]');
	my @taglie = $p->findnodes('taglieDisponibili/taglia/text()');
	my @colori = $p->findnodes('coloriDisponibili/colore/text()');

	my $prezScont=$prezzo;
	if($sconto>0){
		$prezScont=$prezzo-(($prezzo*$sconto)/100);
		
	}

	$prezzo =~ s/\./,/; # rimpiazza il punto con la virgola
	$prezScont=sprintf("%.2f",$prezScont);
	$prezScont =~ s/\./,/; # rimpiazza il punto con la virgola	
	
	$html_string .= "
	<li class='main_item' id='prod".$i."'>
	
		<label for='prod".$i."'>Prodotto ".($i+1)."</label>
		<ul class='plist'>
						
			<li class='pimg'>
				<span>Immagine:</span>
				<a href='../user/schedaProd.cgi?codice=$codice'>
					<img src='/$public_path/images/prodotti/$immagine' alt='$nome immagine' />
				</a>
			</li>
			
			<li class='pcod'><span>Codice:</span>$codice</li>
			
			<li class='pnom'>
				<span>Nome:</span></dt>
				<a href='../user/schedaProd.cgi?codice=$codice' ".tabIndex().">$nome</a>
			</li>
			
			<li class='ppre'>
				<span class='hid'>Prezzo:</span>".($sconto>0 ? "<span class='sales'>$prezzo &euro;</span> $prezScont &euro;" : "$prezzo &euro;")."
			</li>".

			($sconto > 0 ? "<li class='pscont'><span>Sconto:</span>$sconto%</li>" : "")
			
			."<li class='pcat'><span>Categoria:</span>$categoria</li>
									
			<li class='ptip'><span>Tipologia:</span>$tipologia</li>
			
			<li class='pmat'><span>Materiale:</span>$materiale</li>

			<li class='ptag'>
				<span>Taglie:</span>";
			
			my $ntag=@taglie;
			if($ntag==0){
				$html_string .= " ---"; 
			}else{
				for(my $j=0; $j < $ntag; $j++){
					$html_string .= @taglie[$j];
					$html_string .= ($j<$ntag-1 ? "," : "");
				}
			}
				
			$html_string .=  "</li>
			
			<li class='pcol'>
				<span>Colori:</span>";
				my $ncol=@colori;
				if($ncol==0){
					$html_string .= " ---";
				}else{
					$html_string .= "<ul>";	
					
					for(my $j=0; $j<$ncol; $j++){
						$html_string .= "
						<li>
							<span class='color_n'>".@colori[$j]."</span>
							<span id='circle".@colori[$j]."' class='colorSpan' ></span>
						</li>";
					}
					$html_string .= "</ul>";
				}
	
			$html_string .= "
			</li>
			
			<li class='pmod'><a href='formModProd.cgi?codice=$codice' ".tabIndex().">Modifica</a></li>
			<li class='pdel'><a href='function/deleteProd.cgi?selProd=$codice' ".tabIndex().">Elimina</a></li>
			
		</ul>
			
	</li>";
		
}
$html_string .= "
</ul>
<p>".($lower ? "<a class='aprev' href='viewProducts.cgi?lower=".($lower-10)."&amp;upper=".($lower)."' ".tabIndex().">Precedenti </a>" : "").
	(($upper != $numP)  ? "<a class='anext' href='viewProducts.cgi?lower=".($upper)."&amp;upper=".($upper+10)."' ".tabIndex().">Successivi</a> " : "")."</p>
<p><a id='topAnchor' href='#title' ".tabIndex().">Torna su</a></p>";

#footer e chiusura documento
$html_string .= getFooter();

#stampa del documento
printPrettyHTML($html_string);
