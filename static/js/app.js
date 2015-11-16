var SSIS_RENDER = (function(_, Morris, console) {
	'use strict';
	_.templateSettings.interpolate = /{{([\s\S]+?)}}/g;
	var STATUS_CODES = {
		0: 'all',
		1: 'created',
		2: 'running',
		3: 'cancelled',
		4: 'failed',
		5: 'pending',
		6: 'halted',
		7: 'succeeded',
		8: 'stopping',
		9: 'completed'
	};
	var COLORS = {
		0: 'default',
		1: 'default',
		2: 'info',
		3: 'danger',
		4: 'danger',
		5: 'default',
		6: 'danger',
		7: 'success',
		8: 'warning',
		9: 'default'
	};
	var GENERATOR_CODES = {
		10: ['code', 'Entry APIs, such as T-SQL and CLR Stored procedures'],
		20: ['car', 'External process used to run package (ISServerExec.exe)'],
		30: ['archive', 'Package-level objects'],
		40: ['map-signs', 'Control Flow tasks'],
		50: ['map', 'Control Flow containers'],
		60: ['exchange', 'Data Flow task']
	};
	var my = {};
	my.init_env = function(env) {
		my.ENV = env;
	};
	/*execution id - packages_list*/
	my.texecution_id = _.template(
		'<a class="execution_id" href="{{env.base_url}}/{{env.instance}}/folder/' +
		'{{row.folder_name}}/project/{{row.project_name}}/status/all/package/' +
		'{{row.package_name}}/execution/{{row.execution_id}}">' +
		' {{row.execution_id}}</a>');
	my.render_execution_id = function(data, type, row, meta) {
		return my.texecution_id({
			row: row,
			env: my.ENV
		});
	};
	/*project_name - packages_list*/
	my.tproject_name = _.template(
		'<a class="route_overview" href="{{env.base_url}}/{{env.instance}}/folder/{{row.folder_name}}/project/{{row.project_name}}/status/all">' +
		'{{row.project_name}}</a> (v.{{row.project_lsn}})' +
		'<a data-pjax href="{{env.base_url}}/../history/{{env.instance}}/folder/all/project/{{row.project_name}}/package/all"' +
		' title="View History for this project" class="pull-right"><i class="fa fa-area-chart"></i></a>');
	my.render_project_name = function(data, type, row, meta) {
		return my.tproject_name({
			row: row,
			env: my.ENV
		});
	};
	/*package_name - packages_list*/
	my.tpackage_name = _.template(
		'<a class="route_overview" href="{{env.base_url}}/{{env.instance}}/folder/{{row.folder_name}}/project/{{row.project_name}}/status/all' +
		'/package/{{row.package_name}}">{{row.package_name}}</a><a data-pjax href="{{env.base_url}}/../history/{{env.instance}}/' +
		'folder/all/project/all/package/{{row.package_name}}" title="View History for this package" class="pull-right">' +
		'<i class="fa fa-area-chart"></i></a>');

	my.render_package_name = function(data, type, row, meta) {
		return my.tpackage_name({
			row: row,
			env: my.ENV
		});
	};

	my.tstatus = _.template(
		'<a class="execution_id" href="{{env.base_url}}/{{env.instance}}/folder/' +
		'{{row.folder_name}}/project/{{row.project_name}}/status/all/package/' +
		'{{row.package_name}}/execution/{{row.execution_id}}">' +
		'<span class="label label-{{color}}">{{status}}</span></a>');

	var format_status = function(status) {
		return '<span class="label label-' + COLORS[status] + '">' + STATUS_CODES[status] + '</span>';
	};

	my.render_status = function(data, type, row, meta) {
		return my.tstatus({
			row: row,
			env: my.ENV,
			color: COLORS[row.status],
			status: STATUS_CODES[row.status]
		});
	};

	my.render_tcaption = function() {
		var rtn = '';
		rtn += my.ENV.package_name !== 'all' ? 'Package ' + decodeURIComponent(my.ENV.package_name) : 'All Packages';
		rtn += my.ENV.folder !== 'all' ? ' in "' + decodeURIComponent(my.ENV.folder) + '"' : '';
		rtn += my.ENV.project !== 'all' ? ' for "' + decodeURIComponent(my.ENV.project) + '"' : '';
		rtn += my.ENV.status != 'all' ? ' , status ' + decodeURIComponent(my.ENV.status) + '' : '';
		return rtn;
	};

	var format_message_source_type = function(message_source_type) {
		var icon = GENERATOR_CODES[message_source_type][0];
		var text = GENERATOR_CODES[message_source_type][1];
		return '<i class="fa fa-' + icon + '" title="' + text + '"></i>';
	};

	my.render_message_source_type = function(data, type, row, meta) {
		return format_message_source_type(data);
	};

	/*history package name*/
	my.thistory_project_name = _.template(
		'{{row.project_name}}</a> (v.{{row.project_lsn}})');
	my.render_history_project_name = function(data, type, row, meta) {
		return my.thistory_project_name({
			row: row
		});
	};

	/*history status*/
	my.render_history_status = function(data, type, row, meta) {
		var rtn = '';
		rtn += my.render_status(data, type, row, meta);
		if (row.has_expected_values) {
			rtn += '<span class="label label-warning">' + row.percent_complete + '% Estimate)</span>';
		}
		return rtn;
	};

	/*history start_time*/
	my.render_history_start_time = function(data, type, row, meta) {
		var rtn = row.start_time;
		if (row.has_expected_values) {
			rtn += '<span class="label label-warning">Estimate</span>';
		}
		return rtn;
	};

	/*history stop_time*/
	my.render_history_end_time = function(data, type, row, meta) {
		var rtn = row.end_time;
		if (row.has_expected_values) {
			rtn += '<span class="label label-warning">Estimate</span>';
		}
		return rtn;
	};

	/*history graph helper*/
	my.massage_data_for_graph = function(data) {
		var ykeys = ['elapsed_time_min', 'avg_elapsed_time_min'];
		var ylabels = ['Elapsed Time (Min)', 'Average Time (Min)'];
		var genykeys = {};
		var _newdata = [];
		_.forEach(data, function(row) {
			var key = row.project_name + '\\' + row.package_name;
			var newrow = {};
			_.forEach(ykeys, function(ykey, n) {
				var _key = key + '\\' + ykey;
				newrow[_key] = row[ykey];
				if (!_.has(genykeys, _key)) genykeys[_key] = ylabels[n];
			});
			_.extend(newrow, row);
			newrow.key = key;
			_newdata.push(newrow);
		});
		return [_newdata, genykeys];
	};

	my.init_graph = function(data, element) {
		var grdata = my.massage_data_for_graph(data);
		var graph = new Morris.Line({
			element: element,
			data: grdata[0],
			xkey: 'start_time',
			ykeys: _.keys(grdata[1]),
			labels: _.values(grdata[1]),
			hideHoverNull: true,
			hoverCallback: function(index, options, content, row) {
				var rtn = '<div class="morris-hover-row-label">' + _.escape(row.project_name + '\\' + row.package_name) + '</div>';
				if (!_.isNull(row.environment)) {
					rtn += '<div class="morris-hover-row-label"> Env: ' + _.escape(row.environment) + '</div>';
				}
				rtn += content + '<div class="morris-hover-row-label">' + format_status(row.status) + '</div>';
				return rtn;
			},
			resize: true
		});
	};

	return my;
}(_, Morris, console));


