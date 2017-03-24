#!/usr/bin/perl -w

require "../header.cgi";

#====== LETTURA VARIBILI FILTRO =======
sub bindsReader {
	
	$tipo=param('tipo');
	$prom=param('prom');
	$lInf=param('lInf');
	$lSup=param('lSup');
	
	$cat=param('cat');
	@mat=param('mat[]');
	$nmat=@mat; #numero materiali selezionati
	@tipol=param('tipol[]');
	$ntip=@tipol; #numero tipologie selezionate
	@colr=param('colr[]');
	$ncol=@colr; #numero colori selezionati
	$fprezzo=param('fasciaprezzo');
	
	return;
}

#========= STAMPA FILTRI ===========
sub filtersPrinting {
	
	my $html_string = "
	<h3 id='activate_fil'>Filtri</h3>
	
	<form id='filtersList' action='prodList.cgi' method='get'>
		<ul>
			<!-- filtri attivi (tipologia e promozione) -->
			
			".( defined $tipo ? "<li><input type='hidden' name='tipo' value='$tipo' /></li>" : "")."
			".("$prom" eq "yes" ? "<li><input type='hidden' name='prom' value='$prom' /></li>" : "")."
	
			<!-- filtri materiali -->
			<li>
				<span id='displaymat' class='filterClosed'>Materiale</span>
				<ul id='togglemat'>";
				for $m(@materiali) {
					$html_string .= "
					<li><input type='checkbox' name='mat[]' value='$m' ".					
						("@mat" =~ /\b$m\b/ ? "checked='checked' " : "")."/>$m</li>";			
				}
				$html_string .= "
				</ul>
			</li>
		
			<!-- filtri tipologia -->
			<li>
				<span id='displaytip' class='filterClosed'>Tipologia</span>
				<ul id='toggletip'>";
				for $tl("$tipo" eq "Donna" ? @tipologie_totali : @tipologie_uomo) {
					$html_string .= "
					<li><input type='checkbox' name='tipol[]' value='$tl' ".					
						("@tipol" =~ /\b$tl\b/ ? "checked='checked' " : "")."/>$tl</li>";						
				}
				$html_string .= "
				</ul>
			</li>
		
			<!-- filtri colore -->
			<li>
				<span id='displaycol' class='filterClosed'>Colore</span>
				<ul id='togglecol'>";
				for $c(@colori){
					$html_string .= "
					<li><input type='checkbox' name='colr[]' value='$c'".					
						("@colr" =~ /\b$c\b/ ? "checked='checked' " : "").
							"/>$c<span id='circle$c'></span></li>";					
				}
				$html_string .= "
				</ul>
			</li>
		
			<!-- filtri prezzo -->
			<li>
				<span id='displayprice' class='filterClosed'>Prezzo</span>
				<ul id='toggleprice'>";
				for($i=1; $i<=$dimPr; $i++){
					$html_string .= "
					<li><input type='radio' name='fasciaprezzo' value='$i'".
						($fprezzo && $i==$fprezzo ? "checked='checked' " : "")." />".@prezzi[$i-1]."</li>";
				}
				$html_string .= "
				</ul>
			</li>
			
		</ul>
		<p><input type='submit' class='psubmit' value='Applica Filtri' /></p>
	
	</form>";
		
	return $html_string;
		
}

