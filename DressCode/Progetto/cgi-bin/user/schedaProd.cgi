#!/usr/bin/perl -w

require "../header.cgi";
require "function/addRec.cgi";

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

#======= PARAMETRI PER FORM RECENSIONI ============

# prelevo il valore del parametro checkInsRec per sapere 
# se è stato effettuato il submit del form delle recensioni utente
my $checkInsRec = param('checkInsRec');

# Controlla se è stato fatto il submit del form dei commenti degli utenti
# In questo caso effettuo l'inserimento (con i controlli)
if ($checkInsRec){ 
	$resultInsRec = addRec();
	$brd = param('breadcrumbs');
}

#======= COSTRUZIONE PARSER ============
makeUserParser("../../data/utenti.xml");
makeProductParser("../../data/prodotti.xml");
makeReviewParser("../../data/recensioni.xml");

#========= CREAZIONE VARIABILI DI SESSIONE ======
makeSession();

#======= PRELIEVO INFO PRODOTTO ========
my $code = param('codice');
my $checkCart = param('e');
my $checkProm = param('err_prom');

my $name = $docProd->findvalue("//prodotto[attribute::codice='$code']/nome");
my $price = $docProd->findvalue("//prodotto[attribute::codice='$code']/prezzo");
my $sconto = $docProd->findvalue("//prodotto[attribute::codice='$code']/prezzo/attribute::sconto");
my $descr = $docProd->findvalue("//prodotto[attribute::codice='$code']/descrizione");
my $material = $docProd->findvalue("//prodotto[attribute::codice='$code']/materiale");
my $type = $docProd->findvalue("//prodotto[attribute::codice='$code']/tipologia");
my $category = $docProd->findvalue("//prodotto[attribute::codice='$code']/categoria");
my @sizes = $docProd->findnodes("//prodotto[attribute::codice='$code']/taglieDisponibili/taglia/text()");
my @colors = $docProd->findnodes("//prodotto[attribute::codice='$code']/coloriDisponibili/colore/text()");
my @images = $docProd->findnodes("//prodotto[attribute::codice='$code']/immaginiProdotto/immagine/text()");

print "Content-type: text/html\n\n";

#intestazione documento
$keywords = "scheda,prodotto,informazione,dettaglio,caratteristiche,".$name.",".lc(join(", ", @colors));
my $html_string = getHTMLHeader("Scheda Prodotto",$keywords);
		
# ============= CORPO SCHEDA ================

$html_string .= "
<h2 class='ptitle'>Scheda Prodotto</h2>".

