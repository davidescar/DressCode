#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

sub isEmpty {
	return ("$_[0]" eq "" ? "<li>Il campo $_[1] non pu&ograve; essere vuoto</li>" : "");
}

sub isValidPrice {
	return (($_[0] =~ /^([1-9][0-9]*|0)((,|.)[0-9]{2})?$/) ? "" : "<li>Il campo prezzo non &egrave; valido</li>");
}

sub isValidImage {
	return (($_[0] =~ /^.+\.(jpeg|jpg|png|gif|bmp)$/) ? "" : "<li>Formato campo immagine non valido (formati accettati: JPG, PNG, GIF e BMP).</li>");
}

#subroutine per upload immagine se non presente nella cartella prodotti
sub uploadImage {
		
	$CGI::POST_MAX = 1024*5000; #limito dimensione immagini possibili da caricare
	my $page = new CGI;
	my $safe_filename_characters = "a-zA-Z0-9_.-"; #caratteri consentiti nome del file
	my $upload_dir = "../../public_html/images/prodotti"; #cartella destinazione upload file
	
	my $filename = $page->param($_[0]) or die ("Impossibile inserire immagine di queste dimensioni!");
	
	#rimozione percorsi indesiderati, interessa solo nome file e estensioni
	my ( $name, $path, $extension ) = fileparse ( $filename, '..*' );
	$filename = $name . $extension; 
	
	$filename =~ tr/ /_/;
	$filename =~ s/[^$safe_filename_characters]//g;
	
	#controllo se il file contiene caratteri indesiderati
	if ( $filename =~ /^([$safe_filename_characters]+)$/ ) {
		$filename = $1;
	}
	else{	die "Filename contains invalid characters";	}
	
	#carico il file nella cartella destinazione
	my $upload_filehandle = $page->upload($_[0]);
	
	open ( UPLOADFILE, ">$upload_dir/$filename" ) or die "$! || >$upload_dir/$filename";
	binmode UPLOADFILE;

	while ( <$upload_filehandle> ) {
		print UPLOADFILE;
	}
	
	close UPLOADFILE;
	
	return;
	
}


1;