var SSIS_ROUTER = (function(_, crossroads, console, $) {
	'use strict';
	var my = {};
	var BASE_ENV = {
		'folder': 'all',
		'project': 'all',
		'package_name': 'all',
		'execution': 'all',
		'status': 'all',
	};

	my.init_env = function(env) {
		my.ENV = _.extend(env, BASE_ENV);
	};


	var overviewRouter = crossroads.create();

	overviewRouter.addRoute('/:instance:',
		function(instance) {
			console.log('1');
			my.ENV.instance = instance;
			my.ENV.folder = 'all';
			my.ENV.project = 'all';
			my.ENV.status = 'all';
			my.ENV.package_name = 'all';
			my.ENV.execution = 'all';
		}
	);
	overviewRouter.addRoute('/:instance:/folder/:folder:',
		function(instance, folder) {
			console.log('2');
			my.ENV.instance = instance;
			my.ENV.folder = folder;
			my.ENV.project = 'all';
			my.ENV.status = 'all';
			my.ENV.package_name = 'all';
			my.ENV.execution = 'all';
		}
	);
	overviewRouter.addRoute('/:instance:/folder/:folder:/project/:project:',
		function(instance, folder, project) {
			console.log('3');
			my.ENV.instance = instance;
			my.ENV.folder = folder;
			my.ENV.project = project;
			my.ENV.status = 'all';
			my.ENV.package_name = 'all';
			my.ENV.execution = 'all';
		}
	);
	overviewRouter.addRoute('/:instance:/folder/:folder:/project/:project:/status/:status:',
		function(instance, folder, project, status) {
			console.log('4');
			my.ENV.instance = instance;
			my.ENV.folder = folder;
			my.ENV.project = project;
			my.ENV.status = status;
			my.ENV.package_name = 'all';
			my.ENV.execution = 'all';
		}
	);
	overviewRouter.addRoute('/:instance:/folder/:folder:/project/:project:/status/:status:/package/:package_name:',
		function(instance, folder, project, status, package_name) {
			console.log('5');
			my.ENV.instance = instance;
			my.ENV.folder = folder;
			my.ENV.project = project;
			my.ENV.status = status;
			my.ENV.package_name = package_name;
			my.ENV.execution = 'all';
		}
	);
	overviewRouter.addRoute('/:instance:/folder/:folder:/project/:project:/status/:status:/package/:package_name:/execution/:execution:',
		function(instance, folder, project, status, package_name, execution) {
			console.log('6');
			my.ENV.instance = instance;
			my.ENV.folder = folder;
			my.ENV.project = project;
			my.ENV.status = status;
			my.ENV.package_name = package_name;
			my.ENV.execution = execution;
		}
	);
	overviewRouter.addRoute('/:instance:/folder/:folder:/project/:project:/status/:status:/package/:package_name:/execution/:execution:/:event_name:',
		function(instance, folder, project, status, package_name, execution, event_name) {
			console.log('7');
			my.ENV.instance = instance;
			my.ENV.folder = folder;
			my.ENV.project = project;
			my.ENV.status = status;
			my.ENV.package_name = package_name;
			my.ENV.execution = execution;
			my.ENV.event_name = event_name;
		}
	);

	overviewRouter.addRoute('/:instance:/:execution:/details/:event_name:',
		function(instance, execution, event_name) {
			console.log('8');
			my.ENV.instance = instance;
			my.ENV.execution = execution;
			my.ENV.event_name = event_name;
		}
	);

	overviewRouter.addRoute('/:instance:/folder/:folder:/project/:project:/package/:package_name:',
		function(instance, folder, project, package_name) {
			console.log('9');
			my.ENV.instance = instance;
			my.ENV.folder = folder;
			my.ENV.project = project;
			my.ENV.package_name = package_name;
		}
	);

	overviewRouter.routed.add(function(bla) {
		if (my.ENV.execution == 'all') {
			$('#children').addClass('hidden');
			$('#executables').addClass('hidden');
			$('#messages').addClass('hidden');
		} else {
			$('#children').removeClass('hidden').addClass('show');
			$('#executables').removeClass('hidden').addClass('show');
			$('#messages').removeClass('hidden').addClass('show');
		}
		if ((my.ENV.package_name == 'all') && (my.ENV.execution == 'all')) {
			$('#package_kpi').addClass('hidden');
		} else {
			$('#package_kpi').removeClass('hidden').addClass('show');
		}
	});

	overviewRouter.bypassed.add(function(bla) {
		console.log('bypassed', bla);
	});

	my.parse_env = function(currenturl) {
		var parameters = currenturl.replace(my.ENV.base_url, '');
		overviewRouter.parse(parameters);
	};

	my.rebase_url = function(url_to_rebase) {
		return my.ENV.base_url + '/' + url_to_rebase;
	};

	var resourceRouter = crossroads.create();

	my.restFolderURL = resourceRouter.addRoute('../../rest_data/folders/:instance:');
	my.restEngineKpiURL = resourceRouter.addRoute('../../rest_data/engine_kpi/:instance:/folder/:folder:/project/:project:/package/:package_name:');
	my.restPackageKpiURL = resourceRouter.addRoute('../../rest_data/package_kpi/:instance:/folder/:folder:/project/:project:/package/:package_name:/execution/:execution:');
	my.restPackageListURL = resourceRouter.addRoute('../../rest_data/package_list/:instance:/folder/:folder:/project/:project:/status/:status:/package/:package_name:');
	my.restPackageChildrenURL = resourceRouter.addRoute('../../rest_data/package_children/:instance:/execution/:execution:');
	my.restPackageExecutablesURL = resourceRouter.addRoute('../../rest_data/package_executables/:instance:/execution/:execution:');
	my.restPackageDetailsURL = resourceRouter.addRoute('../../rest_data/package_details/:instance:/execution/:execution:');
	my.restPackageInfoURL = resourceRouter.addRoute('../../rest_data/package_info/:instance:/execution/:execution:');
	my.restPackageHistoryURL = resourceRouter.addRoute('../../rest_data/package_history/:instance:/folder/:folder:/project/:project:/package/:package_name:');

	my.feedURL = resourceRouter.addRoute('../../console/rssfeed/:instance:/folder/:folder:/project/:project:/status/:status:/package/:package_name:');

	my.restUrlFor = function(what) {
		var mapper = {
			'folders': my.restFolderURL.interpolate(my.ENV),
			'enginekpi': my.restEngineKpiURL.interpolate(my.ENV),
			'packagekpi': my.restPackageKpiURL.interpolate(my.ENV),
			'packagelist': my.restPackageListURL.interpolate(my.ENV),
			'packagechildren': my.restPackageChildrenURL.interpolate(my.ENV),
			'packageexecutables': my.restPackageExecutablesURL.interpolate(my.ENV),
			'packagedetails': my.restPackageDetailsURL.interpolate(my.ENV),
			'packageinfo': my.restPackageInfoURL.interpolate(my.ENV),
			'packagehistory': my.restPackageHistoryURL.interpolate(my.ENV),
			'rss_feed' : my.feedURL.interpolate(my.ENV)
		};
		return my.rebase_url(mapper[what]);
	};

	my.overviewRouter = overviewRouter;

	return my;

}(_, crossroads, console, $));


