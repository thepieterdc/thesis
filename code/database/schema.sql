create table repositories
(
	id serial not null
		constraint repositories_pk
			primary key,
	url text not null
);

alter table repositories owner to velocity;

create unique index repositories_url_uindex
	on repositories (url);

create table runs
(
	id serial not null
		constraint runs_pk
			primary key,
	commit_hash text not null,
	testorder text,
	base_path text not null,
	repository_id integer
		constraint runs_repositories_id_fk
			references repositories,
	created_at timestamp default now() not null
);

alter table runs owner to velocity;

create table tests
(
	id serial not null
		constraint tests_pk
			primary key,
	testcase text not null,
	repository_id integer not null
		constraint tests_repositories_id_fk
			references repositories
);

alter table tests owner to velocity;

create table tests_coverage
(
	id serial not null
		constraint tests_coverage_pk
			primary key,
	sourcefile text not null,
	from_line integer not null,
	to_line integer not null,
	test_id integer not null
		constraint tests_coverage_tests_id_fk
			references tests
);

alter table tests_coverage owner to velocity;

create table tests_results
(
	id serial not null
		constraint tests_results_pk
			primary key,
	failed boolean not null,
	run_id integer
		constraint tests_results_runs_id_fk
			references runs,
	test_id integer
		constraint tests_results_tests_id_fk
			references tests
);

alter table tests_results owner to velocity;
