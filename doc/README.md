
#
# FIXME: Note the typo in Fig. 3 of the original norare paper (FOREST 402 instead of 420)
#

```sql
select count(distinct variable_id) from (select f.cldf_parameterReference,uv.variable_id, count(uv.cldf_id) as c from formtable as f, `unit-values.csv` as uv where uv.cldf_formReference = f.cldf_id and f.cldf_parameterReference != 0 group by uv.Variable_ID, f.cldf_parameterReference having c > 1 order by c desc) as s;
224
```
