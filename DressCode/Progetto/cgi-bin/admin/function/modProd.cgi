#!/usr/bin/perl -w

require "../header.cgi";
require "function/utility.cgi";

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

sub modProduct{

	#======= COSTRUZIONE PARSER ============
	# imposto il path del file dati
	my $fileProdXML='../../data/prodotti.xml';
	makeProductParser($fileProdXML,"../../data/recensioni.xml");
	
	#============= LETTURA VALORI POST =============
	
	my $codice = param('codice');
	my $nome = param('nome');
	my $materiale = param('materiale');
	my $prezzo = param('prezzo');
	my $descr = param('descr');
	my $categ = param('categ');
	my $tipo = param('tipo');
	my @taglie = param('taglie');	
	my @colori = param('colors');
	
	#Prelievo immagini
	my @images;
	
	for (my $i=0; $i < 3; $i++){
		my $new = param("new_image".$i);
		my $old = param("immagine".$i);
		if("$new" eq ""){ #non ho selezionato una nuova immagine per il prodotto => mantengo quella che c'era
			@images[$i] = $old;
		}else{ #prelevo nuova immagine prodotto
			@images[$i] = $new;	
		}
	}
	
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
	
	my @tags = ("nome","materiale","tipologia","categoria","prezzo","descrizione");
	my @new_values = ($nome,$materiale,$tipo,$categ,$prezzo,$descr);
	
	#=================== CONTROLLO CAMPI ================
	my $error_message = "";

	#controllo campi vuoti
	for(my $i = 0; $i < 6; $i++) { $error_message .= isEmpty(@new_values[$i],@tags[$i]); }

	#controllo prezzo
	$error_message .= isValidPrice($prezzo);

	#controllo taglie
	$error_message .= ( @taglie < 1 ? "<li>Nessuna taglia selezionata.</li>" : "");

	#controllo colori
	$error_message .= ( @colori < 1 ? "<li>Nessuna categoria di colore selezionata.</li>" : "");
	
	if(!length $error_message){
		
		#============ MODIFICA PRODOTTO ==============
			
		# recupero elemento radice
		my $root = $docProd->getDocumentElement;
		
		#controllo e modifica info principali prodotto
		my $new_value_index = 0;
		
		for my $tag(@tags) {
			
			my $node = $root->findnodes("//prodotto[\@codice='$codice']/$tag")->get_node(1);
			my $value = $node->textContent();
			my $new_value = @new_values[$new_value_index++];
			
			if("$value" ne "$new_value") {
				$node->removeChildNodes();
				$node->appendText($new_value);
			}
			
		}
				
		#modifica taglie
		
		my $t_node = $root->findnodes("//prodotto[\@codice='$codice']/taglieDisponibili")->get_node(1);
		$t_node->removeChildNodes();
		
		for $taglia(@taglie) {
			my $new_t = $docProd->createElement("taglia");
			$new_t->appendText($taglia);
			$t_node->appendChild($new_t);
		}
		
		#modifica colori
		
		my $c_node = $root->findnodes("//prodotto[\@codice='$codice']/coloriDisponibili")->get_node(1);
		$c_node->removeChildNodes();
		
		for $colore(@colori) {
			my $new_c = $docProd->createElement("colore");
			$new_c->appendText($colore);
			$c_node->appendChild($new_c);
		}
		
		#modifica immagini
		
		my $i_node = $root->findnodes("//prodotto[\@codice='$codice']/immaginiProdotto")->get_node(1);
		$i_node->removeChildNodes();
		
		
		my $numImm = 3;
		for(my $i = 0; $i < $numImm; $i++) {
			my $immagine = @images[$i];
			if(!(-e "../../public_html/images/prodotti/$immagine")){ 
				uploadImage("new_image".$i); #se no carico l'immagine selezionata
			}
			my $new_i = $docProd->createElement("immagine");
			$new_i->appendText($immagine);
			$i_node->appendChild($new_i);
		}

		open(my $fo, '>', $fileProdXML) or die "Errore nell'apertura del file ".$fileProdXML." ";
		print $fo $docProd->toString;
		close $fo;
		
		printPrettyXML($fileProdXML);
						
		return "success";
		
	}
	
	return $error_message;

}

1
