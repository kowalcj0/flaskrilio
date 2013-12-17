drop table if exists calls;
CREATE TABLE calls (
  id integer primary key autoincrement,
  FromNo string not null,
  ToNo string not null,
  Caller string not null,
  Called string not null,
  AccountSid string not null,
  CallSid string not null,
  Direction string not null,
  CallStatus string not null,
  CallDuration integer not null,
  StartTime string null,
  EndTime string null
);
