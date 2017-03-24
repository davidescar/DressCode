#!/usr/bin/perl -w

use CGI;
use CGI::Session;
use File::Basename;
use XML::LibXML;
use XML::LibXML::PrettyPrint qw();
use HTML::HTML5::Parser qw();
use HTML::HTML5::Writer qw(DOCTYPE_XHTML1);
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

$public_path = "public_html";
$cgi_path = "../cgi-bin";

#========= PRETTY PRINT ============

sub printPrettyHTML {
	
	my $html_string = $_[0];
	my $printer =  XML::LibXML::PrettyPrint->new_for_html( indent_string => "\t" );
	my $html_parser =  HTML::HTML5::Parser->new;
	my $writer = 'HTML::HTML5::Writer'->new(markup => 'xhtml', doctype => +DOCTYPE_XHTML1, charset => 'ASCII');
	
    print $writer->document(
			$printer->pretty_print(
				$html_parser->parse_html_string( $html_string )
			),
		);
	
}

sub printPrettyXML {
	
	my $xml = $_[0];
	
	my $printer = XML::LibXML::PrettyPrint->new (
					indent_string => "\t",
					element => { compact=>[qw/
						email password nome cognome indirizzo citta CAP nazione carta
						materiale tipologia categoria prezzo descrizione taglia colore immagine
						data codice quantita descrizione punteggio
						/]} ); 	
	
	my $document = XML::LibXML->new->parse_file($xml);
		
	open(OUT, ">$xml");
	print OUT $printer->pretty_print($document)->toString;
	close(OUT);
	
}

#============ PARSER ================

sub makeUserParser {
	# se xml non esiste viene creato
	if(!(-e $_[0])) { createDocument($_[0]); }
	# costruisco il parser
	$parserUser = XML::LibXML->new();
	# parser del documento
	$docUser = $parserUser->load_xml(location => $_[0]);
	return;
}

sub makeProductParser {
	# se xml non esiste viene creato
	if(!(-e $_[0])) { createDocument($_[0]); }
	# costruisco il parser
	$parserProd = XML::LibXML->new();
	# parser del documento
	$docProd = $parserProd->load_xml(location => $_[0]); 
	return;
}

sub makeReviewParser {
	# se xml non esiste viene creato
	if(!(-e $_[0])) { createDocument($_[0]); }
	# costruisco il parser
	$parserRec = XML::LibXML->new();
	# parser del documento
	$docRec = $parserRec->load_xml(location => $_[0]); 
	return;	
}

sub makeOrdersParser {
	# se xml non esiste viene creato
	if(!(-e $_[0])) { createDocument($_[0]); }
	# costruisco il parser
	$parserOrder = XML::LibXML->new();
	# parser del documento
	$docOrder = $parserOrder->load_xml(location => $_[0]); 
	return;
}

sub createDocument {
	
	my $xml = $_[0];
	my $filename = basename($xml);
	
	my $xsd;
	my $root;
	
	if("$filename" eq "utenti.xml") { $xsd = "utenti"; $root = "utentiRegistrati"; }
	if("$filename" eq "prodotti.xml") { $xsd = "prodotti"; $root = "catalogo"; }
	if("$filename" eq "ordini.xml") { $xsd = "ordini"; $root = "ordiniEffettuati"; }
	if("$filename" eq "recensioni.xml") { $xsd = "recensioni"; $root = "recensioni"; }
		
	if(defined $xsd && defined $root) {
		
		my $parser = XML::LibXML->new();
		my $doc = XML::LibXML::Document->new("1.0","UTF-8");
		
		my $root_node = $doc->createElement("so:$root");
		$root_node->setAttribute("xmlns:xs","http://www.w3.org/2001/XMLSchema-instance");
		$root_node->setAttribute("xmlns:so","http://informatica.math.unipd.it");
		$root_node->setAttribute("xs:schemaLocation","http://informatica.math.unipd.it $xsd.xsd");
		
		$parser->parse_balanced_chunk($root_node) || die("frammento non ben formato");
		$doc->setDocumentElement($root_node);
		
		open(OUT, ">$xml");
		print OUT $doc->toString;
		close(OUT);
	
	}
	
}

#============ SESSION =============

sub makeSession {	
	if($session=CGI::Session->load()) {
		$email=$session->param("email");
		$admin=$session->param("admin");
	}
	return;
}

#============ CATEGORIES ARRAYS ============

