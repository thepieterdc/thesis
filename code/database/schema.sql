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
	predicted boolean default false,
	repository_id bigint not null
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
	repository_id bigint not null
		constraint tests_repositories_id_fk
			references repositories
);

alter table tests owner to velocity;

create table tests_coverage
(
	sourcefile text not null,
	from_line integer not null,
	to_line integer not null,
	test_id bigint not null
		constraint tests_coverage_tests_id_fk
			references tests,
	constraint tests_coverage_pkey
		primary key (sourcefile, from_line, to_line, test_id)
);

alter table tests_coverage owner to velocity;

create table tests_results
(
	id serial not null
		constraint tests_results_pk
			primary key,
	failed boolean not null,
	duration bigint not null,
	run_id bigint not null
		constraint tests_results_runs_id_fk
			references runs,
	test_id bigint not null
		constraint tests_results_tests_id_fk
			references tests
);

alter table tests_results owner to velocity;

create table predictors
(
	id serial not null
		constraint predictors_pk
			primary key,
	name text not null
		constraint predictors_name_key
			unique
);

alter table predictors owner to velocity;

create table predictors_scores
(
	repository_id integer not null
		constraint predictors_scores_repositories_id_fk
			references repositories,
	predictor_id integer not null
		constraint predictors_scores_predictors_id_fk
			references predictors,
	score integer default 0,
	constraint predictors_scores_pkey
		primary key (predictor_id, repository_id)
);

alter table predictors_scores owner to velocity;

create table predictions
(
	run_id integer not null
		constraint predictions_runs_id_fk
			references runs,
	predictor_id integer not null
		constraint predictions_predictors_id_fk
			references predictors,
	testorder text not null,
	selected boolean default false,
	constraint predictions_pkey
		primary key (predictor_id, run_id)
);

alter table predictions owner to velocity;


