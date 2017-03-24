#!/usr/bin/perl -w

require "../header.cgi";

use Time::Piece;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

sub addRec{
	
	#======= COSTRUZIONE PARSER ============
	#creazione parser utenti
	my $fileRevXML = "../../data/recensioni.xml";
	makeReviewParser($fileRevXML);
	
	#recupero dati form
	my $star = param('rating-input-1');
	my $text = param('textcomment');
	my $codice = param('codice');
	my $author = param('author');
	my $curr_date = localtime->ymd('-');

	#=================== CONTROLLO CAMPI ================
	my $errore=false;
	my $message="";

	if("$text" eq ""){
		$errore = true;
		$message .= "<li><p class='msgerror'>Il testo della recensione deve contenere almeno 10 caratteri.</p></li>";
	}
	if("$star" eq ""){
		$errore = true;
		$message .= "<li><p class='msgerror'>Valutazione prodotto non selezionata!</p></li>";
	}
    if($errore eq true){
		return $message;
	}
	else{
		
		#============ INSERIMENTO RECENSIONE ==============
		
		#cerco il nodo a cui inserire un figlio
		my $padre = $docRec->findnodes("//so:recensioni")->get_node(1);
		
		#costruisco il frammento per il nodo recensione
		my $recensione = $docRec->createElement("rec");
		$recensione->setAttribute("autore",$author);
		$recensione->setAttribute("codice",$codice);
		
		#inserimento tag interni
		my $r = 0;
		my @info = ("data","descrizione","punteggio");
		my @value = ($curr_date,$text,$star);
		foreach my $i(@info) { 
			$recensione->appendChild($docRec->createElement($i));
			$recensione->findnodes($i)->get_node(1)->appendText(@value[$r++]); 
		} 
				
		#aggiungo il nodo
		my $nodo = $parserRec->parse_balanced_chunk($recensione)
			|| die('frammento non ben formato');
		$padre->appendChild($recensione);
			
		open(my $fo, '>', $fileRevXML) or die "Errore nell'apertura del file ".$fileRevXML." ";
		print $fo $docRec->toString;
		close $fo;
		
		printPrettyXML($fileRevXML);
		
		return 1;
		
	}
}

1;
