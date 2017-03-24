#!/usr/bin/perl -w

require "../header.cgi";
require "function/modProd.cgi";

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

#======= COSTRUZIONE PARSER ============
my $fileProdXML='../../data/prodotti.xml';
makeUserParser("../../data/utenti.xml");
makeProductParser($fileProdXML);
makeReviewParser("../../data/recensioni.xml");

#========= CREAZIONE VARIABILI DI SESSIONE ======
makeSession();

#============ DEFINIZIONE TIPOLOGIE E MATERIALI =========
getCategories();

#======= LETTURA VALORI GET =======

#ricava il contenuto del widget 'selProd'
my $codice= param('codice');

if($codice){

	# prelevo il valore del parametro submit per sapere 
	# se è stato effettuato il submit del form
	my $submit = param('submit');

	#======== RECUPERO VALORI ==========

	# recupero elenco prodotti
	my $query="//prodotto[\@codice='$codice']";
	my $prod = $docProd->findnodes($query)->get_node(1);

	my $nome = $prod->findvalue('nome');
	my $materiale = $prod->findvalue('materiale');
	my $prezzo = $prod->findvalue('prezzo');
	my $descr = $prod->findvalue('descrizione');
	my $categ = $prod->findvalue('categoria');
	my $tipo = $prod->findvalue('tipologia');

	my @listaTaglie=$prod->findnodes("taglieDisponibili/taglia/text()");
	my $numTaglie=@listaTaglie;
	my @listaColori=$prod->findnodes("coloriDisponibili/colore/text()");
	my $numColori=@listaColori;
	my @listaImmagini=$prod->findnodes("immaginiProdotto/immagine/text()");

	print "Content-type: text/html\n\n";

	#intestazione documento
	$keywords = "prodotto,modifica,valori,altera,$nome";
	my $html_string = getHTMLHeader("Modifica Prodotto",$keywords);

	#============= CORPO FORM MODIFICA PRODOTTO ==================

	$html_string .= " 
	<h2 class='ptitle'>Modifica prodotto</h2>";
			
	# Controlla se è stato fatto il submit del form
	# In questo caso effettuo l'inserimento (con i controlli)
	if ($submit){
		my $result = modProduct();
		#my @res = modProduct();
		#my $n = @res;
		if("$result" ne "success"){
		#if($n>0){
			#$html_string .= "Immagini ==> ".@res[0]." ".@res[1]." ".@res[2]." ".@res[3];
			$html_string .= "
			<p class='perorr_title'>Impossibile modificare il prodotto!</p>
			<ul class='perror_list'>
				$result; 
			</ul>";
		}
		else{
			$html_string .= "
			<p class='success_msg'>Modifica del prodotto avvenuta con successo!</p>
			<p class='success_link'><a href='selectProd.cgi?form=1' ".tabIndex()." >Modifica un altro prodotto</a></p>
			<p class='success_link'><a href='dashboard.cgi' ".tabIndex()." >Seleziona altra attivit&agrave;</a></p>";
			#footer e chiusura documento
			$html_string .= getFooter();

			#stampa del documento
			printPrettyHTML($html_string);
			$html_string .= "</body></html>";
			exit;
		}
	}

	$html_string .= "				
	<form id='formProduct' action='formModProd.cgi' method='post' enctype='multipart/form-data'>";
	# input per verificare che sia stato effettuato il submit del form
	$html_string .= "
		<p><input type='hidden' name='submit' value='Submit' /></p>
		<fieldset class='general_info'>
		<legend class='plegend'>Informazioni Prodotto</legend>
		<ul>
			<li class='frame_tipologia'>
				<label for='tipo'>Tipologia</label>
				<input type='text' id='tipo' name='tipo' class='pinputlock' value='$tipo' readonly='readonly' />
			</li>
			<li class='frame_codice'>
				<label for='codice'>Codice</label>
				<input type='text' id='codice' name='codice' class='pinputlock' value='$codice' readonly='readonly' />								
			</li>
			<li class='frame_nome'>
				<label for='nome'>Nome</label>
				<input type='text' id='nome' name='nome' class='pinput' value='$nome' ".tabIndex()." />
				<p id='messageNome' class='msgerror'></p>
			</li>
			<li class='frame_categoria'>
				<label for='categ'>Categoria</label>
				<select id='categ' class='pselect' name='categ' ".tabIndex()." >\n";
				for $categoria (@categorie){
					my $selected = ("$categ" eq "$categoria" ? "selected='selected'" : "");
					$html_string .= "<option value='$categoria' $selected>$categoria</option>";
				}
				$html_string .= "
				</select>
				<p id='messageCateg' class='msgerror'></p>
			</li>
			<li class='frame_materiale'>
				<label for='materiale'>Materiale</label>
				<select id='materiale' class='pselect' name='materiale' ".tabIndex()." >\n";
				for $mat (@materiali){
					my $selected = ("$materiale" eq "$mat" ? "selected='selected'" : "");
					$html_string .= "<option value='$mat' $selected>$mat</option>";
				}
				$html_string .= "	
				</select>
				<p id='messageMateriale' class='msgerror'></p>
			</li>
			<li class='frame_prezzo'>
				<label for='prezzo'>Prezzo</label>
				<input type='text' id='prezzo' name='prezzo' value='$prezzo' size='8' maxlength='8' ".tabIndex()." />
				<p id='messagePrezzo' class='msgerror'></p>
			</li>							
			<li class='frame_descrizione'>
				<label for='descr'>Descrizione</label>
				<textarea id='descr' name='descr' rows='5' cols='50' ".tabIndex()." >$descr</textarea>
				<p id='messageDescr' class='msgerror'></p>
			</li>														
		</ul>
	</fieldset>";

	#============= TAGLIE PRODOTTO ============
				
	$html_string .= "<fieldset class='sizes_info'>
		<legend class='plegend'>Lista Taglie Prodotto</legend>
		<ul id='taglieDisponibili'>";
		my $iTaglia=1;
		my @taglieS;
		my $class = "";
		if(grep{ $_ eq $tipo} @tipologie_scarpe) { 
			$class = "class = 'checkbox_number'";
			@taglieS = @taglieNum; 
		}
		else { @taglieS = @taglieChar; }
		
		if(grep{ $_ eq $tipo} @tipologie_uniche){
					
			$html_string .= "
			<li>
				<input type='checkbox' id='tagliaUnica' name='taglie' value='Unica' checked='checked' ".tabIndex()." />
				<label for='tagliaUnica'>Unica</label>
			</li>";
					
		}else {
		
			for $taglia (@taglieS){
				my $sel = (grep{ $_ eq $taglia} @listaTaglie) ? "checked='checked'" : "";
				$html_string .= "
				<li $class>
					<input type='checkbox' id='taglia$iTaglia' name='taglie' value='$taglia' $sel ".tabIndex()." />
					<label for='taglia$iTaglia'>$taglia</label>
				</li>";
				$iTaglia++;
			}#endFor
		
		}
		
		$html_string .= "	
		</ul>
		<p id='messageTaglie' class='msgerror'></p>
	</fieldset>";

	#============= COLORI PRODOTTO =================
				
	$html_string .= "<fieldset class='colors_info'>
		<legend class='plegend'>Lista Categorie Colori Prodotto</legend>
		<ul id='color_space'>";
		my $iColore=1;
		if (grep{ $_ eq $tipo} @tipologie_uniche){ 
			$html_string .= "
			<li id='unique_item'>
				<input type='checkbox' id='coloreUnico' name='colors' value='Unico' checked='checked' ".tabIndex()." />
				<label for='coloreUnico'>Unico</label>
			</li>";
		}else { 
			for $colore (@colori){
				my $sel = (grep{ $_ eq $colore} @listaColori) ? "checked='checked'" : "";
				$html_string .= "
				<li>
					<input type='checkbox' id='colore$iColore' name='colors' value='$colore' $sel ".tabIndex()." />
					<label for='colore$iColore'>$colore<span id='circle$colore' ".("$colore" eq "Unico" ? "" : "class='colorSpan'")."></span></label>
				</li>";
				$iColore++;
			}#endFor
		}#else
		$html_string .= "
		</ul>
		<p id='messageColori' class='msgerror'></p>
	</fieldset>";

	#============= IMMAGINI PRODOTTO ===============
			
	$html_string .= "<fieldset class='images_info'>
		<legend class='plegend'>Lista Immagini Prodotto</legend>
		<ul id='imm_space'>";
		my $numImmagini = 3;
		for (my $i = 0; $i < $numImmagini; $i++) {
			my $immagine = (@listaImmagini[$i] ?  @listaImmagini[$i]->getValue() : "");
			$html_string .= "
			<li id='itemImm$i'>
				<label for='immagine$i'>Immagine ".($i+1)."</label>";
				if($immagine) {
					$html_string .= "<img src='/$public_path/images/prodotti/$immagine' alt='Immagine ".($i+1)." $tipo $nome' />";
					$html_string .= "<input type='text' id='immagine$i' name='immagine$i' value='$immagine' readonly='readonly' />";
				}
				$html_string .= "
				<p><label for='new_image$i'>Immagine sostitutiva</label>
				<input type='file' id='new_image$i' name='new_image$i' ".tabIndex()." />
				<span>(niente se non si vuole modificare)</span></p>
				<p id='messageImmagine$i' class='msgerror'></p>
			</li>";
		}
		$html_string .= "
		</ul>
	</fieldset>".
	($result != 1 ? "\t<p class='submit_p'><input class='psubmit' type='submit' value='Modifica Prodotto' ".tabIndex()." /></p>" : "").
	"</form>".
	($errore ? "<p id='erroreFormPerl'>Errore nei dati inseriti<a id='topAnchor' href='#title' ".tabIndex()." >Torna su</a></p>" : "");

	$html_string .= "
	<script type='text/javascript' src='/$public_path/js/checks.js'></script>
	<script type='text/javascript' src='/$public_path/js/checkFormProd.js'></script>";

	#footer e chiusura documento
	$html_string .= getFooter();

	#stampa del documento
	printPrettyHTML($html_string);
}else{

	#redirect alla pagina di selezione prodotto da modificare
	my $query=new CGI;
	print $query->redirect('selectProd.cgi?form=1');
}
