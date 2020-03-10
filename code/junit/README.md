# JUnit

This Gradle plugin allows JUnit4 tests to be executed in a chosen order. The order must be defined in a json file using the following format:
```json
{
  "order": [
    "package.containing.test.TestClass.TestMethod",
    "package.containing.test.OtherClass.TestMethod2",
  ]
}
```

Tests that are not listed will be executed in a random yet deterministic order after the listed tests.

An example is provided in the `example/` directory.