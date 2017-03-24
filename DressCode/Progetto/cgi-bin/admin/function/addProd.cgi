#!/usr/bin/perl -w

require "../header.cgi";
require "function/utility.cgi";

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

sub addProduct{

	#======= COSTRUZIONE PARSER ============
	# imposto il path del file dati
	my $fileProdXML='../../data/prodotti.xml';
	makeProductParser($fileProdXML);
	
	#======= LETTURA DATI FORM ========
	my $tipo = param('tipo');
	my $nome = param('nome');
	my $categ = param('categ');
	my $materiale = param('materiale');
	my $prezzo = param('prezzo');
	my $descr = param('descr');	
	my @taglie = param('taglie');	
	my @colori = param('colors');
		
	my $valuta="euro";
	
	my @fields = ("tipologia","nome","categ","materiale","descrizione");
	my @values = ($tipo,$nome,$categ,$materiale,$descr);
	
	#=================== CONTROLLO CAMPI ================
	my $error_message = "";

	#controllo campi vuoti
	for(my $i = 0; $i < 5; $i++) { $error_message .= isEmpty(@values[$i],@fields[$i]); }
	
	#controllo prezzo
	$error_message .= isValidPrice($prezzo);

	#controllo taglie
	$error_message .= ( @taglie < 1 ? "<li>Nessuna taglia selezionata.</li>" : "");

	#controllo colori
	$error_message .= ( @colori < 1 ? "<li>Nessuna categoria di colore selezionata.</li>" : "");

	#controllo immagini
	my $numImm = 3;
	for(my $i = 0 ; $i < $numImm; $i++){
		
		my $immagine = param("immagine".$i);
		
		my $error = isEmpty($immagine,"immagine ".($i+1));		
		$error_message .= (length $error ? $error : isValidImage($immagine));

	}
	
	if(!length $error_message){
		
		#============ INSERIMENTO PRODOTTO ==============
		
		# cerco il nodo a cui inserire un figlio
		my $padre = $docProd->findnodes("//so:catalogo")->get_node(1);
					
		# preparo un codice per il prodotto
		my $query = "/*/prodotto[not(\@codice<../prodotto/\@codice)]/\@codice";
		my $codice = $docProd->findnodes($query)->get_node(1);
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
		
		# aggiustamenti per il nome
		$nome =~ s/(\w+)/\u$1/g; #metto maiuscola la prima lettera
		
		# aggiustamenti per il prezzo
		$prezzo =~ s/,/\./;     # rimpiazza un'eventuale virgola con il punto
		
		# trasformo il contenuto di $prezzo in un numero con 2 cifre dopo la virgola
		$prezzo = sprintf( '%.2f', $prezzo );
		
		# aggiustamenti per la descrizione
		# rimpiazzo un'eventuale carattere accentato con la relativa sequenza unicode
		$descr =~ s/à/\&agrave;/;
		$descr =~ s/á/\&aacute;/;
		$descr =~ s/è/\&egrave;/;
		$descr =~ s/é/\&eacute;/;
		$descr =~ s/ì/\&igrave;/;
		$descr =~ s/í/\&iacute;/;
		$descr =~ s/ò/\&ograve;/;
		$descr =~ s/ó/\&oacute;/;
		$descr =~ s/ù/\&ugrave;/;
		$descr =~ s/ú/\&uacute;/;  
			
		# costruisco il frammento per il nodo prodotto
		my $prodotto = $docProd->createElement("prodotto");
		$prodotto->setAttribute("codice",$codice);
		
		#inserimento tag interni
		my $p = 0;
		my @info = ("nome","materiale","tipologia","categoria","prezzo","descrizione");
		my @valori = ($nome,$materiale,$tipo,$categ,$prezzo,$descr);
		foreach my $i(@info) { 
			$prodotto->appendChild($docProd->createElement($i));
			$prodotto->findnodes($i)->get_node(1)->appendText(@valori[$p++]); 
		}
		$prodotto->findnodes("prezzo")->get_node(1)->setAttribute("valuta",$valuta);
		$prodotto->findnodes("prezzo")->get_node(1)->setAttribute("sconto","0");
							
		# inserisco le taglie disponibili
		my $taglieDisp = $docProd->createElement("taglieDisponibili");
		for $taglia (@taglie){
			my $t = $docProd->createElement("taglia");
			$t->appendText($taglia);
			$taglieDisp->appendChild($t);
		}	
		$prodotto->appendChild($taglieDisp);
		
		# inserisco i colori disponibili
		my $coloriDisp = $docProd->createElement("coloriDisponibili");
		for $colore(@colori) {
			my $c = $docProd->createElement("colore");
			$c->appendText($colore);
			$coloriDisp->appendChild($c);
		}
		$prodotto->appendChild($coloriDisp);
				
		# inserisco le immagini del prodotto
		my $immaginiDisp = $docProd->createElement("immaginiProdotto");
		my $i = 0;
		while($i < 3){
			$immagine = param('immagine'.$i);
			if(defined $immagine) {
				#controllo se immagine già presente nella cartella prodotti
				if(!(-e "../../$public_path/images/prodotti/$immagine")){ 
					uploadImage("immagine".$i); #se no carico l'immagine selezionata
				}
				my $im = $docProd->createElement("immagine");
				$im->appendText($immagine);
				$immaginiDisp->appendChild($im);
			}
			$i++;
		}
		$prodotto->appendChild($immaginiDisp);
	
		#aggiungo il nodo
		my $nodo = $parserProd->parse_balanced_chunk($prodotto)
			|| die('frammento non ben formato');
		$padre->appendChild($prodotto);

		open(my $fo, '>', $fileProdXML) or die "Errore nell'apertura del file $fileProdXML ";
		print $fo $docProd->toString;
		close $fo;
		
		printPrettyXML($fileProdXML);
				
		return "success";
		
	}
	
	return $error_message;

}
