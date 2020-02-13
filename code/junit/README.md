# JUnit

This Gradle plugin allows JUnit4 tests to be executed in a chosen order. The order must be defined in a YAML file using the following format:
```yaml
---
order:
  - {class: ClassContainingTest, method: NameOfTestMethod}
```

Tests that are not listed will be executed in a random yet deterministic order after the listed tests.

An example is provided in the `example/` directory.