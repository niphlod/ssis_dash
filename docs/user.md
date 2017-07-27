
# User's guide
 * [Intro](#intro)
   * [overview](#overview-page)
   * [history](#history-page)
 * [URLs](#urls)
   * [overview](#overview)
   * [history](#history)

# Intro
The dashboard leverages [yorek's](https://github.com/yorek/) idea to provide
an overall insight about a SSISDB instance. Much of the initial structure is
retained and several of the original queries are used untouched.
The app is structured into 2 "points of view":

 - overview (aka "operational")
 - history (aka "analysis")

## overview page
The overview page is the "home page" for every SSISDB instance

```
+----------------------------------------------+
|             main section                     |
|  +-----+   +------------------------------+  |
|  |  s  |   |         engine kpi           |  |
|  |  i  |   +------------------------------+  |
|  |  d  |                                     |
|  |  e  |                                     |
|  |  b  |   +------------------------------+  |
|  |  a  |   |                              |  |
|  |  r  |   |                              |  |
|  +-----+   |       package list           |  |
|            |                              |  |
|            |                              |  |
|            +------------------------------+  |
|----------------------------------------------|
|            detail section                    |
|            +------------------------------+  |
|            |     package kpi              |  |
|            +------------------------------+  |
|                                              |
|            +------------------------------+  |
|            |      messages                |  |
|            +------------------------------+  |
|                                              |
|            +------------------------------+  |
|            |      children                |  |
|            +------------------------------+  |
|                                              |
|            +------------------------------+  |
|            |      executables             |  |
|            +------------------------------+  |
|                                              |
|            +------------------------------+  |
|            |      config                  |  |
|            +------------------------------+  |
+----------------------------------------------+
```
Once accessed, the overview will show only the **main section**.

`engine kpi` report counts for each state. You can click
to filter the package list for that status.
Optionally you can use **shift+first letter** to automatically filter
using the status (e.g. `shift+f` filters all **f**ailed executions)

`sidebar` has folder and projects. You can type a folder name to filter
among your folders. Clicking on the project will filter the package list
accordingly.

`package list` has the most useful links.
At the top-left corner you can access the rss feed (useful for constant monitoring)
of the current **filtered** package list.

**NB:** only the top 100 records will be fetched from SSISDB.

Clicking on the first column (or the status column) will enable the `detail section`
to be shown for that execution.
The `detail section` will show errors and warning counters for that execution
(`package kpi`). This block is shown also if you click on the `package` column.

Every specific execution will show `messages`, `children` packages, `executables` and `configuaration`.

Clicking on the <a><i class="fa fa-area-chart"></i></a> element next to project
or package name will redirect to the [history](#history-page) point of view.

## history page
The `history` page shows a graph for the last 25 executions plus a table
reporting executions and their duration (with an estimate for running packages)

```
+----------------------------------------------+
|                                              |
|  +-----+   +------------------------------+  |
|  |  s  |   |         graph                |  |
|  |  i  |   |                              |  |
|  |  d  |   |                              |  |
|  |  e  |   +------------------------------+  |
|  |  b  |                                     |
|  |  a  |   +------------------------------+  |
|  |  r  |   |                              |  |
|  +-----+   |       details                |  |
|            |                              |  |
|            |                              |  |
|            |                              |  |
|            |                              |  |
|            +------------------------------+  |
+----------------------------------------------+
```


# URLs
The app tries to have as much clean urls as possible.
It's safe to pass around urls to your coworkers, as the URL has every information
needed to build the dashboard page.


Given a base index page residing at

/appname/default/index

## overview

The **overview** of a particular instance is on

/appname/console/overview/instance_name

You can filter for any execution relative to folder **foo** at

/appname/console/overview/instance_name/`folder`/**foo**

You can drill down to a project named **bar**

/appname/console/overview/instance_name/folder/foo/`project`/**bar**

show only the **failed** status

/appname/console/overview/instance_name/folder/foo/project/bar/`status`/**failed**

(**failed** can actually also be one of **running,cancelled,failed,halted,succeeded**)

and the package **baz**

/appname/console/overview/instance_name/folder/foo/project/bar/status/failed/`package`/**baz**

or, link to a specific execution **1109**

/appname/console/overview/instance_name/folder/foo/project/bar/status/failed/package/baz/`execution`/**1109**

and, even, filter messages by **type**

/appname/console/overview/instance_name/folder/foo/project/bar/status/failed/package/baz/execution/1109/**errors**

(**errors** can actually also be one of **warnings,duplicate_warnings,memory_warnings**)


**NB:** the `all` "placeholder" can be used to avoid filtering, such as
"every project named **dwh**, whichever the folder"
will be reachable at

/appname/console/overview/instance_name/folder/`all`/project/**dwh**

You can use the `*` character in folder, project and package names to allow
and even more flexible shorcut to a given package list.

## history

The *history* of the last 25 executions on a particular instance is on

/appname/console/history/instance_name

You can use the same rules for the *overview* pages to restrict the context,
in regards of folder, project and package names