var SSIS_TABLES = (function(_, SSIS_RENDER, console, $) {
	'use strict';
	var my = {};
	$.extend($.fn.dataTable.defaults, {
		'dom': '<"row"<"col-sm-3"B><"col-sm-5"l><"col-sm-4"f>><"row"<"col-sm-12"tr>><"row"<"col-sm-7"p><"col-sm-5"i>>',
		'lengthMenu': [
			[10, 25, 50, -1],
			[10, 25, 50, 'All']
		],
		'autoWidth': false,
		'responsive': true,
		'language': {
			'loadingRecords': '<i class="fa fa-refresh fa-spin"></i>'
		},
		'retrieve': true
	});
	my.dt_details = {
		'order': [],
		buttons: [
			'colvis', 'copy', 'excel'
		],
		columns: [{
			title: 'Message Time',
			data: 'message_time',
			className: 'text-nowrap'
		}, {
			title: 'Message',
			data: 'message'
		}, {
			title: 'Package',
			data: 'package_name'
		}, {
			title: 'Package Path',
			data: 'package_path'
		}, {
			title: 'Subcomponent Name',
			data: 'subcomponent_name'
		}, {
			title: 'Execution Path',
			data: 'execution_path'
		}],
	};

	my.dt_history = {
		'order': [],
		buttons: [
			'colvis', 'copy', 'excel'
		],
		columns: [{
			title: '#',
			data: 'execution_id'
		}, {
			title: 'Project',
			data: 'project_name',
			render: SSIS_RENDER.render_history_project_name
		}, {
			title: 'Package',
			data: 'package_name'
		}, {
			title: 'Status',
			data: 'status',
			render: SSIS_RENDER.render_history_status
		}, {
			title: 'Environment',
			data: 'environment'
		}, {
			title: 'Start Time',
			data: 'start_time',
			render: SSIS_RENDER.render_history_start_time
		}, {
			title: 'Stop Time',
			data: 'end_time',
			render: SSIS_RENDER.render_history_end_time
		}, {
			title: 'Elapsed (Min)',
			data: 'elapsed_time_min',
			className: 'text-nowrap text-right'
		}, ]
	};

	my.dt_packages = {
		'order': [],
		buttons: [
			'colvis', 'copy', 'excel'
		],
		columns: [{
			title: '#',
			data: 'execution_id',
			render: SSIS_RENDER.render_execution_id
		}, {
			title: 'Project',
			data: 'project_name',
			render: SSIS_RENDER.render_project_name
		}, {
			title: 'Package',
			data: 'package_name',
			render: SSIS_RENDER.render_package_name
		}, {
			title: 'Status',
			data: 'status',
			render: SSIS_RENDER.render_status
		}, {
			title: 'Start Time',
			data: 'start_time'
		}, {
			title: 'End Time',
			data: 'end_time'
		}, {
			title: 'Elapsed (Min)',
			data: 'elapsed_time_min',
			className: 'text-nowrap text-right'
		}, {
			title: 'Warnings',
			data: 'warnings',
			className: 'text-nowrap text-right'
		}, {
			title: 'Errors',
			data: 'errors',
			className: 'text-nowrap text-right'
		}],
		createdRow: function(row, data, dataIndex) {
			if (data.execution_id == ENV.execution) {
				$(row).addClass('info');
			}
		},
		drawCallback: function(settings) {
			$('#datatable_packages_caption').html(SSIS_RENDER.render_tcaption());
		}
	};

	my.dt_children = {
		'order': [],
		'buttons' : [
			'colvis', 'copy', 'excel'
		],
		columns: [{
			title: '#',
			data: 'event_message_id'
		}, {
			title: 'Generator',
			data: 'message_source_type',
			render: SSIS_RENDER.render_message_source_type,
			className: 'text-center'
		}, {
			title: 'Package',
			data: 'package_name'
		}, {
			title: 'Source',
			data: 'message_source_name'
		}, {
			title: 'Execution Path',
			data: 'execution_path'
		}, {
			title: 'Start Time',
			data: 'pre_message_time',
			className: 'text-nowrap'
		}, {
			title: 'Stop Time',
			data: 'post_message_time',
			className: 'text-nowrap'
		}, {
			title: 'Elapsed (Min)',
			data: 'elapsed_time_min',
			className: 'text-nowrap text-right'
		}, ]
	};

	my.dt_executables = {
		'order': [],
		buttons: [
			'colvis', 'copy', 'excel'
		],
		columns: [{
			title: '#',
			data: 'event_message_id'
		}, {
			title: 'Generator',
			data: 'message_source_type',
			render: SSIS_RENDER.render_message_source_type,
			className: 'text-center'
		}, {
			title: 'Package',
			data: 'package_name'
		}, {
			title: 'Source',
			data: 'message_source_name'
		}, {
			title: 'Execution Path',
			data: 'execution_path'
		}, {
			title: 'Start Time',
			data: 'pre_message_time',
			className: 'text-nowrap'
		}, {
			title: 'Stop Time',
			data: 'post_message_time',
			className: 'text-nowrap'
		}, {
			title: 'Elapsed (Min)',
			data: 'elapsed_time_min',
			className: 'text-nowrap text-right'
		}, ]
	};

	my.fill_table = function(dt, data) {
		dt.clear();
		dt.rows.add(data);
		dt.columns.adjust().responsive.recalc().draw();
		$(dt.table().container()).closest('.box').css('height', '').find('.overlay').addClass('hidden');
	};

	my.fill_table_adv = function(dt, pro) {
		$(dt.table().container()).closest('.box').find('.overlay').removeClass('hidden');
		dt.clear();
		pro.done(function(data) {
			dt.rows.add(data);
			dt.columns.adjust().draw(); //.responsive.recalc().draw();
			$(dt.table().container()).closest('.box').css('height', '').find('.overlay').addClass('hidden');
		});
	};

	my.slice_details = function(data, event_type) {
		var newdata = [];
		switch (event_type) {
			case 'warnings':
				newdata = _.filter(data, function(element) {
					return (element.event_name == 'OnWarning');
				});
				break;
			case 'memory_warnings':
				newdata = _.filter(data, function(element) {
					return (element.event_name == 'OnInformation' && element.message.indexOf('memory allocation') > -1);
				});
				break;
			case 'errors':
				newdata = _.filter(data, function(element) {
					return (element.event_name == 'OnError');
				});
				break;
			case 'duplicate':
				newdata = _.filter(data, function(element) {
					return (element.event_name == 'OnWarning' && element.message.indexOf('duplicate') > -1);
				});
				break;
			default:
				newdata = data;
		}
		return newdata;
	};

	return my;

}(_, SSIS_RENDER, console, $));