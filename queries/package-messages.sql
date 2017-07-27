DECLARE @hourspan INT = ?;
DECLARE @folderNamePattern NVARCHAR(100) = ?;
DECLARE @projectNamePattern NVARCHAR(100) = ?;
DECLARE @packageNamePattern NVARCHAR(100) = ?;
DECLARE @statusFilter INT = ?;


with CTEex as (
SELECT TOP 100
            e.execution_id
    FROM    [catalog].executions e
    WHERE   e.folder_name LIKE @folderNamePattern
            AND e.project_name LIKE @projectNamePattern
            AND e.package_name LIKE @packageNamePattern
            AND e.start_time >= DATEADD(HOUR, -@hourspan, SYSDATETIME())
            AND ( e.[status] = @statusFilter
                  OR @statusFilter = 0
                )
    ORDER BY e.execution_id DESC
)

SELECT
	   operation_id,
	   FORMAT(SWITCHOFFSET(message_time, '-00:00'), 'yyyy-MM-dd HH:mm:ss') AS message_time ,
	   [message] ,
	   package_name ,
	   package_path ,
	   subcomponent_name ,
	   execution_path ,
	   event_name
FROM    [catalog].event_messages e
inner join CTEex on CTEex.execution_id = e.operation_id
WHERE   (
        event_name =  'OnWarning' OR event_name = 'OnError'
        )

