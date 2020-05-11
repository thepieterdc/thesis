(
  SELECT gh_build_started_at, true as failed
  FROM `travistorrent`
  WHERE
    tr_build_id IN (
      SELECT DISTINCT(tr_prev_build)
      FROM `travistorrent`
      WHERE tr_log_bool_tests_ran=true AND tr_log_bool_tests_failed=true
    )
    AND gh_build_started_at IS NOT null AND tr_log_bool_tests_failed=true
) UNION ALL (
  SELECT gh_build_started_at, false as failed
  FROM `travistorrent`
  WHERE tr_build_id IN (
    SELECT DISTINCT(tr_prev_build)
    FROM `travistorrent`
    WHERE tr_log_bool_tests_ran=true AND tr_log_bool_tests_failed=false
  )
  AND gh_build_started_at IS NOT null AND tr_log_bool_tests_failed=true
)
