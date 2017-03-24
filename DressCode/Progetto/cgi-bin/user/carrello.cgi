#!/usr/bin/perl -w

require "../header.cgi";

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

#======= COSTRUZIONE PARSER ============
makeUserParser("../../data/utenti.xml");
makeProductParser("../../data/prodotti.xml");

#========= CREAZIONE VARIABILI DI SESSIONE ======
makeSession();
my $numProd = $session->param("numProd");
my $checkSped=param("err_sped");

print "Content-type: text/html\n\n";

#intestazione documento
my $keywords = "carrello,prodotti";
my $html_string = getHTMLHeader("Carrello",$keywords);

#========== CORPO CARRELLO ===========
$html_string .= "<h2 class='ptitle'>Carrello</h2>";

if(!$numProd){

	if(param('ins')){
		$html_string .= "<p id='order_ok'>Ordine effettuato con successo!</p>
		<p class='success_link'>Torna alla&nbsp;<a href='../home.cgi'>home</a>.</p>";
	}else {
		$html_string .= "<p id='cart_alert'>Carrello vuoto!</p>";
	}

}else{
	
	if(param("missN") || param("missI") || param("missC") || param("err_sped")) {
		$html_string .= "<p class='msgerror'>Errore: dati non corretti per effettuare l'ordine.</p>";
	}
	
	$html_string .= "
	<table id='cart_table' summary='Questa tabella contiene tutti i prodotti che utente $email ha aggiunto al carrello e che intende acquistare. Ogni prodotto è descritto da: immagine rappresentativa, nome, taglia, colore, prezzo e quantità'>
		<caption>Lista prodotti presenti attualmente nel carrello</caption>
		<thead>
			<tr><th>Immagine</th><th>Nome</th><th>Taglia</th><th class='hide_t'>Colore</th><th class='hide_t'>Prezzo</th><th>Quantit&agrave;</th></tr>
		</thead>
		<tbody>";
		my $tot=0;
		for(my $i=1; $i<=$numProd; $i++){
	
			my $codice=@{$session->param("prod".$i)}[0];
			my $taglia=@{$session->param("prod".$i)}[1];
			my $colore=@{$session->param("prod".$i)}[2];
			my $quant=$session->param("qnt".$i);
			my $name=$docProd->findvalue("//prodotto[attribute::codice='$codice']/nome");
			my $sconto=$docProd->findvalue("//prodotto[attribute::codice='$codice']/prezzo/attribute::sconto");
			my $price=$docProd->findvalue("//prodotto[attribute::codice='$codice']/prezzo");
			my $immagine = $docProd->findnodes("//prodotto[attribute::codice='$codice']/immaginiProdotto/immagine[1]/text()");
			
			#applico lo sconto al prezzo del prodotto
			$price=$price-(($price*$sconto)/100);
			$price=sprintf("%.2f",$price);
			$price =~ s/\./,/; # rimpiazza il punto con la virgola
		
			$html_string .= "
			<tr>
				<td><a href='schedaProd.cgi?codice=$codice'><img src='/$public_path/images/prodotti/$immagine' alt='foto $name'/></a></td>
				<td><a href='schedaProd.cgi?codice=$codice' ".tabIndex().">$name</a></td>				
				<td class='hide_t'>$taglia</td>
				<td class='hide_t'>$colore</td>
				<td>$price &euro;</td>
				<td>
					<ul class='quantity'>
						<li>$quant</li>
						<li><a href='function/changeAmount.cgi?numero=$i&amp;op=Add'><span class='hid'>Aggiungi</span></a></li>
						<li><a href='function/changeAmount.cgi?numero=$i&amp;op=Rmv'><span class='hid'>Rimuovi</span></a></li>
					</ul>
				</td>
			</tr>";
		
			$price =~ s/,/./; #sostituzione , con . per somma float
			$tot = $tot + ($price * $quant);
	}
	
	$tot=sprintf("%.2f",$tot);
	$tot =~ s/\./,/; # rimpiazza il punto con la virgola
	
	my $nome = $docUser->findvalue("//utente[email='$email']/nome");
	my $cognome = $docUser->findvalue("//utente[email='$email']/cognome");
	my $indirizzo = $docUser->findvalue("//utente[email='$email']/indirizzo");
	my $citta = $docUser->findvalue("//utente[email='$email']/citta");
	my $CAP = $docUser->findvalue("//utente[email='$email']/CAP");
	my $nazione = $docUser->findvalue("//utente[email='$email']/nazione");
	my $carta = $docUser->findvalue("//utente[email='$email']/carta");
	my $circuito = $docUser->findvalue("//utente[email='$email']/carta/attribute::circuito");
	
	#divido in 4 carta e inserisco -
	$carta =~ s/(.{4})/$1 - /gs; substr ($carta, -2) = "";

	$html_string .= "
		</tbody>
	</table>";
	
	$html_string .= "
	<p id='totale'>Totale acquisti: $tot &euro;</p>".
	(("$checkSped" eq "1") ? "<p class='msgerror'>Metodo di spedizione non selezionato!</p>" : "")."
	
	<form id='add_purchase' action='function/addPurchase.cgi' method='post'>
		<h3><span id='spedizione'></span>Metodo di spedizione</h3>
		<ul>
			<li>				
				<label for='spGr'>Gratuita</label>
				<input type='radio' id='spGr' name='spedizione' value='gratuita' / ".tabIndex().">
				<p class='info_sped'>Consegna prevista in 4-5 giorni lavorativi (+0,00 &euro;)</p>
			</li>
			<li>				
				<label for='spSt'>Standard</label>
				<input type='radio' id='spSt' name='spedizione' value='standard' / ".tabIndex().">
				<p class='info_sped'>Consegna prevista in 3-4 giorni lavorativi (+2,00 &euro;)</p>
			</li>
			<li>
				<label for='spEx'>Express</label>
				<input type='radio' id='spEx' name='spedizione' value='express' / ".tabIndex().">
				<p class='info_sped'>Consegna prevista in 1-2 giorni lavorativi (+5,00 &euro;)</p>
			</li>
		</ul>
		<h3><span id='identita'></span>Nome e Cognome</h3>".
		(("$nome" ne "" && "$cognome" ne "") ? "<p>$nome $cognome - <a href='profile.cgi?form=profile' ".tabIndex().">Modifica</a></p>" 
		: "<p class='msgerror'>Non Specificati - Inserisci <a href='profile.cgi?form=profile' ".tabIndex().">Nome e Cognome Utente</a></p>")."
		<h3><span id='address'></span>Indirizzo di spedizione</h3>".
		(("$indirizzo" ne "") ? "<p>$indirizzo, $citta ($CAP) - $nazione - <a href='profile.cgi?form=address' ".tabIndex().">Modifica</a></p>" 
		: "<p class='msgerror'>Non Specificato - Inserisci <a href='profile.cgi?form=address' ".tabIndex().">Indirizzo Spedizione</a></p>")."
		<h3><span id='pagamento'></span>Metodo di pagamento</h3>".
		(("$carta" ne "") ? "<p>$circuito $carta - <a href='profile.cgi?form=credit' ".tabIndex().">Modifica</a></p>" 
		: "<p class='msgerror'>Non Specificato - Inserisci <a href='profile.cgi?form=credit' ".tabIndex().">Numero Carta di Credito</a></p>")."
		<p><input type='submit' class='psubmit' name='acquisto' value='Procedi' / ".tabIndex()."></p>
	</form>";
	
	#controllo eventuali errori creati dall'acquisto
	if(param("missN") || param("missI") || param("missC")) {	
		$html_string .= "
		<p class='msgerror'>ATTENZIONE: per poter effettuare l'ordine è necessario specificare le seguenti informazioni</p>
		<ul id='error_list'>".
		(param("missN") ? "<li><a href='profile.cgi?form=profile' ".tabIndex().">Nome e Cognome Utente</a></li>" : "").
		(param("missI") ? "<li><a href='profile.cgi?form=address' ".tabIndex().">Indirizzo Spedizione</a></li>" : "").
		(param("missC") ? "<li><a href='profile.cgi?form=credit' ".tabIndex().">Numero Carta di Credito</a></li>" : "").
		"</ul>";
	}
		
}#else

#footer e chiusura documento
$html_string .= getFooter();

#stampa del documento
printPrettyHTML($html_string);
