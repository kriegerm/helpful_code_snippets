#!/usr/bin/env python3
import sys

#All the packages for accessing records and URLs
from pubmed_lookup import PubMedLookup
from pubmed_lookup import Publication
email = 'kriegema@ohsu.edu'
from Bio import Entrez
Entrez.email = "kriegema@ohsu.edu" #Entrez requires you to input an email address

#Packages for opening the URLS and extracting information
from bs4 import BeautifulSoup as bs
import urllib3
from selenium import webdriver
import webbrowser
import requests


def search_ncbi(searchterm):
    handle1 = Entrez.esearch(db="pubmed", term=searchterm) #Search pubmed for all entries with the search term specified in the input
    records1 = Entrez.read(handle1)

    #This creates a list of lists, where there is just one list as an entry - the ID numbers found above
    ID_list1 = []
    ID_list1.append((records1["IdList"]))

    #To extract the ID numbers into an actual list of ID numbers and not a list of lists, I have to run this.
    #There is probably a better way to do this but NCBI is awful.
    ID_list2 = []
    for entry in ID_list1:
        for secondentry in entry:
            ID_list2.append(secondentry.strip())

    print("There are %s PubMed ID's fitting your search term. They are:"%len(ID_list2), ID_list2)

    pubmed_URLs = [] #making a list to store the URL's in
    for entry in ID_list2:
        ID = int(entry.strip())
        handle2 = Entrez.esummary(db="pubmed", id =ID)
        record2 = Entrez.parse(handle2)

    #Include these if you want to print out any info about the record
        #for record in record2:
        #    print(record['AuthorList'], record['Title'], record['PubDate'])

        #This works and creates a URL, and then uses the package pubmed_lookup to scan through entires to get a publication URL for the DOI
        URL = str("http://www.ncbi.nlm.nih.gov/pubmed/"+entry.strip())
        lookup = PubMedLookup(URL, email)
        publication = Publication(lookup, resolve_doi=False)
        pubmed_URLs.append((str(publication.url))) #this gives you the URL! and I'm storing it in the list of URLs

    print(pubmed_URLs) #will print out a list of the URLs if you want it to


if __name__ == '__main__':
    if len(sys.argv) == 2:
         search_ncbi(sys.argv[1])
    else:
         print("Usage: search term")
         sys.exit(0)
