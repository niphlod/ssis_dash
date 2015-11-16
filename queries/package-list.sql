DECLARE @hourspan INT = ?;
DECLARE @folderNamePattern NVARCHAR(100) = ?;
DECLARE @projectNamePattern NVARCHAR(100) = ?;
DECLARE @packageNamePattern NVARCHAR(100) = ?;
DECLARE @statusFilter INT = ?;

WITH    cteWE
          AS ( SELECT   operation_id ,
                        event_name ,
                        event_count = COUNT(*)
               FROM     [catalog].event_messages
               WHERE    event_name IN ( 'OnError', 'OnWarning' )
               GROUP BY operation_id ,
                        event_name
             ),
        cteKPI
          AS ( SELECT   operation_id ,
                        [errors] = OnError ,
                        warnings = OnWarning
               FROM     cteWE PIVOT
        ( SUM(event_count) FOR event_name IN ( OnError, OnWarning ) ) p
             )
    SELECT TOP 100
            e.execution_id ,
            e.folder_name ,
            e.project_name ,
            e.package_name ,
            e.project_lsn ,
            e.status ,
            start_time = FORMAT(e.start_time, 'yyyy-MM-dd HH:mm:ss') ,
            end_time = FORMAT(e.end_time, 'yyyy-MM-dd HH:mm:ss') ,
            elapsed_time_min = FORMAT(DATEDIFF(ss, e.start_time, e.end_time)
                                      / 60., '#,0.00') ,
            k.warnings ,
            k.errors
    FROM    [catalog].executions e
            LEFT OUTER JOIN cteKPI k ON e.execution_id = k.operation_id
    WHERE   e.folder_name LIKE @folderNamePattern
            AND e.project_name LIKE @projectNamePattern
            and e.package_name LIKE @packageNamePattern
            AND e.start_time >= DATEADD(HOUR, -@hourspan, SYSDATETIME())
            AND ( e.[status] = @statusFilter
                  OR @statusFilter = 0
                )
    ORDER BY e.execution_id DESC
OPTION  ( RECOMPILE );