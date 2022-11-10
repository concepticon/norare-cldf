import os


def test_valid(cldf_dataset, cldf_logger, cldf_sqlite_database):
    assert cldf_dataset.validate(log=cldf_logger)
    if os.environ.get('CI') == 'true':
        return
    # Make sure all variables have associated datapoints:
    res = cldf_sqlite_database.query("""
SELECT
  EXISTS(
    SELECT variable_id, COUNT(cldf_id) AS dp
    FROM `norare.csv`
    GROUP BY variable_id
    HAVING dp = 0
  )
""")
    assert res[0][0] == 0
    res = cldf_sqlite_database.query("""
SELECT
  v.cldf_id, count(distinct n.value) AS c
FROM
  `variables.csv` AS v, `norare.csv` AS n
WHERE
  n.variable_id = v.cldf_id
GROUP BY v.cldf_id HAVING c = 1
""")
    assert not res

