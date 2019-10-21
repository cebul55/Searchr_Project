-- DROP database searchrprojectdb;

CREATE database searchrprojectdb;

create user searchradmin with password 'aqq123!';

alter role searchradmin set client_encoding to 'utf8';
alter role searchradmin set default_transaction_isolation to 'read committed';
alter role searchradmin set timezone to 'utc';

grant all privileges on database searchrprojectdb to searchradmin;
grant all privileges on database searchrprojectdb to bartoszcybulski;