sub getCategories {
	# elenco categorie disponibili
	@categorie = ("Donna", "Uomo", "Bambino");
	#array contenente le tipologie comuni di prodotto
	@tipologie_comuni=("Camicia","Completo","Felpa","Giacca","Giubbotto","Maglione","Pantalone","T-Shirt");
	#array contenente le tipologie donna di prodotto
	@tipologie_donna=("Borsa","Gonna","Orecchini","Shorts","Vestito",);
	#array contenente le tipologie scarpe di prodotto
	@tipologie_scarpe=("Infradito","Scarpa","Stivale");
	#array contenente le tipologie accessori di prodotto
	@tipologie_accessori=("Bracciale","Cappello","Cintura","Collana");
	#array con tutte tipologie senza donna
	@tipologie_uomo = (@tipologie_comuni,@tipologie_scarpe,@tipologie_accessori);
	#array con tutte tipologie
	@tipologie_totali = (@tipologie_comuni,@tipologie_donna,@tipologie_scarpe,@tipologie_accessori);
	#tipologie taglie/colore unici
	@tipologie_uniche = (@tipologie_accessori,"Orecchini");
	#array contenente tutti i materiali
	@materiali=("Acciaio","Argento","Cotone","Cuoio","Jeans","Lana","Lino","Oro","Pelle","Seta","Sintetico","Velluto");
	#array contenente tutti i colori
	@colori=("Nero","Bianco","Azzurro","Rosso","Giallo","Blu","Marrone","Grigio","Verde","Arancione","Viola","Rosa");
	#array contenente tutte le fasce di prezzo
	@prezzi=("&lt; 20 &euro;","20-50 &euro;","50-100 &euro;","&gt; 100 &euro;");
	$dimPr = @prezzi;
	# elenco taglie tradizionali disponibili
	@taglieChar = ("XXS", "XS", "S", "M", "L", "XL", "XXL", "XXXL");
	# elenco taglie (numeri) disponibili
	my $min=38;	my $max=45;
	@taglieNum = ($min);
	for($i=$min+1; $i<=$max; $i++){
		push(@taglieNum,$i-0.5); 
		push(@taglieNum,$i);
	}
	return;
}

#============ OTHERS FUNCTIONS ==========

#funzione per sostituzione sottostringa $_[1] con un'altra $_[2]
#nella stringa data $_[0]
sub replace {
	my $pos = index($_[0], $_[1]); #cerca posizione iniziale 
	while ( $pos > -1 ) {
		substr( $_[0], $pos, length( $_[1] ), $_[2] );
		$pos = index( $_[0], $_[1], $pos + length( $_[2] ));
	}
	return;
}

sub getCSSPage {
	
	my $perlPage = $_[0];	
	my %cssPages = (
		"home.cgi" => "home.css",
		"login.cgi" => "login.css",
		"registration.cgi" => "registration.css",
		"prodList.cgi" => "list.css",
		"search.cgi" => "list.css",
		"schedaProd.cgi" => "scheda.css",
		"carrello.cgi" => "carrello.css",
		"profile.cgi" => "profile.css",
		"ordini.cgi" => "ordini.css",
		"dashboard.cgi" => "dashboard.css",
		"viewProducts.cgi" => "products.css",
		"selectProd.cgi" => "formAdmin.css",
		"formAddProd.cgi" => "formAdmin.css",
		"formModProd.cgi" => "formAdmin.css",
		"deleteProd.cgi" => "formAdmin.css",
	);
	
	if (!(defined $cssPages{$perlPage})) { return "base.css"; }
	else { return $cssPages{$perlPage}; }
	
}

sub getCSSPageMobile {
	
	my $perlPage_m = $_[0];	
	my %cssPages_m = (
		"home.cgi" => "home_m.css",
		"login.cgi" => "login_m.css",
		"registration.cgi" => "registration_m.css",
		"prodList.cgi" => "list_m.css",
		"search.cgi" => "list_m.css",
		"schedaProd.cgi" => "scheda_m.css",
		"carrello.cgi" => "carrello_m.css",
		"profile.cgi" => "profile_m.css",
		"ordini.cgi" => "ordini_m.css",
		"dashboard.cgi" => "dashboard_m.css",
		"viewProducts.cgi" => "products_m.css",
		"selectProd.cgi" => "formAdmin_m.css",
		"formAddProd.cgi" => "formAdmin_m.css",
		"formModProd.cgi" => "formAdmin_m.css",
		"deleteProd.cgi" => "formAdmin_m.css"
	);
	
	if (!(defined $cssPages_m{$perlPage_m})) { return "base_m.css"; }
	else { return $cssPages_m{$perlPage_m}; }
	
}

