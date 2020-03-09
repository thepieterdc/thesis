-- we don't know how to generate schema main (class Schema) :(
create table runs
(
	id integer
		constraint runs_pk
			primary key autoincrement,
	commit_hash text,
	created_at datetime default current_timestamp
);

create table orders
(
	id integer
		constraint orders_pk
			primary key autoincrement,
	testorder text,
	run_id int
		references runs
);

create table tests
(
	id integer
		constraint tests_pk
			primary key autoincrement,
	testcase text
);

create unique index tests_testcase_uindex
	on tests (testcase);

create table tests_coverage
(
	id integer
		constraint tests_coverage_pk
			primary key autoincrement,
	sourcefile text,
	from_line integer,
	to_line integer,
	test_id integer
		references tests
);

create table tests_results
(
	id integer
		constraint tests_results_pk
			primary key autoincrement,
	run_id int
		references runs,
	test_id int
		references tests,
	failed boolean
);


