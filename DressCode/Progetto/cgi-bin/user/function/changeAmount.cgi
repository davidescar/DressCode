#!/usr/bin/perl -w

require "../../header.cgi";

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

#========= CREAZIONE VARIABILI DI SESSIONE ======
makeSession();
my $numProd = $session->param("numProd");

my $numero = param("numero");
my $operation = param("op");

print "Content-type: text/html\n\n";

if("$operation" eq "Add") {

	my $newValue = $session->param("qnt".$numero) + 1; #prelievo qnt attuale aggiungo nuovo elemento
	$session->param("qnt".$numero, $newValue); #salvo nuovo valore nella variabile di sessione associata al prodotto

}else {
	
	if("$operation" eq "Rmv") {
			
		my $newValue = $session->param("qnt".$numero) - 1; #prelievo qnt attuale rimuovo un elemento
		
		if($newValue < 1) { #se qnt < 1 devo rimuovere prodotto dal carrello
			
			#ciclo per shift degl'altri prodotto dovuta alla rimozione del prodotto selezionato
			for(my $i = $numero; $i < $numProd; $i++) {
				
				my @next = @{$session->param("prod".($i+1))}; #elemento in var di sessione successiva a prod da eliminare
				my $nNext = $session->param("qnt".($i+1)); #qnt di questo elemento
				$session->param("prod".$i,\@next); #shift del prodotto i+1 a i
				$session->param("qnt".$i,$nNext);
				
			}
		
			$session->param("numProd",$numProd - 1); #scalo dimensione numero prodotti nel carrello
			
		}else {
			
			$session->param("qnt".$numero,$newValue); #se qnt ancora > 1 semplicemente rimuovo un elemento
		
		}
	
	}
	
}


print "<meta http-equiv='refresh' content='0; url=../carrello.cgi' />";
