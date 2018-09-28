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


**_Models_** :
1. User (storing basic info of user)
2. Items (storig items related info)
3. Variants (storing variant related info)
4. ItemsEdited (stores the info of all edits/updates made on items with the user id and timestamp at which edit been made)
5. VariantEdited (works same as ItemsEdited)
6. VariantProperties (storing variant's properties info)

# Model relationships explained

1. User - Items (OneToMany)
2. User - Variants (OneToMany)
3. Items - Variants (OneToMany)
4. Variant - VariantProperties (OneToMany)