#=============== BREADCRUMBS ====================

# ritorna il nome dello script della pagina corrente
sub current_page {
    return url( -relative => 1 );
}


# ritorna il link relativo alla pagina corrente
sub current_link {
	my $actLink=$ENV{'REQUEST_URI'};
	$actLink=~ s/^(.*[\\\/])//;
	$actLink=~ s/&.*//;
	return $actLink;
}


# ritorna il link relativo alla pagina precedente
sub past_link {
	my $preLink=$ENV{'HTTP_REFERER'};
	$preLink=~ s/^(.*[\\\/])//;
	$preLink=~ s/&.*//;
	
	# sistemazioni per home.cgi che si trova ad un livello superiore
	if("$preLink" eq "home.cgi"){ $preLink="../".$preLink; }
	
	return $preLink;
}

# restituisce la pagina di provenienza per la pagina indicata
sub parentPage {
	my $page_id = $_[0];
	
	#aggiustamenti per le pagine di cui non servono i parametri
    $page_id = paramPage($page_id);
    
    my $pastPage = past_link();
    
    # Hash coppie 'pagina => genitore'
    my %parents = (
        '../home.cgi' => 'no',
        'home.cgi' => 'no',
        'login.cgi' => 'no',
        'registration.cgi' => 'no',
        'carrello.cgi' => 'no',
        'prodList.cgi' => '../home.cgi',
        'prodList.cgi?tipo=Uomo' => '../home.cgi',
        'prodList.cgi?tipo=Donna' => '../home.cgi',
        'prodList.cgi?tipo=Bambino' => '../home.cgi',
        'prodList.cgi?prom=yes' => '../home.cgi',        
        'schedaProd.cgi' => $pastPage,
        'search.cgi' => '../home.cgi',
        'dashboard.cgi' => 'no',
        '../dashboard.cgi' => 'no',
        'viewProducts.cgi' => 'dashboard.cgi',
        'selectProd.cgi' => 'dashboard.cgi',
        'selectProd.cgi?form=0' => 'dashboard.cgi',
        'selectProd.cgi?form=1' => 'dashboard.cgi',
        'selectProd.cgi?form=2' => 'dashboard.cgi',
        'selectProd.cgi?form=3' => 'dashboard.cgi',
        '../selectProd.cgi?form=2' => '../dashboard.cgi',
        'formAddProd.cgi' => 'selectProd.cgi?form=0',
        'formModProd.cgi' => 'selectProd.cgi?form=1',
        'deleteProd.cgi' => '../selectProd.cgi?form=2',
        'formDelUser.cgi' => 'selectProd.cgi?form=3',        
        'profile.cgi' => 'no',
        'profile.cgi?op=ok' => 'no',
        'profile.cgi?form=profile' => 'profile.cgi',
        'profile.cgi?form=password' => 'profile.cgi',
        'profile.cgi?form=address' => 'profile.cgi',
        'profile.cgi?form=credit' => 'profile.cgi',
        'ordini.cgi' => 'profile.cgi',
        'pagina'=> 'no'
    );	
	
    if ( defined $parents{$page_id} ) { return $parents{$page_id}; }
    else { return $parents{'pagina'}; }
}



# costruisce i breadcrumbs passo passo
sub breadcrumbs {	
    my $page_id = $_[0];
    
    #aggiustamenti per pagine speciali
    if("$page_id" eq "prodList.cgi" or "$page_id" eq "profile.cgi" ){ $page_id=current_link(); }
    
    #elenco pagine admin
    my @pagineAdmin=("dashboard.cgi", "viewProducts.cgi", "selectProd.cgi", "formDelUser.cgi", "carrello.cgi");
    
    my $i=0;
    my @brcrPages;
    @brcrPages[$i]='<li>'.nomePag($page_id).'</li>';
    $pastPage = parentPage($page_id);

    while ( $pastPage ne "no" ) {
		$i++;
		
		# aggiustamenti per la cartella di destinazione del path della pagina precedente
		my $selPath="../user/";
		if($pastPage eq "../home.cgi"){ $selPath=""; }
		$pastPageName=$pastPage;
		$pastPageName=~ s/\?.*//;
		if(grep{ $_ eq $pastPageName} @pagineAdmin){ $selPath="../admin/"; }		
        
        @brcrPages[$i] = '<li><a href="'.$selPath."".$pastPage.'">'.nomePag($pastPage).'</a></li>';
        $pastPage  = parentPage($pastPage);
    }

    for($i; $i>=0; $i--){ $breadcrumb .=@brcrPages[$i]; }
    return $breadcrumb;
}



