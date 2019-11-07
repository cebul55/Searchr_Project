-- DROP database searchrprojectdb;
-- -- Get pid of connections
-- SELECT pg_terminate_backend(pg_stat_activity.pid)
-- FROM pg_stat_activity
-- WHERE pg_stat_activity.datname = 'searchrprojectdb'
--   AND pid <> pg_backend_pid();

CREATE database searchrprojectdb;

create user searchradmin with password 'aqq123!';

alter role searchradmin set client_encoding to 'utf8';
alter role searchradmin set default_transaction_isolation to 'read committed';
alter role searchradmin set timezone to 'utc';

grant all privileges on database searchrprojectdb to searchradmin;
grant all privileges on database searchrprojectdb to bartoszcybulski;

