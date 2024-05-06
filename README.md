# LLM EXTRACTOR :it:

## Introduction

uses llm calls to openapi and azure to extract informations from documents, specifically differents type of kids of different issuers.
uses general prompt extraction on text and pydantic tagging on results and on extracted tables from azure api document-layout service


## Table of Contents

- [Introduction](#introduction)
- [Basic Structure](#basic-structure)
- [Configurations](#configurations)
- [Extractors](#extractors)
  - [Kid](#kid)
  - [Gkid](#gkid)
  - [Leonteq](#leonteq)
  - [BNP](#bnp)
  - [Vontobel](#vontobel)
- [Contact](#contact)
- [DEVS](#devs)

## Basic Structure

generally divided in 3 parts, the first 2 run in parallel different tasks 
1. extracts tables and everything that can be extracted directly
2. extracts from the tables found
3. postprocessing and creating excel or json

## Configurations

every issuer has a number of configs files:
config_X: prompts and general config
json_X: configs for creating the json, renaming and models
tags_X: pydantic classes for the issuer
cleaning_X: regex configs for cleaning results or regex extraction

## Extractors

### Kid

classic and first issuer made, uses direct extraction for market and extraction+tag for general,
tables extract everything else, uses cleaning and is the most worked on 

### Gkid

same as kid but extra problems due to structure changing with rhp, uses a lot more regex and is way faster
performances are set to -

### Leonteq

first derivati extractor, pretty difficult, especially extracting the different ways data can be displayed
dense text is the main difficult chunk
the rest is very standard 
### BNP

very complicated issuer, has lots of data, tables are not recognized well and divided, uses more general table extraction that looks at pages instead of tables

### Vontobel

really easy issuer, no tables, all from text extraction+tag, very fast



### Important Points

- tables are cached in self.di_table_pages ( as azure gives all tables in pages check not just the one you ask)
- fill_table asks azure directly for multiple pages(fills cache), faster but more costly if not all pages used
- if adding more issuers, pls use already developed tools if they exist, regex shortcuts exists in the utils files and llm extractors tools exist in llm_functions.py or extractor.py,
- extractor architecture is Extractor -> Kid_extractor -> Derivati_extractor -> X_extractor
- good luck :finnadie:

## Contact


## DEVS

Current
- Jacopo Morabito
- Marco Menon
- Giovanni Furetti
Past
- Elia Fieberg

for: [Prometeia S.p.A.](https://www.prometeia.com) *DAS*