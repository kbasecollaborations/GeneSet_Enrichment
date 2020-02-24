#!/usr/bin/perl

open (fh,$ARGV[0]) or die "could not open file\n";
while ($input = <fh>)
{
   chomp($input); 
   @arr = split("\t",$input);
   print ($arr[1]."_".$arr[0]."\t".$arr[1]."\t");   
   @geneids  = split(" ",$arr[2]);
   $len = scalar(@geneids);
   for ($i = 0; $i < $len -1; $i++)
   {
      print ($geneids[$i]."\t");
   }
   print($geneids[$len-1]."\n"); 
}
close(fh); 
