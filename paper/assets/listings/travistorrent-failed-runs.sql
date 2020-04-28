SELECT 
  COUNTIF(tr_log_bool_tests_failed) as failed,
  COUNTIF(tr_log_bool_tests_ran) as ran,
  COUNT(1) as total
FROM `travistorrent`
