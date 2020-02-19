# JUnit example

This example illustrates the junit-reorder library. The order is specified in `src/test/resources/order.yaml` and the used order is printed upon execution of the `velocity` target.

```shell script
(cd ../ && ./gradlew jar publishToMavenLocal) && ./gradlew velocity --rerun-tasks --stacktrace
```

```text
io.github.thepieterdc.thesis.junitreorder.example.FirstTest > testHello STANDARD_OUT
    Test: FirstTest#testHello

io.github.thepieterdc.thesis.junitreorder.example.SecondTest > testWorld STANDARD_OUT
    Test: SecondTest#testWorld

io.github.thepieterdc.thesis.junitreorder.example.SecondTest > testLoremIpsum STANDARD_OUT
    Test: SecondTest#testLoremIpsum

io.github.thepieterdc.thesis.junitreorder.example.FirstTest > testFoo STANDARD_OUT
    Test: FirstTest#testFoo

io.github.thepieterdc.thesis.junitreorder.example.SecondTest > testBar STANDARD_OUT
    Test: SecondTest#testBar
```