# fornisce il nome per una pagina
sub nomePag {
    my $page_id = $_[0];
    
    #aggiustamenti per le pagine di cui non servono i parametri
    $page_id = paramPage($page_id);
    
    my %titolo  = (
        '../home.cgi' => 'Home',
        'home.cgi' => 'Home',
        'prodList.cgi' => 'Prodotti',
        'prodList.cgi?tipo=Uomo' => 'Prodotti Uomo',
        'prodList.cgi?tipo=Donna' => 'Prodotti Donna',
        'prodList.cgi?tipo=Bambino' => 'Prodotti Bambino',
        'prodList.cgi?prom=yes' => 'Promozioni',
        'schedaProd.cgi' => 'Scheda Prodotto',
        'login.cgi' => 'Login',
        'registration.cgi' => 'Registrazione',
        'carrello.cgi' => 'Carrello',
        'search.cgi' => 'Ricerca',
        'dashboard.cgi' => 'Dashboard Admin',
        '../dashboard.cgi' => 'Dashboard Admin',
        'viewProducts.cgi' => 'Lista Completa Prodotti',
        'selectProd.cgi' => 'Selezione Prodotto',
        'selectProd.cgi?form=0' => 'Selezione Prodotto',
        'selectProd.cgi?form=1' => 'Selezione Prodotto',
        'selectProd.cgi?form=2' => 'Selezione Prodotto',
        'selectProd.cgi?form=3' => 'Selezione Utente',
        '../selectProd.cgi?form=2' => 'Selezione Prodotto',
        'formAddProd.cgi' => 'Inserimento Prodotto',
        'formModProd.cgi' => 'Modifica Prodotto',
        'deleteProd.cgi' => 'Elimina Prodotto',
        'formDelUser.cgi' => 'Elimina Utente',        
        'profile.cgi' => 'Gestione Profilo',
        'profile.cgi?op=ok' => 'Gestione Profilo',
        'profile.cgi?form=profile' => 'Gestione Identit&agrave;',
        'profile.cgi?form=password' => 'Gestione Password',
        'profile.cgi?form=address' => 'Gestione Indirizzo',
        'profile.cgi?form=credit' => 'Gestione Carta',
        'ordini.cgi' => 'Storico Ordini',        
        'pagina' => 'Pagina'
    );

    if ( defined $titolo{$page_id} ) { return $titolo{$page_id}; }
    else { return $titolo{'pagina'}; }
}

# fornisce la descrizione per una determinata pagina
sub pageDescr {
    my $page_id = $_[0];
        
    #aggiustamenti per le pagine di cui non servono i parametri
    $page_id = paramPage($page_id);
    
    my %descr = (
        "home.cgi"   => "Pagina principale del sito DressCode",
        "prodList.cgi"  => "Lista dei prodotti di DressCode",
        "prodList.cgi?tipo=Uomo" => "Lista dei prodotti per uomo di DressCode",
        "prodList.cgi?tipo=Donna" => "Lista dei prodotti per donna di DressCode",
        "prodList.cgi?tipo=Bambino" => "Lista dei prodotti per bambino di DressCode",
        "prodList.cgi?prom=yes" => "Lista dei prodotti in promozione di DressCode",
        "schedaProd.cgi" => "Pagina di dettaglio di un prodotto di DressCode",
        "login.cgi" => "Pagina di accesso all&#39account DressCode",
        "registration.cgi" => "Pagina di registrazione al sito DressCode",
        "carrello.cgi" => "Pagina di gestione del carrello personale di DressCode",
        "carrello.cgi?ins=ok" => "Pagina di visualizzazione ordine effettuato dal carrello personale di DressCode",
        "search.cgi" => "Pagina dei risultati di ricerca di prodotti in DressCode",
        "dashboard.cgi" => "Pagina di gestione per l&#39amministratore del sito DressCode",
        "viewProducts.cgi" => "Pagina di visualizzazione rapida di tutti i prodotti di DressCode",
        "selectProd.cgi" => "Pagina di selezione del prodotto di DressCode",
        "selectProd.cgi?form=0" => "Pagina di selezione del prodotto da inserire nel database di DressCode",
        "selectProd.cgi?form=1" => "Pagina di selezione del prodotto da modificare nel database di DressCode",
        "selectProd.cgi?form=2" => "Pagina di selezione del prodotto da eliminare dal database di DressCode",
        "selectProd.cgi?form=3" => "Pagina di selezione dell&#39utente da eliminare dal database di DressCode",
        "formAddProd.cgi" => "Pagina di inserimento di un nuovo prodotto nel database di DressCode",
        "formModProd.cgi" => "Pagina di modifica di un prodotto nel database di DressCode",
        "deleteProd.cgi" => "Pagina di cancellazione di un prodotto dal database di DressCode",
        "formDelUser.cgi" => "Pagina di cancellazione di un utente dal database di DressCode",        
        "profile.cgi" => "Pagina di gestione del profilo personale di un utente del sito DressCode",
        "profile.cgi?form=profile" => "Pagina di gestione delle informazioni sull&#39identità di un utente del sito DressCode",
        "profile.cgi?form=password" => "Pagina di gestione della password di un utente del sito DressCode",
        "profile.cgi?form=address" => "Pagina di gestione dell&#39indirizzo personale di un utente del sito DressCode",
        "profile.cgi?form=credit" => "Pagina di gestione della carta di credito personale di un utente del sito DressCode",
        "ordini.cgi" => "Pagina di visualizzazione dello storico degli ordini effettuati da un utente del sito DressCode",    
        "pagina"   => "Sito DressCode"
    );

    if ( defined $descr{$page_id} ) {
        return $descr{$page_id};
    }
    else {
        return $descr{'pagina'};
    }
}


