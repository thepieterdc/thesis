<!-- $theme: gaia -->
<!-- $size: 4:3 -->

<link rel="stylesheet" href="../styles.css" />

<!-- *footer: Promotors: prof. dr. Volckaert, prof. dr. ir. De Turck | Supervisors: Jasper Vaneessen, Dwight Kerkhove-->

<!-- Note: Welkom -->

<!-- Note: Meer vertellen -->

<!-- Note: Test Prioritering -->

# Optimising ==CI== using
# ==Test Case Prioritisation==

#### June 19, 2020

###### Pieter De Clercq

---

<!-- footer: Pieter De Clercq - July 19, 2020 -->
<!-- page_number: true -->

<!-- Note: Kort structuur -->

<!-- Note: Probleem bespreken -->

## Overview
1) Problem

---

<!-- page_same: true -->

<!-- Note: Bestaande oplossingen -->

## Overview
1) Problem
2) Solutions

---

<!-- Note: Eigen implementatie -->

## Overview
1) Problem
2) Solutions
3) Implementation

---

<!-- Note: Effect op bestaande -->

## Overview
1) Problem
2) Solutions
3) Implementation
4) Results

---

<!-- Note: Demo -->

## Overview
1) Problem
2) Solutions
3) Implementation
4) Results
5) Demo

---

<!-- page_same: false -->
<!-- *template: gaia -->

<!-- Note: Eerst en vooral -->

# ==But== first

---

<!-- Note: Wat? -->

<!-- Note: Afkorting CI -->

# Just what is ==CI==?

---

<!-- Note: Voorbeeld -->

<!-- Note: Bedrijf Android -->

## Continuous Integration

<br/>
<br/>
<center>
	<img src="android.svg" style="height: 150pt" />
  
**Example:** Android app
</center>

---

<!-- page_same: true -->

<!-- Note: Werknemer -->

<!-- Note: CI service op server -->

## Continuous Integration

<br/>
<center>
	<img src="ci-init.svg" />
</center>

---

<!-- Note: Meerdere keren per dag -->

<!-- Note: Sync met werknemers -->

<!-- Note: Integreren -->

## Continuous Integration

<br/>
<center>
	<img src="ci-sync.svg" />
</center>

---

<!-- Note: Checks (Stijl, Compileer) -->

<!-- Note: Tests -->

## Continuous Integration

<br/>
<center>
	<img src="ci-tests-0.svg" />
</center>

---

<!-- Note: Tests -->

## Continuous Integration

<br/>
<center>
	<img src="ci-tests-1.svg" />
</center>

---

## Continuous Integration

<!-- Note: Falen of Slagen -->

<br/>
<center>
	<img src="ci-tests-2.svg" />
</center>

---

<!-- Note: Weet waar is probleem? -->

<!-- Note: Oplossen -->

## Continuous Integration

<br/>
<center>
	<img src="ci-tests-fail.svg" />
</center>

---

<!-- Note: Ofwel slagen -->

## Continuous Integration

<br/>
<center>
	<img src="ci-tests-ok.svg" />
</center>

---

<!-- Note: Automatisch Play Store -->

<!-- Note: Nieuwste versie -->

## Continuous Integration

<br/>
<center>
	<img src="ci-final.svg" />
</center>

---

<!-- page_same: false -->
<!-- *template: gaia -->

<!-- Note: Wat is probleem? -->

# Problem?

---

<!-- Note: In tests -->


# ==Tests!==

---

<!-- Note: Begin -->

<!-- Note: Weinig functionaliteit -->

<!-- Note: Weinig tests -->

## Tests

<center>
	<img src="tests-1.svg" />
</center>

---

<!-- *page_same: true -->

<!-- Note: Tijd verstrijkt -->

## Tests

<center>
	<img src="tests-2.svg" />
</center>

---

<!-- *page_same: true -->

<!-- Note: Meer functionaliteit -->

<!-- Note: Meer tests nodig -->

<!-- Note: Duurt langer [TODO PLAATS TIJD] -->

## Tests

<center>
	<img src="tests-3.svg" />
</center>

---

<!-- *template: gaia -->

<!-- Note:  Wat aan doen? -->

<!-- Note: Drie oplossingen -->

# Solutions

---

<!-- Note: Test Selectie -->

# Solutions

## Test Case ==Selection==

---

<!-- Note: Beschouw tests -->

<!-- Note: Analyseer veranderingen -->

## Solutions / Test Case ==Selection==

<img src="method-initial.svg" style="width: 100%" />

---

<!-- *page_same: true -->

<!-- Note: Welke beinvloed? -->

## Solutions / Test Case ==Selection==

<img src="method-tcs.svg" style="width: 100%" />

---

<!-- Note: Test Minimalisatie -->

# Solutions
## Test Suite ==Minimisation==

---

<!-- Note: Neem tests -->

## Solutions / Test Suite ==Minimisation==

