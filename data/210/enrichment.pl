#!/usr/bin/perl
#use Math::GSL::CDF qw/:beta/;
#print gsl_cdf_beta_P(1,2,3) . "\n";
use strict;
use warnings;

my %go_dict;
my %gene_ids;
my %gene_go;

=pod
sub logfact {
   return gammln(shift(@_) + 1.0);
}

sub gammln {
  my $xx = shift;
  my @cof = (76.18009172947146, -86.50532032941677,
             24.01409824083091, -1.231739572450155,
             0.12086509738661e-2, -0.5395239384953e-5);
  my $y = my $x = $xx;
  my $tmp = $x + 5.5;
  $tmp -= ($x + .5) * log($tmp);
  my $ser = 1.000000000190015;
  for my $j (0..5) {
     $ser += $cof[$j]/++$y;
  }
  -$tmp + log(2.5066282746310005*$ser/$x);
}

sub hypergeom {
    my ($n, $m, $N, $i) = @_;

    my $loghyp1 = $logfact[ $m ] + $logfact[ $n ] + $logfact[ $N ] + $logfact[ $m + $n - $N ];
    my $loghyp2 = $logfact[ $i ] + $logfact[ $n - $i ] + $logfact[ $m + $i - $N ] + $logfact[ $N - $i ]  + $logfact[ $m + $n ];

    return exp($loghyp1 - $loghyp2);
}
=cut




open(my $fh, $ARGV[0]) or die "could not open gmt file";
while(my $input = <$fh>)
{
   chomp($input);
   my @rec;
   @rec=split("\t",$input);
   my $goid;
   $goid = $rec[1];
   $go_dict{$rec[1]} = $#rec-1;

   for (my $i =2; $i < $#rec+1; $i++)
   {
     if(exists $gene_go{$rec[$i]}) {
      push(@{$gene_go{$rec[$i]}},$goid);
     } else {
     my @goids=();
     push(@goids,$goid);
     $gene_go{$rec[$i]}=\@goids;
   }

       $gene_ids{$rec[$i]} = 1;
   }
}
close($fh);

my $N = keys %gene_ids;


foreach my $key (keys %go_dict)
{
 # print "$key costs $go_dict{$key}\n";
}

foreach my $key (keys %gene_go)
{
  #print "$key --- @{$gene_go{$key}}\n";
}


my $K = 0;
my $k = 0;
my $n = 0;

my %gofreq;
open (my $fgl, $ARGV[1])  or die "could not open gene list\n";
while (my $line = <$fgl>)
{
   chomp($line);
   my @genearray;
   @genearray=split("\t",$line);
   #print(@genearray."\n");
   $n = scalar(@genearray);
   for (my $j = 0; $j < $#genearray; $j++)
   {
      if(exists ($gene_go{$genearray[$j]}))
      {
         #print("$genearray[$j]---@{$gene_go{$genearray[$j]}}\n");
         my @go_inputs = @{$gene_go{$genearray[$j]}};
         for (my $c=0; $c < $#go_inputs ; $c++)
         {
             $gofreq{$go_inputs[$c]}++; 
         }   
      }
   }
}
close($fgl);

foreach my $key (keys %gofreq)
{
  #print "$key --- $gofreq{$key}\n";
}

my $input_goid;
$input_goid = $ARGV[2];
print($input_goid."\n");
$K = $go_dict{$input_goid};
print("n = ".$n."\n");
print("N = ".$N."\n");
print("K = ".$K."\n");
$k = $gofreq{$input_goid};
print ("k = ".$k."\n");

#print hypergeom( $K, $N, $n, $k );



