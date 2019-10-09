---
title: "Samenvatting bronnen"
author: [Pieter De Clercq]
date: "2019-10-15"
geometry: margin=1in
mainfont: Lato
---

# A learning algorithm for optimizing continuous integration development and testing practice
*Simula Research (Noorwegen); Cisco (Noorwegen)*

Regression testing (tests die zorgen dat reeds gefixte issues niet opnieuw opduiken) is tegelijk heel belangrijk, duurt zeer lang en is niet schaalbaar.

**Probleem:** Redundantie: Tests worden onnodig uitgevoerd en vaak meer dan 1 keer want modulaire software

**Oplossing:** Machine learning algoritme dat bepaalt welke tests uitgevoerd moeten worden en welke niet op basis van historische data en coverage $\Rightarrow$ redundantie vermijden.

# Implementation of Continuous Delivery Systems
*Master Thesis -- University of Tampere (Finland)*

Er bestaat niet echt veel research naar CI, de informatie die bestaat is veelal overal verspreid en niet allemaal samen te vinden.

**Probleem:** Veel bedrijven hebben moeite met snelle release cycles. Bedrijven zijn er wel van overtuigd dat CI goed is, maar hebben vaak moeilijkheden met het te implementeren gezien de willekeur van de job.

**Paper:** Implementatie van een CD systeem in een Fins softwarebedrijf. Vanaf verzamelen van business, technical en user requirements tot en met het uittekenen van een pipeline en de implementatie hiervan op AWS servers.

# Issues on Applying Continuous Integration in Mobile Application Development: A Case Study
*Master Thesis -- University of Tampere (Finland)*

CI wordt toegepast bij een bedrijf dat mobile applicaties maakt. Auteur van de thesis maakt hierna de vergelijking met de (nieuwe) development practice, en de vorige (zonder CI), om aan te tonen wat de voordelen en problemen zijn, met als doel ervoor te zorgen dat developers CI niet links laten liggen en het vooral op de juiste manier toepassen.

# Scaling Continuous Integration
*Conference paper Extreme Programming 2004 (Duitsland)*

Titel leek interessant, maar fulltext was nergens te vinden.

$\Rightarrow$ Aangevraagd op ResearchGate (\url{https://www.researchgate.net/publication/221592550_Scaling_Continuous_Integration})

# Test Agents: The Next Generation of Test Cases
*Malardalen University (Zweden)*

**Probleem:** Software wordt steeds groter en complexer, regression testing duurt steeds langer, er is nood aan automatische test-case selectie tijdens CI.

**Oplossing:** Vervang de simpele test scripts door intelligent agents die kunnen aanpassen en bijleren ("Test agents").

$\Rightarrow$ Decentralizatie van regression testing door test agents zelf te laten bepalen wanneer ze uitgevoerd moeten worden, mogelijks communiceren ze met elkaar.

# Test Case Prioritization for Continuous Regression Testing: An Industrial Case Study
*Simula Research (Noorwegen)*

**Probleem:** Regressietesten duren lang en zijn gebonden door strenge tijdsrestricties. Om dit op te lossen moeten tests volgens een bepaalde manier worden gerangschikt zodanig dat fouten sneller worden gedetecteerd.

**Oplossing:** "ROCKET" algoritme: Test cases rangschikken op basis van eerdere fouten, duur van de tests en andere domein-specifieke heuristieken. Met weights volgorde in de tests bepalen.

# Test prioritization in continuous integration environments
*University of Oulu (Finland)*

2 heuristieken (Diversity-based en History-based) Test Prioritization bestaan, combinatie van de 2 is nog niet echt bestudeerd in CI.

$\Rightarrow$ Regression tests op volgorde uitvoeren door deze 2 heuristieken te combineren, conclusie: Vrij goed voorspelbaar.

# The continuity of continuous integration: Correlations and consequences
*Ericsson, Saab, Chalmers University of Technology (Sweden)*

Veel bedrijven doen reeds CI, maar veel vragen hierover blijven onbeantwoord: Scaling?

**Probleem:** Vanaf wanneer wordt scaling binnen CI een probleem? Welke code size, welk aspect van CI, ...

**Paper:** Correlatie onderzoeken tussen codesize en structuur (+grootte) van devteam $\Rightarrow$ de manier van werken wordt bepaald door het soort team. Opvallend dat frequente integratie er niet persé voor zorgt dat elke developer individueel veel commit

# Towards Cloud Native Continuous Delivery: An Industrial Experience Report
*Vincit; Tampere University of Technology (Finland)*

**Probleem:** Bedrijven hebben moeilijkheden met CI/CDel/CDep implementeren. Hierover is wel wat informatie te vinden, maar scattered

**Oplossing:** Cloud-based Continuous Delivery tool geimplementeerd bij een bedrijf (Vincit), zowel pure cloud als hybrid cloud gebaseerd. Deze paper bevat vaststellingen tijdens die implementatie

# Towards Multi-container Deployment
*KU Leuven*

Storage/verwerking van IoT data verplaatsen van datacenters naar end-devices (load op datacenter verminderen) -> *Multi-purpose IoT gateways*.

**Probleem:** IoT devices zijn resource contrained + applicaties zeer verschillend

$\Rightarrow$ gebruik containers of OS-level virtualisatie

**Paper:** architectuur bespreken + mogelijkheid om dit te implementeren op AGILE (micro-service open source framework voor IoT gateways)

# Usage, Costs, and Benefits of Continuous Integration in Open-Source Projects
*Chicago/Illinois University (USA)*

CI is aan een grote opmars bezig maar nog niet veel aandacht gekregen van onderzoekers.

**Probleem:** Wat zijn de kosten en voordelen van CI nu precies?

**Oplossing:** 35.000 projecten onderzocht, developers geondervraagd om te concluderen dat CI voordelen heeft + kosten in kaart gebracht
