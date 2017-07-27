DECLARE @hourspan INT = ?;
DECLARE @folderNamePattern NVARCHAR(100) = ?;
DECLARE @projectNamePattern NVARCHAR(100) = ?;
DECLARE @packageNamePattern NVARCHAR(100) = ?;
DECLARE @statusFilter INT = ?;

WITH cteLoglevel as
(
  select
    execution_id,
    cast(parameter_value as int) as logging_level
  from
    [catalog].[execution_parameter_values]
  where
    parameter_name = 'LOGGING_LEVEL'
)

    SELECT TOP 100
            e.execution_id ,
            e.folder_name ,
            e.project_name ,
            e.package_name ,
            e.project_lsn ,
            environment = isnull(e.environment_folder_name, '') + isnull('\' + e.environment_name,  ''),
            e.status ,
            start_time = FORMAT(SWITCHOFFSET(e.start_time, '-00:00'), 'yyyy-MM-dd HH:mm:ss') ,
            end_time = FORMAT(SWITCHOFFSET(e.end_time, '-00:00'), 'yyyy-MM-dd HH:mm:ss') ,
            elapsed_time_min = FORMAT(DATEDIFF(ss, e.start_time, e.end_time)
                                      / 60., '#,0.00'),
            l.logging_level
    FROM    [catalog].executions e
    left outer join cteLoglevel l on e.execution_id = l.execution_id
    WHERE   e.folder_name LIKE @folderNamePattern
            AND e.project_name LIKE @projectNamePattern
            and e.package_name LIKE @packageNamePattern
            AND e.start_time >= DATEADD(HOUR, -@hourspan, SYSDATETIME())
            AND ( e.[status] = @statusFilter OR @statusFilter = 0 )
    ORDER BY e.execution_id DESC
OPTION  ( RECOMPILE );