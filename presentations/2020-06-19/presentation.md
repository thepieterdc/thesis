<!-- $theme: gaia -->

<link rel="stylesheet" href="../styles.css" />

<!-- *footer: Promotors: prof. dr. Volckaert, prof. dr. ir. De Turck | Supervisors: Jasper Vaneessen, Dwight Kerkhove-->

# Optimising ==CI== using
# ==Test Case Prioritisation==

#### June 19, 2020

###### Pieter De Clercq

---

<!-- footer: Pieter De Clercq - July 19, 2020 -->
<!-- page_number: true -->

## Overview
1) Problem

---

<!-- page_same: true -->

## Overview
1) Problem
2) Solutions

---

## Overview
1) Problem
2) Solutions
3) Implementation

---

## Overview
1) Problem
2) Solutions
3) Implementation
4) Results

---

## Overview
1) Problem
2) Solutions
3) Implementation
4) Results
5) (Demo)

---

<!-- page_same: false -->
<!-- *template: gaia -->

# ==But== first

---

# Just what is ==CI==?

---

## Continuous Integration

<center>
	<img src="android.svg" style="height: 200pt" />
  
**Example:** Android app
</center>

---

<!-- page_same: true -->
## Continuous Integration

<center>
	<img src="ci-fail-init.svg" />
</center>

---

## Continuous Integration

<center>
	<img src="ci-fail-sync.svg" />
</center>

---

## Continuous Integration

<center>
	<img src="ci-fail-tests-init.svg" />
</center>

---

## Continuous Integration

<center>
	<img src="ci-fail-tests-1.svg" />
</center>

---

## Continuous Integration

<center>
	<img src="ci-fail-tests-2.svg" />
</center>

---

## Continuous Integration

<center>
	<img src="ci-fail-final.svg" />
</center>

---

## Continuous Integration

<center>
	<img src="ci-ok-init.svg" />
</center>

---

## Continuous Integration

<center>
	<img src="ci-ok-sync.svg" />
</center>

---

## Continuous Integration

<center>
	<img src="ci-ok-tests-init.svg" />
</center>

---

## Continuous Integration

<center>
	<img src="ci-ok-tests-1.svg" />
</center>

---

## Continuous Integration

<center>
	<img src="ci-ok-tests-2.svg" />
</center>

---

## Continuous Integration

<center>
	<img src="ci-ok-tests-3.svg" />
</center>

---

## Continuous Integration

<center>
	<img src="ci-ok-final.svg" />
</center>

---

<!-- page_same: false -->

<!-- *template: gaia -->

# Problem?

---


# ==Tests!==

---

## Tests

<center>
	<img src="tests-1.svg" />
</center>

---

<!-- *page_same: true -->

## Tests

<center>
	<img src="tests-2.svg" />
</center>

---

<!-- *page_same: true -->

## Tests

<center>
	<img src="tests-3.svg" />
</center>

---

<!-- *template: gaia -->

# Solutions

---

# Solutions

## Test Case ==Selection==

---

## Solutions / Test Case ==Selection==

<img src="method-initial.svg" style="width: 100%" />

---

<!-- *page_same: true -->

## Solutions / Test Case ==Selection==

<img src="method-tcs.svg" style="width: 100%" />

---

# Solutions
## Test Suite ==Minimisation==

---

## Solutions / Test Suite ==Minimisation==

<img src="method-initial.svg" style="width: 100%" />

---

<!-- *page_same: true -->

## Solutions / Test Suite ==Minimisation==

<img src="method-tsm.svg" style="width: 100%" />

---

# Solutions
## Test Case ==Prioritisation==

---

## Solutions  / Test Case ==Prioritisation==

<img src="method-initial.svg" style="width: 100%" />

---

<!-- *page_same: true -->

<!-- Voorbeeld: kritische tests voor medische shizzle -->

## Solutions / Test Case ==Prioritisation==

<img src="method-tcp-arrows.svg" style="width: 100%" />

---

<!-- *template: gaia -->

# So.. problem ==solved!==

---

# ..right?

---

<!-- Wel, de waarheid is dat het probleem hiermee niet is opgelost. -->

<img src="well-yes-but-no.jpg"/>

---

<!-- *template: invert -->

<!-- Dit is theoretisch allemaal heel mooi, maar laten we eens kijken naar welke implementaties er bestaan. -->

# ==State== of the art

---

<!-- Clover (door Atlassian - BitBucket) bestaat voor Java, is onlangs geopensourced. Werkt vrij goed maar enkel voor Java en 5 ingebouwde manieren om tests te herordenen. -->

## State of the art

<br/>
<br/>
<img src="state-of-art-1.svg" style="width: 100%" />

---

<!-- Voor alle andere programmeertalen is er geen algemeen iets dat gemakkelijk uitbreidbaar is. -->

## State of the art

<br/>
<br/>
<img src="state-of-art-2.svg" style="width: 100%" />

---

<!-- *template: gaia -->

# Implementation

---

# Implementation

## <img src="implementation-empty.svg" style="width: 100%" />

---

<!-- page_same: true -->

# Implementation

## <img src="implementation-1.svg" style="width: 100%" />

---

# Implementation

## <img src="implementation-2.svg" style="width: 100%" />

---

# Implementation

## <img src="implementation-full.svg" style="width: 100%" />

---

<!-- page_same: false -->

# Implementation

