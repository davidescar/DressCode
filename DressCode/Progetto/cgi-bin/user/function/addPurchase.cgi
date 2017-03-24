#!/usr/bin/perl -w

require "../../header.cgi";

use Time::Piece;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

#======= COSTRUZIONE PARSER ============
makeUserParser("../../../data/utenti.xml");
makeProductParser("../../../data/prodotti.xml");

#creazione parser ordini
my $fileOrdiniXML = "../../../data/ordini.xml";
makeOrdersParser($fileOrdiniXML);

#========= CREAZIONE VARIABILI DI SESSIONE ======
makeSession();
my $numProd = $session->param("numProd");
my $spedizione = param("spedizione");

#========== RECUPERO VALORI NECESSARI ==========
my $data = localtime->ymd('-');

#========= CONTROLLO DATI UTENTE ==========
# recupero elemento radice
my $rootUser = $docUser->getDocumentElement;

#recupero tutti gli utenti
my $nome = $rootUser->findvalue("//utente[email='$email']/nome");
my $indirizzo = $rootUser->findvalue("//utente[email='$email']/indirizzo");
my $carta = $rootUser->findvalue("//utente[email='$email']/carta");

print "Content-type: text/html\n\n";

if(!$spedizione || !$nome || !$indirizzo || !$carta){
	print "<html><head><meta http-equiv='refresh' content='0; url=../carrello.cgi?"
			.(!$spedizione ? "&amp;err_sped=1" : "")
			.(!$nome ? "&amp;missN=yes" : "")
			.(!$indirizzo ? "&amp;missI=yes" : "")
			.(!$carta ? "&amp;missC=yes" : "")
			."' /></head></html>";
}else{
					
	#preparo un codice per l'ordine
	#codice come attributo
	my $query="/*/ordine[not(\@codice<../ordine/\@codice)]/\@codice";
	my $codice = $docOrder->findnodes($query)->get_node(1);
	if($codice){
		$codice = $codice->nodeValue + 1;
		$lunCod = length($codice);
		$zeriCod = "";
		for($numZeri=$lunCod ; $numZeri<5 ; $numZeri++){
			$zeriCod .= "0";
		}
		$codice = $zeriCod . $codice;
	}
	else{ $codice = "00001"; }

	#======== CREAZIONE FRAMMENTO =========
	
	#cerco il nodo a cui inserire un figlio
	my $padre = $docOrder->findnodes("//so:ordiniEffettuati")->get_node(1);
	
	#costruisco il frammento per il nodo ordine
	my $ordine = $docOrder->createElement("ordine");
	$ordine->setAttribute("codice",$codice);
	$ordine->setAttribute("spedizione",$spedizione);
	
	#creo tag email e data
	$ordine->appendChild($docUser->createElement("email"));
	$ordine->appendChild($docUser->createElement("data"));
	$ordine->findnodes("email")->get_node(1)->appendText($email);
	$ordine->findnodes("data")->get_node(1)->appendText($data);
	
	my $prodAcq = $docOrder->createElement("prodottiAcquistati");
	
	#inserimento prodotti
	for(my $i=1; $i<=$numProd; $i++){
		
		my $codice=@{$session->param("prod".$i)}[0];
		my $taglia=@{$session->param("prod".$i)}[1];
		my $colore=@{$session->param("prod".$i)}[2];
		my $quant=$session->param("qnt".$i);
		my $name=$docProd->findvalue("//prodotto[attribute::codice='$codice']/nome");
		my $price=$docProd->findvalue("//prodotto[attribute::codice='$codice']/prezzo");
		my $sconto=$docProd->findvalue("//prodotto[attribute::codice='$codice']/prezzo/attribute::sconto");
		$price=$price-(($price*$sconto)/100);
		$price=sprintf("%.2f",$price);
		
		#costruisco il frammento per il nodo prodotto
		my $prodotto = $docOrder->createElement("prodotto");
		my @info = ("codice","nome","prezzo","taglia","colore","quantita");
		foreach my $i(@info) { $prodotto->appendChild($docOrder->createElement($i)); } 
		
		#inserisco i nuovi valori
		my $v = 0;
		my @valori = ($codice,$name,$price,$taglia,$colore,$quant);
		foreach my $i(@info) { $prodotto->findnodes($i)->get_node(1)->appendText(@valori[$v++]); } 
		
		$prodAcq->appendChild($prodotto);
		
	}
	
	#chiudo il frammento
	$ordine->appendChild($prodAcq);

	#======== INSERIMENTO NEL FILE XML ============
	#aggiungo il nodo
	my $nodo = $parserOrder->parse_balanced_chunk($ordine)
			|| die('frammento non ben formato');
	$padre->appendChild($ordine);
	
	open(my $fo, '>', $fileOrdiniXML) or die "Errore nell'apertura del file ".$fileOrdiniXML." ";
	print $fo $docOrder->toString;
	close $fo;
	
	printPrettyXML($fileOrdiniXML);

	$session->param("numProd",0); #svuoto carrello utente

	print "<html><head><meta http-equiv='refresh' content='0; url=../carrello.cgi?ins=ok' /></head></html>";
	
}