#========== CALCOLO QUERY FILTRI ======
sub filtersQuery {
		
		my $query = ""; #query ricerca nodi con caratteristiche scelte
		
		#lista completa prodotti
		if(!$prom && !$tipo){
			$query .= "//prodotto[\@codice!=''";
		}
		
		else{		
			#ricerca per prodotti in promozione
			if($prom) {
			  $query .= "//prodotto[prezzo/attribute::sconto > 0";
			}else{ #o per tipologie Uomo,Donna,Bambino
			  $query .= "//prodotto[categoria/text()='$tipo'";
			}
		}
		
		#imposto variabili min max se var fprezzo presente
		if($fprezzo ne ""){
			$min; $max;
			if($fprezzo==1){
				$min=0; $max=20.00;
			}
			if($fprezzo==2){
				$min=20.01;	$max=50.00;
			}
			if($fprezzo==3){
				$min=50.01;	$max=100.00;
			}
			if($fprezzo==4){
				$min=100.01; $max=10000.00;
			}
		}		
		
		#vincoli di materiale se selezionati
		for($i=0; $i<$nmat; $i++){
			(!$i) ? ($query.=" and (") : (""); # aggiungo condizione and alla query			
			$query.="materiale/text()='@mat[$i]' "; #inserisco il materiale 
			($i+1<$nmat) ? ($query.="or ") : ($query.=")"); # se selezionati più materiali aggiungo or			
		}
		#vincoli di tipologia vestiario
		for($i=0; $i<$ntip; $i++){
			(!$i) ? ($query.=" and (") : ("");
			$query.="tipologia/text()='@tipol[$i]' ";
			($i+1<$ntip) ? ($query.="or ") : ($query.=")");
		}
		#vincoli di colore
		for($i=0; $i<$ncol; $i++){
			(!$i) ? ($query.=" and (") : ("");
			$query.="coloriDisponibili/colore/text()='@colr[$i]' ";
			($i+1<$ncol) ? ($query.="or ") : ($query.=")");			
		}
		#vincoli di prezzo
		$query .= ($fprezzo ne "") ? " and (prezzo/text()>'$min' and prezzo/text()<'$max')" : "";
		$query .= "]"; #chiusura query
				
		return $query;

}

#============== CALCOLO LIMITI VISUALIZZAZIONE ==========
sub limitsPrint {
	
	my $html_string;
		
	my $limI = $_[0]; #limite inferiore attuale
	my $limS = $_[1]; #limite superiore attuale
	my $numP = $_[2]; #numero di prodotti derivanti dalla query
		
	$html_string .= "<p class='limitString'>Prodotti da ".(!$limI ? 1 : $limI+1)." a "
		.($limS<$numP ? $limS : $numP)." visualizzati su $numP totali ";
	
	if(!$limI){ #se limI 0 allora stampo solo link per limite superiore
		if($limS < $numP) { #se limite superiore supera numero di prodotti non stampo nulla, altrimenti stampo link visualizzazione prossimi 9 prodotti
			
			my $query = $ENV{QUERY_STRING}; #controllo se la query string ha già i limiti presenti
			my $check = index($query,"lInf");
			if($check == -1){
				$html_string .= "<a class='pnext' href='prodList.cgi?$ENV{QUERY_STRING}&amp;lInf=9&amp;lSup=18' ".tabIndex().">Prossimi</a></p>";
			}else{
				$query =~ s/&/&amp;/g;
				$query =~ s/lInf=0/lInf=9/g;
				$query =~ s/lSup=9/lSup=18/g;
				$html_string .= "<a class='pnext' href='prodList.cgi?$query' ".tabIndex().">Prossimi</a></p>";
			}
		}else {
			$html_string .= "</p>";
		}
	}else{
	
		#se limI già presente allora variabili limite già presenti nella query string HTTP
		#creo due variabili per visualizzare prodotti precedenti e successivi ai 9 attuali
		my $queryprev = $ENV{QUERY_STRING};
		my $querypost = $ENV{QUERY_STRING};
		#creazione query string per ritorno a 9 elementi precedenti
		$queryprev =~ s/&/&amp;/g;
		replace($queryprev,"lInf=$limI","lInf=".($limI-9));
		replace($queryprev,"lSup=$limS","lSup=$limI");
		$html_string .= "<a class='pprev' href='prodList.cgi?$queryprev' ".tabIndex().">Precedenti</a>";
		#se limS < numP allora creo stringa per 9 elementi superiori
		if($limS < $numP) {
			$querypost =~ s/&/&amp;/g;
			replace($querypost,"lInf=$limI","lInf=$limS");
			replace($querypost,"lSup=$limS","lSup=".($limS+9));
			$html_string .= "<a class='pnext' href='prodList.cgi?$querypost' ".tabIndex().">Prossimi</a><p>";
		}else{
			$html_string .= "</p>";
		}
	
	}
	
	return $html_string;
	
}

1;
