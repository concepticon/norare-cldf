SELECT c.cldf_id as cid, c.cldf_name, f.cldf_languageReference, f.cldf_form, var.cldf_id, v.value FROM
  `norare.csv` as v,
  `variables.csv` as var,
  FormTable as f,
  ParameterTable as c
WHERE
  v.cldf_formReference = f.cldf_id
  AND v.Variable_ID = var.cldf_id
  AND f.cldf_parameterReference = c.cldf_id
  AND c.cldf_id IN ('420', '906', '1803', '344', '670')
  AND var.category = 'norms'
  AND var.cldf_id LIKE '%FREQUENCY_LOG'
  AND f.cldf_languageReference IN ('eng', 'deu')
ORDER BY cid
