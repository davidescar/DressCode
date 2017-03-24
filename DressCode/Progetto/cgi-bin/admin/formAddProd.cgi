#!/usr/bin/perl -w

require "../header.cgi";
require "function/addProd.cgi";

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

#======= COSTRUZIONE PARSER ============
makeUserParser("../../data/utenti.xml");

#========= CREAZIONE VARIABILI DI SESSIONE ======
makeSession();

#============ DEFINIZIONE TIPOLOGIE E MATERIALI =========
getCategories();

# Prelevo tipologia selezionata precedentemente
my $tipo = param('tipo');

if($tipo){

	# prelevo il valore del parametro submit per sapere 
	# se è stato effettuato il submit del form
	my $submit = param('submit');

	print "Content-type: text/html\n\n";

	#intestazione documento
	$keywords = "inserimento,aggiunta,nuovo";
	my $html_string = getHTMLHeader("Aggiunta Prodotto",$keywords);

	$html_string .= "<h2 class='ptitle'>Inserimento Nuovo Prodotto</h2>";
			
	#=========== CORPO FORM INSERIMENTO PRODOTTO ==========			
				
	# Controlla se è stato fatto il submit del form
	# In questo caso effettuo l'inserimento (con i controlli)
	if ($submit){
		my $result = addProduct();
		if("$result" ne "success"){
			$html_string .= " 
			<p class='perorr_title'>Impossibile inserire il prodotto!</p>
			<ul class='perror_list'>";
			$html_string .= $result; 
			$html_string .= "</ul>";
		}
		else{ 
			$html_string .= "
			<p class='success_msg'>Inserimento prodotto avvenuto con successo!</p>
			<p class='success_link'><a href='selectProd.cgi?form=0' ".tabIndex().">Inserisci un nuovo prodotto</a></p>
			<p class='success_link'><a href='dashboard.cgi' ".tabIndex()." >Seleziona altra attivit&agrave;</a></p>";
			#footer e chiusura documento
			$html_string .= getFooter();
			#stampa del documento
			printPrettyHTML($html_string);
			exit;
		}
	}

	#=========== FORM INSERIMENTO PER TIPOLOGIA SCELTA ============	
				
	# Controllo validità tipologia scelta
				
	if(!(grep{ $_ eq $tipo} @tipologie_totali)){
		#redirect alla selezione della tipologia del prodotto
		print "redirect";
	}
	else{

		$html_string .= "
		<form id='formProduct' action='formAddProd.cgi' method='post' enctype='multipart/form-data' >";
		
		#========= INFO GENERALI ==========
		$html_string .= "
			<p><input type='hidden' name='submit' value='Submit' /></p>
			<fieldset class='general_info'>
				<legend class='plegend'>Informazioni sul prodotto</legend>
				<ul>

					<li class='frame_tipologia'>
						<label for='tipo'>Tipologia</label>
						<input type='text' id='tipo' name='tipo' class='pinputlock' value='$tipo' readonly='readonly' />
						<p id='messageTipo' class='msgerror'></p>
					</li>
		
					<li class='frame_nome'>
						<label for='nome'>Nome</label>
						<input type='text' id='nome' name='nome' class='pinput' value='".param("nome")."' ".tabIndex()."/>
						<p id='messageNome' class='msgerror'></p>
					</li>
		
					<li class='frame_categoria'>
						<label for='categ'>Categoria</label>
						<select id='categ' name='categ' class='pselect' ".tabIndex().">";
						for $categoria (@categorie){
							my $categ = param('categ');
							my $sel = "$categoria" eq "$categ" ? $sel="selected='selected'" : "";
							$html_string .= "<option value='$categoria' $sel>$categoria</option>";
						}	
						$html_string .= "
						</select>
						<p id='messageCateg' class='msgerror'></p>
					</li>
		
					<li class='frame_materiale'>
						<label for='materiale'>Materiale</label>
						<select id='materiale' name='materiale' class='pselect' ".tabIndex().">";
						for $mat (@materiali){
							my $matateriale = param("materiale");
							my $sel = "$materiale" eq "$mat" ? $sel="selected='selected'" : "";
							$html_string .= "<option value='$mat' $sel>$mat</option>";
						}
						$html_string .= "
						</select>
						<p id='messageMateriale' class='msgerror'></p>
					</li>
		
					<li class='frame_prezzo'>
						<label for='prezzo'>Prezzo</label>
						<input type='text' id='prezzo' name='prezzo' value='".param("prezzo")."' size='6' maxlength='6'/ ".tabIndex().">
						<p id='messagePrezzo' class='msgerror'></p>
					</li>	
					
					<li class='frame_descrizione'>
						<label for='descr'>Descrizione</label>
						<textarea id='descr' name='descr' rows='3' cols='50' ".tabIndex().">".param("descr")."</textarea>
						<p id='messageDescr' class='msgerror'></p>
					</li>		
		
				</ul>
			</fieldset>";
					
			#============= TAGLIE PRODOTTO ============				
			
			$html_string .= "
			<fieldset class='sizes_info'>
				<legend class='plegend'>Seleziona Taglie</legend>
				<ul id='taglieDisponibili'>";
			
				my $iTaglia=1;
				my @taglieS;
				my @taglie = param('taglie');
				my $class = "";
			
				if(grep{ $_ eq $tipo} @tipologie_scarpe) { 
					$class = "class = 'checkbox_number'";
					@taglieS = @taglieNum; 
				}
				else { @taglieS = @taglieChar; }
			
				if(grep{ $_ eq $tipo} @tipologie_uniche){
					
					$html_string .= "
					<li>
						<input type='checkbox' id='tagliaUnica' name='taglie' value='Unica' checked='checked' / ".tabIndex().">
						<label for='tagliaUnica'>Unica</label>
					</li>";
					
				}else {
				
					for $taglia (@taglieS){
						my $sel = (grep{ $_ eq $taglia} @taglie) ? "checked='checked'" : "";
						$html_string .= "
						<li $class>
							<input type='checkbox' id='taglia$iTaglia' name='taglie' value='$taglia' $sel ".tabIndex()." />
							<label for='taglia$iTaglia'>$taglia</label>
						</li>";
						$iTaglia++;
					}#endFor
				
				}#else
				
				$html_string .= "
				</ul>
				<p id='messageTaglie' class='msgerror'></p>
			</fieldset>";
					
			#============= COLORI PRODOTTO =================
									
			@colori ? $numColori = @colori : $numColori=1; 		
			$html_string .= "
			<fieldset class='colors_info'>
				<legend class='plegend'>Seleziona Categorie Colori</legend>
				<ul id='color_space'>";
			
				my $iColore=1;
				my @colors = param('colors');
				if (grep{ $_ eq $tipo} @tipologie_uniche){ 
					$html_string .= "
					<li id='unique_item'>
						<input type='checkbox' id='coloreUnico' name='colors' value='Unico' checked='checked' ".tabIndex()." />
						<label for='coloreUnico'>Unico</label>
					</li>";
				}else { 
					for $colore (@colori){
						my $sel = (grep{ $_ eq $colore} @colors) ? "checked='checked'" : "";
						$html_string .= "
						<li>
							<input type='checkbox' id='colore$iColore' name='colors' value='$colore' $sel ".tabIndex()." />
							<label for='colore$iColore'>$colore</label><span id='circle$colore' class='colorSpan'></span>
						</li>";
						$iColore++;
					}#endFor
				}
				
				$html_string .= "
				</ul>
				<p id='messageColori' class='msgerror'></p>
			</fieldset>";
					
			#============= IMMAGINI PRODOTTO ===============
			
			#ripristino valori form immagini	
			my @listaImmagini;
			for(my $i = 0; $i < 3; $i++) { push(@listaImmagini,param("immagine".$i));}
			
			$html_string .= "
			<fieldset class='images_info'>
				<legend class='plegend'>Lista Immagini Prodotto</legend>
				<ul id='imm_space'>"; 
			
				for (my $i = 0; $i < 3; $i++) {
					my $immagine = (@listaImmagini[$i] ?  @listaImmagini[$i] : "");
					$html_string .= "
					<li id='itemImm$i'>
						<label for='immagine$i'>Immagine ".($i+1)."</label>";		
						if($immagine) {
							$html_string .= "<input type='text' id='immagine$i' name='immagine$i' class='pinputlock' value='$immagine' readonly='readonly'/>";
						}else{
							$html_string .= "<input type='file' id='immagine$i' name='immagine$i' ".tabIndex()." />";
						}		
						$html_string .= "
						<p id='messageImmagine$i' class='msgerror'></p>
					</li>";
				}
				$html_string .= "
				</ul>
			</fieldset>".

			($result != 1 ? "<p class='submit_p'><input class='psubmit' type='submit' value='Inserisci Prodotto' ".tabIndex()." /></p>" : "")."
		</form>".
		($errore ? "<p id='erroreFormPerl'>Errore nei dati inseriti<a href='#breadcrumb' ".tabIndex()." >Torna su &#9650;</a></p>" : "");
			
	}#endElse

	$html_string .= "
	<script type='text/javascript' src='/$public_path/js/checks.js'></script>
	<script type='text/javascript' src='/$public_path/js/checkFormProd.js'></script>";

	#footer e chiusura documento
	$html_string .= getFooter();

	#stampa del documento
	printPrettyHTML($html_string);

}else{

	#redirect alla pagina di selezione tipologia prodotto da inserire
	my $query=new CGI;
	print $query->redirect('selectProd.cgi?form=0');
}