<img src="method-initial.svg" style="width: 100%" />

---

<!-- Note: Voer alles uit -->

<!-- Note: Wanneer tevreden -->

<!-- Note: Permanent -->

<!-- Note: Verschil met Selectie -->

<!-- *page_same: true -->

## Solutions / Test Suite ==Minimisation==

<img src="method-tsm.svg" style="width: 100%" />

---

<!-- Note: Prioritering -->

# Solutions
## Test Case ==Prioritisation==

---

<!-- Note: Vorige technieken -->

<!-- Note: Medische software -->

<!-- Note: Belangrijk alles uitvoeren -->

<!-- Note: Neem alle tests -->

## Solutions  / Test Case ==Prioritisation==

<img src="method-initial.svg" style="width: 100%" />

---

<!-- *page_same: true -->

<!-- Note: Voer allemaal uit -->

<!-- Note: Volgorde -->

<!-- Note: Snel falen -->

<!-- Note: Ontwikkelaar weet waar fout [5M] -->

## Solutions / Test Case ==Prioritisation==

<img src="method-tcp-arrows.svg" style="width: 100%" />

---

<!-- *template: gaia -->

<!-- Note: Voila -->

# So.. problem ==solved!==

---

<!-- Note: Of niet -->

# ..right?

---

<!-- Note: Theorie -->

<!-- Note: Ander paar mouwen -->

<img src="well-yes-but-no.jpg"/>

---

<!-- *template: invert -->

<!-- Note: Wat bestaat? -->

# ==State== of the art

---

<!-- Note: Java -->

<!-- Note: Clover -->

<!-- Note: Vrij goed -->

<!-- Note: Niet aanpasbaar -->

## State of the art

<br/>
<br/>
<img src="state-of-art-1.svg" style="width: 100%" />

---

<!-- Note: Andere talen -->

<!-- Note: Wel ja -->

## State of the art

<br/>
<br/>
<img src="state-of-art-2.svg" style="width: 100%" />

---

<!-- *template: gaia -->

<!-- Note: Naadloos -->

# Implementation

---

<!-- Note: 3 componenten -->

<!-- Note: Uniforme interface -->

<!-- Note: Apart ontwikkelen -->

# Implementation

## <img src="implementation-empty.svg" style="width: 100%" />

---

<!-- page_same: true -->

<!-- Note: Agent -->

# Implementation

## <img src="implementation-1.svg" style="width: 100%" />

---

<!-- Note: Controller -->

# Implementation

## <img src="implementation-2.svg" style="width: 100%" />

---

<!-- Note: Tenslotte -->

# Implementation

## <img src="implementation-full.svg" style="width: 100%" />

---

<!-- page_same: false -->

<!-- Note: Bespreken -->

<!-- Note: Agent -->

# Implementation

## <img src="implementation-full-1.svg" style="width: 100%" />

---

<!-- Note: Ingeplugd in tests -->

<!-- Note: Dus Taal afhankelijk -->

<!-- Note: Twee taken -->

<!-- Note: Volgorde uitvoeren (predictor) -->

## Implementation / Agent

<br/>
<br/>
<center>
	<img src="agent-1.svg" style="width: 75%" />
</center>

---

<!-- Note: Daarnaast -->

<!-- Note: Feedback over uitvoering -->

<!-- *page_same: true -->

## Implementation / Agent

<br/>
<br/>
<center>
	<img src="agent-2.svg" style="width: 75%" />
</center>

---

<!-- Note: Controller -->

# Implementation

## <img src="implementation-full-2.svg" style="width: 100%" />

---

<!-- Note: Agent / Predictor zijn onafh.-->

<!-- Note: Koppelen -->

## Implementation / Controller

<br/>
<br/>
<br/>
<center>
<img src="controller-1.svg" style="width: 75%" />
</center>

---

<!-- *page_same: true -->

<!-- Note: Verwerk resultaten agent -->

<!-- Note: Performantie volgende runs -->

## Implementation / Controller

<br/>
<br/>
<br/>
<center>
<img src="controller-2.svg" style="width: 75%" />
</center>

---

<!-- Note: Predictor -->

# Implementation

## <img src="implementation-full-3.svg" style="width: 100%" />

---

<!-- Note: Volgorde Falen -->

## Implementation / Predictor

<br/>
<br/>
<center>
<img src="predictor-1.svg" style="width: 90%" />
</center>

---

<!-- *page_same: true -->

<!-- Note: 10 Algoritmes -->

<!-- Note: Elk eigen volgorde genereren -->

## Implementation / Predictor

<br/>
<br/>
<center>
<img src="predictor-2.svg" style="width: 90%" />
</center>

---

<!-- *page_same: true -->

<!-- Note: Uitbreidbaar -->

<!-- Note: Interface -->

<!-- Note: Voorbeeld [9M] -->

## Implementation / Predictor

<br/>
<br/>
<center>
<img src="predictor-3.svg" style="width: 90%" />
</center>

