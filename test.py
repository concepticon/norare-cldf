import os

from pycldf import Database


def test_valid(cldf_dataset, cldf_logger, tmp_path):
    assert cldf_dataset.validate(log=cldf_logger)
    if os.environ.get('CI') == 'true':
        return
    print('Im staying')
    db = Database(cldf_dataset, fname=tmp_path / 'norare.sqlite')
    db.write_from_tg()
    # Make sure all variables have associated datapoints:
    res = db.query("""
SELECT
  EXISTS(
    SELECT variable_id, COUNT(cldf_id) AS dp
    FROM `norare.csv`
    GROUP BY variable_id
    HAVING dp = 0
  )
""")
    assert res[0][0] == 0

