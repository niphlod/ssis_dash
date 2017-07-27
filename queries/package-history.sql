DECLARE @folderNamePattern NVARCHAR(100) = ?;
DECLARE @projectNamePattern NVARCHAR(100) = ?;
DECLARE @packageNamePattern NVARCHAR(100) = ?;

WITH cte
AS (
	SELECT TOP (25) e.execution_id
		,e.project_name
		,e.package_name
		,e.project_lsn
		,e.[status]
		,e.start_time
		,e.end_time
		,environment = COALESCE(e.environment_folder_name, '.\') + e.environment_name
		,elapsed_time_min = datediff(ss, e.start_time, e.end_time) / 60.
		,avg_elapsed_time_min = avg(datediff(ss, e.start_time, e.end_time) / 60.) OVER (
			PARTITION BY e.project_name
			,e.package_name ORDER BY e.start_time ROWS BETWEEN 5 PRECEDING
					AND CURRENT ROW
			)
	FROM CATALOG.executions e
	WHERE e.STATUS IN (
			2
			,7
			)
		AND e.folder_name LIKE @folderNamePattern
		AND e.package_name LIKE @packageNamePattern
		AND e.project_name LIKE @projectNamePattern
	ORDER BY e.execution_id DESC
	)
SELECT execution_id
	,project_name
	,package_name
	,project_lsn
	,environment
	,[status]
	,start_time = FORMAT(SWITCHOFFSET(start_time, '-00:00'),'yyyy-MM-dd HH:mm:ss')
	,end_time = FORMAT(CASE
			WHEN end_time IS NULL
				THEN SWITCHOFFSET(DATEADD(minute, cast(CEILING(avg_elapsed_time_min) AS INT), start_time),  '-00:00')
 			ELSE SWITCHOFFSET(end_time, '-00:00')
			END, 'yyyy-MM-dd HH:mm:ss')
	,elapsed_time_min = FORMAT(CASE
			WHEN end_time IS NULL
				THEN avg_elapsed_time_min
			ELSE elapsed_time_min
			END, '#,0.00')
	,avg_elapsed_time_min = FORMAT(avg_elapsed_time_min, '#,0.00')
	,percent_complete = FORMAT(100 * (DATEDIFF(ss, start_time, SYSDATETIMEOFFSET()) / 60.) / avg_elapsed_time_min, '#,0.00')
	,has_expected_values = CASE
		WHEN end_time IS NULL
			THEN 1
		ELSE 0
		END
FROM cte
ORDER BY execution_id DESC

