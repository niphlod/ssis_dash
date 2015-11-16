SELECT f.folder_id
	,f.[name] AS folder_name
	,p.project_id
	,p.[name] AS project_name
	,p.[description]
FROM [catalog].projects p
INNER JOIN [catalog].folders f
	ON p.folder_id = f.folder_id
ORDER BY f.[name], f.folder_id, p.[name], p.project_id
