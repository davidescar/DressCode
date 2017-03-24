#!/usr/bin/perl -w

require "../header.cgi";

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

#======= COSTRUZIONE PARSER ============
makeUserParser("../../data/utenti.xml");
makeOrdersParser("../../data/ordini.xml");
makeProductParser("../../data/prodotti.xml");

#========= CREAZIONE VARIABILI DI SESSIONE ======
makeSession();

print "Content-type: text/html\n\n";


#intestazione documento
my $keywords = "storico,ordini,acquisti,effettuati";
my $html_string = getHTMLHeader("Storico Ordini",$keywords);

#========== CORPO CARRELLO ===========

$html_string .= "	
<h2 class='ptitle'>Storico Ordini</h2>";

my @orders = $docOrder->findnodes("//ordine[email='$email']");

if (!defined @orders){	$html_string .= "<p class='simple_msg'>Nessun ordine trovato.</p>"; }
else{
	$html_string .= "<ol id='orders_list'>";
	for $ord(@orders) {
		
		my $tot = 0;
		my $data = $ord->findvalue("data");
		my $spedizione = $ord->findvalue("attribute::spedizione");
		$spedizione=~ s/(\w+)/\u$1/g; #metto maiuscola la prima lettera
		my @prods = $ord->findnodes("prodottiAcquistati/prodotto");
		my @d=split("-",$data);
		$data=@d[2]."-".@d[1]."-".@d[0];
		$html_string .= "
		<li>
			<p class='date_ord'>Data Ordine: $data</p><p class='sped_ord'>Spedizione: $spedizione";
			if("$spedizione" eq "Standard"){
				$html_string .= " (+2,00 &euro;)";
			}
			if("$spedizione" eq "Express"){
				$html_string .= " (+5,00 &euro;)";
			}
			$html_string .="</p>
			<table class='order_table' summary='Questa tabella contiene tutti i prodotti che utente $email ha acquistato in data $data. Ogni prodotto e&grave; descritto da: immagine rappresentativa, nome, taglia, colore, prezzo e quantita&grave;. Infine e&grave; riassunto il totale della transazione.'>
				<caption>Lista prodotti acquistati nell'ordine del $data</caption>	
				<thead>
					<tr>
						<th scope='col'>Immagine</th>
						<th scope='col'>Nome</th>
						<th class='hide_t' scope='col'>Taglia</th>
						<th class='hide_t' scope='col'>Colore</th>
						<th scope='col'>Prezzo</th>
						<th scope='col'>Quantit&agrave;</th>
					</tr>
				</thead>
				<tbody>";
					
			for $p(@prods) {
				my $codice = $p->findvalue("codice");
				my $nome = $p->findvalue("nome");
				my $prezzo = $p->findvalue("prezzo");
				my $taglia = $p->findvalue("taglia");
				my $colore = $p->findvalue("colore");
				my $quantita = $p->findvalue("quantita");
				my $immagine = $docProd->findnodes("//prodotto[attribute::codice='".$codice."']/immaginiProdotto/immagine[1]/text()");
				$tot = $tot + $prezzo*$quantita;
				$prezzo =~ s/\./,/; # rimpiazza il punto con la virgola
				$html_string .= "
				<tr>
					<td><img src='/$public_path/images/prodotti/$immagine' alt='foto $nome'/></td>
					<td class='name_pad'><a href='schedaProd.cgi?codice=$codice' ".tabIndex().">$nome</a></td>						
					<td class='hide_t'>$taglia</td>
					<td class='hide_t'>$colore</td>
					<td>$prezzo &euro;</td>
					<td>$quantita</td>
				</tr>";
			}
			
			if("$spedizione" eq "Standard"){
				$tot+=2.00;
			}
			if("$spedizione" eq "Express"){
				$tot+=5.00;
			}

			$tot=sprintf("%.2f",$tot);
			$tot =~ s/\./,/; # rimpiazza il punto con la virgola
			$html_string .= "
				</tbody>	
			</table>
			<p class='tot_ord'>Totale: $tot &euro;</p>
		</li>";
		
	}	
	$html_string .= "</ol>";
}#else

#footer e chiusura documento
$html_string .= getFooter();

#stampa del documento
printPrettyHTML($html_string);
