import os


def test_valid(cldf_dataset, cldf_logger, cldf_sqlite_database):
    #assert cldf_dataset.validate(log=cldf_logger)
    if os.environ.get('CI') == 'true':
        return
    print('Im staying')
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

