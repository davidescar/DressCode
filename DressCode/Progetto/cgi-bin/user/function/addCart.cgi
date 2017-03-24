#!/usr/bin/perl -w

use CGI;
use CGI::Session;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

my $codice = param('codice');
my $taglia = param('taglia');
my $colore = param('colore');

print "Content-type: text/html\n\n";

my $session=CGI::Session->load();
my $email=$session->param("email");
my $admin=$session->param("admin");
my $numProd=$session->param("numProd");

if($email){
	my @prod = ($codice,$taglia,$colore);
	if(!$numProd){ 
		$session->param("prod1",\@prod);
		$session->param("qnt1",1);
		$session->param("numProd",1); 
	}else { 
		my $r = checkProduct();
		if($r == 0) {
			my $np=$numProd+1;
			$session->param("prod".$np,\@prod);
			$session->param("qnt".$np,1);
			$session->param("numProd",$np);		
		}else{
			$q=$session->param("qnt".$r)+1;
			$session->param("qnt".$r,$q);
		}
	}
	print "<html><head><meta http-equiv='refresh' content='0; url=../carrello.cgi' /></head></html>";
}else {
	print "<html><head><meta http-equiv='refresh' content='0; url=../schedaProd.cgi?codice=".$codice."&e=1' /></head></html>"; 
}

sub checkProduct { 
	for(my $i=1; $i<=$numProd; $i++) {
		my $c=@{$session->param("prod".$i)}[0];
		my $t=@{$session->param("prod".$i)}[1];
		my $cl=@{$session->param("prod".$i)}[2];
		if("$c" eq "$codice") {
			if("$t" eq "$taglia" && "$cl" eq "$colore") {
				return $i;
			}
		}
	}
	return 0;
}
