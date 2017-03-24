#!/usr/bin/perl -w

use CGI;
use XML::LibXML;
use CGI::Session;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use Digest::SHA1 qw(sha1_hex);

# imposto il path del file dati
my $fileXML='../../../data/utenti.xml';

# costruisco il parser
my $parser=XML::LibXML->new();

# parser del documento
my $doc=$parser->parse_file($fileXML);

# recupero elemento radice
my $root=$doc->getDocumentElement;

#recupero tutti gli utenti
my @allUsers=$doc->findnodes("//utente");

#recupero dati form
my $email=param('email');
my $pass=param('password');

if("$email" eq "") {
	print "Content-type: text/html\n\n";
	print "<html><head><meta http-equiv='refresh' content='0; url=../login.cgi?error=1' /></head></html>"; 
} 
else {

	# hash della password
	$pass = sha1_hex($pass);

	my $found=0;
	my $error=0;

	for $user (@allUsers) {
		
		my $em=$user->findnodes("email");
		my $psw=$user->findnodes("password");
		my $ad=$user->findnodes("attribute::admin");
		
		if("$email" eq "$em"){
			$found=1;
			if("$pass" ne "$psw"){
				$error=1;
			}else{		
				#creazione sessione
				$session=new CGI::Session() or die CGI::Session->errstr;
				
				#creazione cookie di sessione
				print $session->header();

				#memorizzazione variabili di sessione
				$session->param('email',$email);
				if("$ad" eq "0"){
					$session->param('admin','user');
				}else{
					$session->param('admin','admin');
				}
					
			}
			last;			
		}
		
	}

	if(!$found || $error){ 
		print "Content-type: text/html\n\n";
		if(!$found){
			print "<html><head><meta http-equiv='refresh' content='0; url=../login.cgi?error=2' /></head></html>"; 
		}else{
			print "<html><head><meta http-equiv='refresh' content='0; url=../login.cgi?error=3' /></head></html>"; 
		}
	}else{
		print "<html><head><meta http-equiv='refresh' content='0; url=../../home.cgi' /></head></html>";
	}

}