<br/>

```python
# Generate a random order.
def predict(test_cases, coverage, results, duration):
	return shuffle(test_cases)
```

---

<!-- Note: Een van 10 -->

<!-- Note: Alpha -->

<!-- Note: Zelf gemaakt -->

<!-- Note: Combineer andere -->

## Implementation / Alpha-algorithm

&nbsp;

---

<!-- page_same: true -->

<!-- Note: Code aangepast -->

<!-- Note: Onlangs gefaald (2 vorige) -->

## Implementation / Alpha-algorithm

1) Unstable, affected test cases (by duration)

---

<!-- Note: Code aangepast -->

## Implementation / Alpha-algorithm

1) Unstable, affected test cases (by duration)
2) Affected test cases (by duration)

---

<!-- Note: Overblijvende tests -->

<!-- Note: Nog niet geteste lijnen -->

## Implementation / Alpha-algorithm

1) Unstable, affected test cases (by duration)
2) Affected test cases (by duration)
3) Test cases based on added coverage

---

<!-- Note: Elke lijn getest -->

<!-- Note: Redundant -->

<!-- Note: Toch uitvoeren [10M] -->

## Implementation / Alpha-algorithm

1) Unstable, affected test cases (by duration)
2) Affected test cases (by duration)
3) Test cases based on added coverage
4) Other test cases <code>[redundant]</code>

---

<!-- page_same: false -->

<!-- Note: Aandachtige luisteraar -->

<!-- Note: 10 algoritmes -->

<!-- Note: 10 volgordes -->

## Implementation / Meta predictor

<img src="metapredictor-1.svg" style="width: 100%" />

---

<!-- page_same: true -->

<!-- Note: Hoe weten? -->

## Implementation / Meta predictor

<img src="metapredictor-2.svg" style="width: 100%" />

---

<!-- Note: Meta predictor -->

## Implementation / Meta predictor

<img src="metapredictor-3.svg" style="width: 100%" />

---

<!-- Note: Eenvoudige tabel -->

<!-- Note: Score per algo -->

<!-- Note: Controller verhoogt als goed -->

<!-- Note: Machine Learning -->

## Implementation / Meta predictor

<img src="metapredictor-4.svg" style="width: 100%" />

---

<!-- page_same: false -->
<!-- *template: gaia -->

<!-- Note: Weten hoe -->

<!-- Note: Kijken hoe goed -->

# Results

---

## Results

<!-- Note: Dodona UGent -->

<!-- Note: Aantal tests tot faal -->

<!-- Note: Grijs origineel -->

<!-- Note: Rood Alpha -->

<!-- Note: 25 keer -->

#### Performance on Dodona (Tests)

<img src="charts/rq4-dodona-alpha.svg" style="width: 100%" />

<br />

<center>
  <strong># test cases:</strong> < 25x
  <br/>
  <span>until first observed failure</span>
</center>

---

## Results

<!-- Note: Tijd -->

<!-- Note: Grafiek gelijkaardig -->

<!-- Note: 40 keer -->

#### Performance on Dodona (Duration)

<img src="charts/rq4-dodona-alpha-time.svg" style="width: 100%" />

<br />

<center>
  <strong>duration:</strong> < 40x
  <br/>
  <span>until first observed failure</span>
</center>

---

<!-- *template: gaia -->

<!-- Note: Demo -->

# Demo

---

<!-- *template: gaia -->

<!-- Note: Samengevat --> 

# Wrapping up

---

## Conclusion

<!-- Note: Tests goed -->

<!-- Note: Fouten detecteren -->

<!-- Note: Eindgebruikers -->

<center>
	<img src="conclusion-tests-begin.svg" style="width: 50%" />
</center>

---

<!-- *page_same: true -->

<!-- Note: Veel tests -->

<!-- Note: Probleem -->

<!-- Note: Traag feedback -->

## Conclusion

<center>
	<img src="conclusion-tests-full.svg" style="width: 50%" />
</center>

---

<!-- Note: Oplossen -->

<!-- Note: Test Prioritering -->

<!-- Note: Rangschikken -->

<!-- Note: Snel falen -->

## Conclusion

<p>&nbsp;</p>
<center>
	<img src="conclusion-reorder.svg" style="width: 20%" />
  <br/>
  <strong>Test Case Prioritisation</strong>
</center>

---

<!-- Note: Resultaat -->

<!-- Note: Wachten daalt -->

<!-- Note: Productiviteit stijgt -->

## Conclusion

<p>&nbsp;</p>
<center>
	<img src="conclusion-time.svg" style="width: 80%" />
</center>

---

<!-- *template: gaia -->

<!-- Note: Was presentatie -->

<!-- Note: Eventuele vragen -->

# Questions?

---

## References
- Slides created using [Marp](https://marpit.marp.app/).
- Icons are property of [FontAwesome](https://fontawesome.com/).
