# UserActivityFeedEndPoint
### This is an API endpoint developed in python/flask which loggs user activities on POS system.
### _Tech stack used_
```
- python/flask, mysql
- SQLalchemy (ORM)
```
**_Arguments to endpoint_** :

1. User ID, Time range
```
- I am assuming time range as a single digit representing number of hours.
- The time at which endpoint is called, it loggs user activities for past (time_range) hours.
- If user id is not given then it loggs all user activities for past (time_range) hours.
```
