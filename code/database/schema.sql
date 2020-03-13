-- we don't know how to generate schema main (class Schema) :(
create table repositories
(
	id integer
		constraint repositories_pk
			primary key autoincrement,
	url text not null
);

create unique index repositories_url_uindex
	on repositories (url);

create table runs
(
	id integer
		constraint runs_pk
			primary key autoincrement,
	commit_hash text not null,
	created_at datetime default current_timestamp,
	repository_id int not null
		references repositories
);

create table orders
(
	id integer
		constraint orders_pk
			primary key autoincrement,
	testorder text not null,
	run_id int not null
		references runs
);

create table tests
(
	id integer
		constraint tests_pk
			primary key autoincrement,
	testcase text not null
);

create unique index tests_testcase_uindex
	on tests (testcase);

create table tests_coverage
(
	id integer
		constraint tests_coverage_pk
			primary key autoincrement,
	sourcefile text not null,
	from_line integer not null,
	to_line integer not null,
	test_id integer not null
		references tests
);

create table tests_results
(
	id integer
		constraint tests_results_pk
			primary key autoincrement,
	run_id int not null
		references runs,
	test_id int not null
		references tests,
	failed boolean not null
);