sub paramPage {
	my $page_id = $_[0];
	
	#aggiustamenti pagine speciali
    my @pageParam=("prodList.cgi", "selectProd.cgi", "../selectProd.cgi", "profile.cgi");  
    my $pageName=$page_id;
    $pageName=~ s/\?.*//;
    if(! grep{ $_ eq $pageName} @pageParam){ $page_id=$pageName; }
    
    return $page_id;
}


# funzione per l'aggiunta dei tabindex
sub tabIndex {
    if ( !( defined $tabindex ) || $tabindex < 1 ) { $tabindex = 1; }
    else { $tabindex++; }
    return "tabindex=\"".$tabindex."\"";
}

sub makeALink {
	my $link = $_[0];
	my $content = $_[1];
	return "<a href='$link' ".tabIndex().">$content</a>";
}


#================ HTML =================

sub getHTMLHeader {
	
	my $title = $_[0];
	my $keywords = "abbigliamento,abiti,store,online".($_[1] ? ",$_[1]" : "");
	
	my $cssPage = getCSSPage(current_page());
	my $cssPage_m = getCSSPageMobile(current_page());
		
	my $string = "
	<html xml:lang='it' lang='it'>
		<head>
			<title>$title</title>
			<meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>
			<meta name='title' content='DressCode' />
			<meta name='author' content='DressCodeTeam' />
			<meta name='language' content='italian it' />
			<meta name='keywords' content='$keywords' />
			<meta name='description' content='".pageDescr(current_link())."' />
			<link rel='stylesheet' type='text/css' href='/$public_path/css/desktop/$cssPage'/>
			<link rel='stylesheet' type='text/css' media='only screen and (max-width: 480px), only screen and (max-device-width: 480px)' href='/$public_path/css/mobile/$cssPage_m'/>
		</head>
		<body>";		
	
	#aggiunta body header [navbar title menu]
	$string .= getBodyHeader();	
		
	return $string;
	
}