(("$admin" ne "admin") ? "<form action='function/addCart.cgi' method='get'>" : "")."
<ul id='info_list'>
		
	<li id='info_code'>
		<span>Codice prodotto: $code</span>
		<input type='hidden' id='codice' name='codice' value='$code' />
	</li>
		
	<li id='info_title'><span class='hid'>Nome: </span>$name ".($sconto ? "<span id='imgsale'></span>":"")."</li>";

	$html_string .= "
	<li id='info_price'>
		<span class='hid'>Prezzo: </span>";
		if($sconto){
			my $priceScont = $price-(($price*$sconto)/100);
			$priceScont = sprintf("%.2f",$priceScont);
			$priceScont =~ s/\./,/;     # rimpiazza il punto con la virgola
			$price =~ s/\./,/;     # rimpiazza il punto con la virgola
			$html_string .= "<span class='sales'>$price &euro; </span>"; #prezzo di listino
			$html_string .= "<span class='hid'> in sconto a: </span>$priceScont &euro; "; #prezzo scontato
			$html_string .= "<span id='info_disc'>Risparmi il $sconto%</span>"; #sconto effettuato
		}else{
			$price =~ s/\./,/;     # rimpiazza il punto con la virgola
			$html_string .= "$price &euro;";
		}
	$html_string .= "
	</li>";
		
	#operazioni amministratore
	if("$admin" eq "admin"){
			
		$html_string .= 
		(("$checkProm" eq "1") ? "<p class='msgerror'>Percentuale di sconto non valida!</p>" : "")."
		
		<li id='info_operations'>
			<p>Operazioni Amministratore</p>
			<ul>";
			if(!$sconto){ #se prodotto non in sconto
				$html_string .=	"<li class='prom_on'>".formSetPromo($code,7)."</li>";								
			}else{
				$html_string .= "<li class='prom_off'><a href='../admin/function/setPromoProd.cgi?codice=$code&amp;promo=rimuovi'>Togli Promozione</a></li>";
			}
			$html_string .= "
				<li class='modify'><a href='../admin/formModProd.cgi?codice=$code' ".tabIndex().">Modifica Prodotto</a></li>
				<li class='delete'><a href='../admin/function/deleteProd.cgi?selProd=$code' ".tabIndex().">Elimina Prodotto</a></li>
			</ul>
		</li>";
		
	}else{
	
		if("$checkCart" eq "1"){
			$html_string .= "<li><p class='msgerror'>Effettua il <a href='login.cgi' ".tabIndex().">LOGIN</a> per aggiungere al carrello i prodotti che ti interessano e poter procedere agli acquisti!</p></li>";
		}else{
			$html_string .= "<li id='info_cart'><input type='submit' class='psubmit' value='Aggiungi al carrello' / ".tabIndex()."></li>";
		}# else checkCart
	
	}#else if admin

	$html_string .= "
	<li id='info_det'>
		<span>Dettagli</span>
		<ul id='det_list'>";

		my $n=@sizes;
		if($n>0){
			#taglie disponibili
			$html_string .= "
			<li>				
				<label for='staglia'>Taglie</label>
				<select id='staglia' name='taglia' class='pselect' ".tabIndex().">";
				for ($i=0; $i<$n; $i++){
					my $s = @sizes[$i]->getValue();
					$html_string .= "<option value='$s'>$s</option>";
				}
				$html_string .= "
				</select>
			</li>";
		}#if n>0 taglie

		my $n=@colors;
		if($n>0){
			#colori disponibili
			$html_string .= "
			<li>
				<label for='scolore'>Colori</label>
				<select id='scolore' name='colore' class='pselect' ".tabIndex().">";
				for ($i=0; $i<$n; $i++){
					my $c = @colors[$i]->getValue();
					$html_string .= "<option value='$c'>$c</option>";
				}
				$html_string .= "
				</select>
			</li>";
		}#if n>0 colori

		#materiale e descrizione prodotto
		$html_string .= "
			<li id='det_mat'><span>Materiale</span> $material</li>
			<li id='det_descr'><span>Descrizione</span> <p class='italic'>$descr</p></li>
		</ul>

	</li>
</ul>".
(("$admin" ne "admin") ? "</form>" : "")."


<!-- immagini -->
<h3 id='images_title'>Immagini Prodotto</h3>
<ul id='images_list'>";
my $n = @images;
my $img = @images[0]->getValue();
$html_string .= "<li id='b_image'><img id='bigImg' src='/$public_path/images/prodotti/$img' alt='$name immagine'/></li>";
for(my $i=1; $i<$n; $i++){
	$img = @images[$i]->getValue();
	$html_string .= "<li class='s_images'><img id='smallImg$i' src='/$public_path/images/prodotti/$img' alt='$name immagine'/></li>";
}
$html_string .= "</ul>
	<p id='notaClickImm'>Nota: clicca su una delle due immagini pi&ugrave; piccole per ingrandirla.</p>";


# ============= RECENSIONI UTENTI ================

$html_string .= "
<h3 id='com_title'><span></span>Recensioni degli utenti</h3>		
				
<ul id='com_list'>";