## <img src="implementation-full-1.svg" style="width: 100%" />

---

<!-- Enige programmeertaalafhankelijke component -->

## Implementation / Agent

<br/>
<br/>
<center>
	<img src="agent-2.svg" style="width: 75%" />
</center>

---

<!-- *page_same: true -->

## Implementation / Agent

<br/>
<br/>
<center>
	<img src="agent-2.svg" style="width: 75%" />
</center>

---

# Implementation

## <img src="implementation-full-2.svg" style="width: 100%" />

---

<!-- Routeren tussen agent en predictor -->

## Implementation / Controller

<br/>
<br/>
<br/>
<center>
<img src="controller-1.svg" style="width: 75%" />
</center>

---

<!-- *page_same: true -->

<!-- De resultaten analyseren nadat tests zijn uitgevoerd -->

## Implementation / Controller

<br/>
<br/>
<br/>
<center>
<img src="controller-2.svg" style="width: 75%" />
</center>

---

# Implementation

## <img src="implementation-full-3.svg" style="width: 100%" />

---

## Implementation / Predictor

<br/>
<br/>
<center>
<img src="predictor-1.svg" style="width: 90%" />
</center>

---

<!-- *page_same: true -->

## Implementation / Predictor

<br/>
<br/>
<center>
<img src="predictor-2.svg" style="width: 90%" />
</center>

---

<!-- *page_same: true -->

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

<!-- Eigen algoritme door bestaande algoritmes te combineren. -->

## Implementation / Alpha-algorithm

&nbsp;

---

<!-- page_same: true -->

## Implementation / Alpha-algorithm

1) Unstable, affected test cases (by duration)

---

## Implementation / Alpha-algorithm

1) Unstable, affected test cases (by duration)
2) Affected test cases (by duration)

---

## Implementation / Alpha-algorithm

1) Unstable, affected test cases (by duration)
2) Affected test cases (by duration)
3) Test cases based on additional coverage

---

## Implementation / Alpha-algorithm

1) Unstable, affected test cases (by duration)
2) Affected test cases (by duration)
3) Test cases based on additional coverage
4) Other test cases

---

## Implementation / Alpha-algorithm

1) Unstable, affected test cases (by duration)
2) Affected test cases (by duration)
3) Test cases based on additional coverage
4) Other test cases <code>[redunant]</code>

---

<!-- page_same: false -->

<!-- Er is echter wel nog een probleem. Zoals gezegd zijn er in de predictor 10 algoritmes beschikbaar, met elk een eigen voorspelde volgorde. -->

## Implementation / Meta predictor

<img src="metapredictor-1.svg" style="width: 100%" />

---

<!-- page_same: true -->

<!-- Maar hoe kunnen we uit al die 10 volgordes nu bepalen wat de finale moet zijn? -->

## Implementation / Meta predictor

<img src="metapredictor-2.svg" style="width: 100%" />

---

<!-- Dit is precies waar de metapredictor voor dient. -->

## Implementation / Meta predictor

<img src="metapredictor-3.svg" style="width: 100%" />

---

<!-- Werkt door elk algoritme een score te geven per applicatie en dan degene met de hoogste te kiezen. Score wordt bijgewerkt in de feedbackfase van de controller. -->

## Implementation / Meta predictor

<img src="metapredictor-4.svg" style="width: 100%" />

---

<!-- page_same: false -->

<!-- *template: gaia -->

# Results

---

## Results

#### RQ1: Failure probability

<br/>
<img src="charts/rq1-failure-probability.svg" style="width: 100%" />

<br/>
<br/>
<center>
	11% - 19%
</center>

---

## Results

#### RQ2: Average test run duration

<img src="charts/rq2-test-run-durations.svg" style="width: 100%" />

---

## Results

#### RQ3: Consecutive failure probability

<img src="charts/rq3-consecutive-failure.svg" style="width: 100%" />

---

## Results

#### RQ4: Performance on Dodona

<img src="charts/rq4-dodona-alpha.svg" style="width: 95%" />

<br />
<br />
<center>
  <strong># test cases:</strong> < 25x | <strong>duration:</strong> < 40x
</center>

---

<!-- *template: gaia -->

# Demo

---

<!-- *template: gaia -->

# Wrapping up

---

## Conclusion

<!-- Tests zijn goed -->
<!-- De oplossing is om ze te herordenen -->
<!-- Uitvoeringstijd daalt, Productiviteit stijgt -->

<center>
	<img src="conclusion-tests-begin.svg" style="width: 50%" />
</center>

---

<!-- *page_same: true -->

## Conclusion

<!-- Maar veel tests kunnen al snel een probleem worden -->

<center>
	<img src="conclusion-tests-full.svg" style="width: 50%" />
</center>

---

## Conclusion

<!-- De oplossing is om ze te herordenen -->

<p>&nbsp;</p>
<center>
	<img src="conclusion-reorder.svg" style="width: 20%" />
  <br/>
  <strong>TCP</strong>
</center>

---

## Conclusion

<!-- Uitvoeringstijd daalt, Productiviteit stijgt -->

<p>&nbsp;</p>
<center>
	<img src="conclusion-time.svg" style="width: 80%" />
</center>

---

<!-- *template: gaia -->

# Questions?

---

## References
- Slides created using [Marp](https://marpit.marp.app/).
- Icons are property of [FontAwesome](https://fontawesome.com/).