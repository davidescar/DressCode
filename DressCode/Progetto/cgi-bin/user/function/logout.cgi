#!/usr/bin/perl -w

use CGI;
use CGI::Session;
use CGI qw(:standard);

use CGI::Carp qw(fatalsToBrowser);

print "Content-type: text/html\n\n";

$session=CGI::Session->load() or die CGI::Session->errstr;
$session->close();
$session->delete();
$session->flush();

print "<html><head><meta http-equiv='refresh' content='0; url=../../home.cgi' /></head></html>";




