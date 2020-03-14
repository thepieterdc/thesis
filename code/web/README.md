# analyser

## Create a test run
```shell script
./create-run ${database.db}
```

## Save test results
```shell script
cat ${results.json} | ./test-results ${run_id} ${database.db}
```

## Parse coverage results
```shell script
./parse-coverage ${database.db} ${folder_containing_xmlfiles}
```