my @allComments = $docRec->findnodes("//rec[attribute::codice=$code]");
my $allComments = @allComments;
if(!$allComments){
	$html_string .= "
		<li id='no_review'>Non ci sono recensioni!</li>
	</ul>";
	# Stampa form per inserimento recensione
	$html_string .= formRec(0);
}else{							
	for my $commento(@allComments){
		my $author = $commento->findvalue("attribute::autore");
		my $data = $commento->findvalue('data');
		my @d = split('-',$data);
		$data = @d[2]."-".@d[1]."-".@d[0];
		my $testo = $commento->findvalue('descrizione');
		my $punt = $commento->findvalue('punteggio');
		$html_string .= "
		<li>
			<dl>
			
				<dt>Autore</dt>
				<dd class='author'>$author</dd>
				
				<dt>Data</dt>
				<dd class='date'>$data</dd>";
				
				if("$admin" eq "admin") {
					$html_string .="
					<dt>Opzione Amministratore</dt>
					<dd class='admin_option'><a href='../admin/function/deleteRec.cgi?selUser=$author&amp;selProd=$code'>Elimina Recensione</a></dd>";
				}
				
				$html_string .= "
				<dt>Valutazione</dt>
				<dd class='val'>
				<span class='hid'>$punt</span>";
				for($i=0; $i<$punt; $i++){
					$html_string .= "<span class='star'></span>";
				}
				$html_string .= "
				</dd>	
									
				<dt>Descrizione</dt>
				<dd class='comment'>$testo</dd>
			
			</dl>
		</li>";
	}#for
	$html_string .= "</ul>";	
	# Stampa form per inserimento recensione
	$html_string .= formRec(1);		
}#else

#footer e chiusura documento
$html_string .= "
<script type='text/javascript' src='/$public_path/js/switchImages.js'></script>
<script type='text/javascript' src='/$public_path/js/checkFormComm.js'></script>";
$html_string .= getFooter();

#stampa del documento
printPrettyHTML($html_string);


sub formRec{
	
	my $html_string;
	my $tipMess = $_[0];
	my @authorRec = $docRec->findnodes("//rec[attribute::autore='$email' and attribute::codice='$code']");
	my $allMyRec = @authorRec;
	if(!$session->is_empty && "$admin" eq "user" && !$allMyRec){					
		
		$html_string .= "
		<form id='form_rec' action='schedaProd.cgi' method='post' >

			<fieldset>
			
				<input type='hidden' name='checkInsRec' value='Inserisci Recensione' />
				<input type='hidden' name='breadcrumbs' value='$brd' />";
		
				if(!$tipMess){ $html_string .= "<p>Inserisci la prima recensione per questo prodotto!</p>"; }
				else{ $html_string .= "<p>Inserisci una recensione del prodotto anche tu!</p>"; }
		
				#textarea testo recensione			
				$html_string .= "
				<label for='textcomment' id='inp_comm'><span class='hid'>Scrivi la tua recensione</span></label>								
				<textarea rows='10' cols='80' id='textcomment' name='textcomment'></textarea>
				<p id='messageTextComm'></p>
		
				<!-- sistema valutazione prodotto -->
				<span class='hid'>Valutazione Prodotto</span>
				<span class='rating'>";
				my $rating_value = 5;
				while($rating_value>0){ 
					$html_string .= "
					<input type='radio' class='rating-input' id='rating-input-1-$rating_value' name='rating-input-1' value='$rating_value' />
					<label class='rating-star' for='rating-input-1-$rating_value'></label>";
					$rating_value--;
				}
				$html_string .= "
				</span>
				<p id='messageStarComm'></p>	
						
				<input type='submit' class='psubmit' id='subRec' value='Inserisci recensione'/>
				
				<input type='hidden' name='codice' value='$code' />
				<input type='hidden' name='author' value='$email' />
			
		</fieldset>";
			
		if("$admin" eq "user"){
			if ($checkInsRec){
				if($resultInsRec!=1){
					$html_string .= "
					<p>Impossibile inserire la recensione!</p>
					<ul>".$resultInsRec."</ul>";
				}
			}
		}
		
		$html_string .= "</form>";
			
	}#if
	
	return $html_string;
	
}