sub getBodyHeader {
	
	my $c_page = current_page();
	my $q_string = $ENV{'QUERY_STRING'};
	
	#navbar
	my $string = "<ul id='navbar'>";
	if($email){
		
		#cerco nome e cognome utente
		my $query="//utente[email='$email']";
		my $user=$docUser->findnodes($query)->get_node(1);
		my $nome=$user->findnodes('nome');
		my $cognome=$user->findnodes('cognome');
		
		#se presenti stampo nome cognome altrimenti email
		my $identity = (("$nome" ne "") ? "$nome $cognome" : "$email");

		$string .= "<li id='imguser'>".(("$c_page" ne "profile.cgi") ? makeALink("/$cgi_path/user/profile.cgi",$identity) : $identity )."</li>";
		
		#creazione link gestione se admin o profilo se user
		if("$admin" eq "admin"){
			$string .= "<li id='imggest'>".(("$c_page" ne "dashboard.cgi") ? makeALink("/$cgi_path/admin/dashboard.cgi","Gestione") : "Gestione")."</li>";
		}else{
			$string .= "<li id='imgcart'>".(("$c_page" ne "carrello.cgi") ? makeALink("/$cgi_path/user/carrello.cgi","Carrello") : "Carrello")."</li>";
		}
		
		$string .="<li id='imgout'><a href='/$cgi_path/user/function/logout.cgi' ".tabIndex().">Log Out</a></li>";
		
	}else{
		$string .=	
		"<li id='imglog'>".(("$c_page" ne "login.cgi") ? makeALink("/$cgi_path/user/login.cgi","Accedi") : "Accedi")."</li>".
		"<li id='imgreg'>".(("$c_page" ne "registration.cgi") ? makeALink("/$cgi_path/user/registration.cgi","Registrati") : "Registrati")."</li>".
		"<li id='imgcart'>".(("$c_page" ne "carrello.cgi") ? makeALink("/$cgi_path/user/carrello.cgi","Carrello") : "Carrello")."</li>";
	}			
	$string .="</ul>
	
	<h1 id='title'><span id='logo'>DressCode</span></h1>
	<ul id='menu'>
		<li>".(("$c_page" ne "home.cgi") ? makeALink("/$cgi_path/home.cgi","Home") : "Home")."</li>
		<li>".(("$q_string" ne "tipo=Uomo") ? makeALink("/$cgi_path/user/prodList.cgi?tipo=Uomo","Uomo") : "Uomo")."</a></li>
		<li>".(("$q_string" ne "tipo=Donna") ? makeALink("/$cgi_path/user/prodList.cgi?tipo=Donna","Donna") : "Donna")."</a></li>
		<li>".(("$q_string" ne "tipo=Bambino") ? makeALink("/$cgi_path/user/prodList.cgi?tipo=Bambino","Bambino") : "Bambino")."</a></li>
		<li>".(("$q_string" ne "prom=yes") ? makeALink("/$cgi_path/user/prodList.cgi?prom=yes","Promozioni") : "Promozioni")."</a></li>	
	</ul>
	
	<form id='search' action='/$cgi_path/user/search.cgi' method='get'>
		<fieldset>
			<input type='text' id='query' name='query' value='Ricerca prodotti...' onclick='value=&#34;&#34;' ".tabIndex()."/>
			<input type='submit' class='psubmit' value='Cerca' />
		</fieldset>
	</form>";
	
	#breadcrumb
	if(!defined($brd)){ $brd = breadcrumbs( current_link() ); }
	$string .= "<p id='brdIntro'>Ti trovi in: </p><ul id='breadcrumb'>".$brd."</ul>";
				
	$string .= "<div id='contents'>";
	
	return $string;
	
}

sub formSetPromo {
	
	my $code = $_[0];
	
	my $html_string = "
	<form action='../admin/function/setPromoProd.cgi' method='get'>
		<div>
			<input type='hidden' name='codice' value='$code' />
			<input type='hidden' name='promo' value='aggiungi' />
			<input type='text' name='sconto' size='3' maxlenght='3' class='add_prom'/>
			<input type='submit' class='psubmit' value='Metti in promozione' />
		</div>
	</form>";
	
	return $html_string;
	
}

sub getFooter {
	
	my $string = "</div>
	<div id='footer'>
	<div>";
	
	#pagamenti
	my @payments = ("American Express","Master Card","Paypal","Visa","Postepay");
	$string .= "
	<div>
		<p class='title_foot'>Pagamenti Accettati</p>
		<ul id='payments'>";
		for my $p(@payments) {
			$string .= "<li><span class='hid'>$p</span></li>";
		}
		$string .= "</ul>
	</div>";
	
	#gruppo progetto
	my @group = ("Canal Davide","Casotto Federico","Pegoraro Gianluca","Scarparo Davide");
	$string .= "
	<div>
		<p class='title_foot'>DressCode Team</p>
		<ul id='group_list'>";
		for my $g(@group) {
			$string .= "<li>$g</li>";
		}
		$string .= "</ul>
	</div>";
	
	#certificazioni
	$string .= "
	<div>
		<p class='title_foot'>Certificazioni</p>
		<ul id='certifications'>		
			<li><span class='hid'>W3C XHTML 1.0 Valid</span></li>
			<li><span class='hid'>W3C CSS Valid</span></li>
		</ul>
	</div>";
	
	#chiusura footer e documento
	$string .= "
			</div>
			</div>
		</body>
	</html>";
	
	return $string;
	
}

1;
