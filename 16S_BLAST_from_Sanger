#!/usr/bin/env bash

##########################################################################
#
#
#
#
##########################################################################

'''
#Only run this for code optimization
rm -rf ./combinedSeqs
rm -rf ./ClustalWAlignments
rm -rf ./ConsensusSeqs
rm -rf ./Mergers
rm -rf ./BlastResults
'''

#create some directories for our outputs
mkdir combinedSeqs
mkdir ClustalWAlignments
mkdir ConsensusSeqs
mkdir Mergers
mkdir BlastResults

#Look through the sequence directory and make an array of each of the sample identifiers
arr=()
search_dir=./Seqs
for entry in "$search_dir"/*
do
  name=${entry%_*}
  name=${name##*/}
  arr+=($name)
done

#Makes an array of unique values of sample identifiers
uniqs_arr=($(for ip in "${arr[@]}"; do echo "${ip}"; done | sort -u))

#For each unique value, we are going to use emboss revseq to reverse complement and make a new rc file
for value in "${uniqs_arr[@]}"
do

  echo "Analyzing sequences for identifier " $value;

  revseq ./Seqs/$value"_R.fasta" ./Seqs/rc_$value"_R.fasta";

  #combine the two F and rc files into one in a new directory
  cat ./Seqs/rc_$value"_R.fasta" ./Seqs/$value"_F.fasta" >> ./combinedSeqs/$value"_F_rcR.fasta";

  #Now well use clustalw to create an alignment file from the _F and rc files
  clustalw -infile="./combinedSeqs/"$value"_F_rcR.fasta" -output=FASTA -outfile="./ClustalWAlignments/"$value"_clustalw.fasta" -quiet;

  #Then are going to make a consensus sequence from the clustalw output
  consambig "./ClustalWAlignments/"$value"_clustalw.fasta" "./ConsensusSeqs/"$value"_cons.fasta" -name=$value;

  #Also create a merger file so you can manually look at the alignment if you want to
  merger -asequence="./Seqs/"$value"_F.fasta" -bsequence="./Seqs/rc_"$value"_R.fasta" -outfile="./Mergers/"$value"_merged.fasta" -outseq=FASTA;

  #delete the original rc file for now so my program doesnt get confused when I run it.
  rm ./Seqs/rc_$value"_R.fasta";

  #Now we can use blast to search for results!
  ~/ncbi-blast-2.13.0+/bin/blastn -db ~/blastdb/16S_ribosomal_RNA -query "./ConsensusSeqs/"$value"_cons.fasta" -max_hsps 1 -max_target_seqs 100 -out "./BlastResults/"$value"_blastn_results.csv" -outfmt '10 qseqid qstart qend stitle sseqid sacc sstrand slen sstart send sseq evalue length pident nident mismatch gapopen gaps';
done

#Adding a header to our blast results
for csv in ./BlastResults/*.csv; do (echo "qseqid,qstart,qend,stitle,sseqid,sacc,refseq,sstrand,slen,sstart,send,sseq,evalue,length,pident,nident,mismatch,gapopen,gaps"; cat $csv) > tmp; mv tmp $csv; done

#Make a new csv with all the top hits
echo "qseqid,qstart,qend,stitle,sseqid,sacc,refseq,sstrand,slen,sstart,send,sseq,evalue,length,pident,nident,mismatch,gapopen,gaps" >> ./BlastResults/Top-hits.csv
for csv in ./BlastResults/*.csv; do awk 'NR==2 {print; exit}' $csv >> ./BlastResults/Top-hits.csv; done
