# CS 586: Homework 1

### Eric Stevens
### January 11, 2020

## Part 1

### 1) 

**agent**(<u>agent_id</u>, first, middle, last, address, city, country, salary, clearance_id)
- agent(clearance_id) --> securityclearance(sc_id)

**skill**(<u>skill_id</u>, skill)

**skillrel**(<u>skill_id, agent_id</u>)
- skillrel(skill_id) --> skill(skill_id)
- skillrel(agent_id) --> agent(agent_id)

**mission**(<u>mission_id</u>, name, access_id, team_id, mission_status)
- mission(access_id) --> securityclearance(sc_id)
- mission(team_id) --> team(team_id)

**securityclearance**(<u>sc_id</u>, sc_level, description)

### 2a) 
**Question:** Can two languages have the same name?

**Answer:** Yes, since the primary key is `lang_id` the `language` attribute can have repeats (the cardinality of  `spy.language` is not that of the `spy.language.language`. Currently, however, there are no repeats in the table.

### 2b) 
**Question:** How many languages can an agent speak?

**Answer:** Using the table `spy.languagerel` we can see that an agent can speak as many languages as cardinality of the `spy.language` table. Currently this number is 20 languages.

### 2c) 
**Question:** How many security clearance levels can an agent have?

**Answer:** This is a bit of a tricky question. If we assume that each agent can only have a single `agent_id` then we can say that each agent can only have a single clearance. However, because `agent_id` is the primary key it is possible that the same person could be assigned multiple `agent_id`s and could therefore be assigned multible clearances.

### 2d) 
**Question:** How many agents can have a given skill?

**Answer:** The `skillrel` primary key is the joint attributes `(skill_id, agent_id)`. There is no limit to the number of agents that a skill can be assigned to. The only limit to the number of agents that can have a given skill is the cardinality of the `agent` table.

### 2e) 
**Question:** How many teams can participate in any given mission?

**Answer:** In the `mission` table, `mission_id` is the primary key and is associated with a `team_id`. Therefore, only a single team can be associated with any `mission_id`.

### 2f)
**Question:** Can two agents have different affiliation strengths to the same organization?

**Answer:** The question is unclear since the term *organization* does not appear in any of the relevant tables. `aff_id` is the primary key of the `affiliation` table while the combined `(aff_id, agent_id)` is the primary key of `affiliationrel`. Lets assume that *organization* has a one-to-one mapping with `aff_id`. In this case, it is still possible for two different agents to have two different affiliation strengths to the same organization, since in the `affiliationrel` table, there is no constraint on the `affiliation_strength` attribute.

### 2g) 
**Question:** Can one agent have different affiliation_strengths to two or more different organizations?

**Answer:** This case is the same as the previous. Organization is not clearly defined. Again assuming a one-to-one mapping from *organization* to `aff_id`, it is possible for one agent to have different affiliation strength in different organizations, since the primary key of the `affiliationrel` table would differ in the `aff_id` attribute. 

### 2h) 
**Question:** Can an agent participate in more than one ongoing mission?

**Answer:** Yes, missions are assigned to teams and agents are assigned to teams through the `teamrl` table. The primary key for the `teamrel` table is the joint `(team_id, agent_id)` attribute. Therefore, an agent can be assigned to multiple teams without violating the primary key of `teamrel`. There appears to be no constraint on `mission.mission_status` and therefore no reason an agent on two or more teams could not be assigned to multiple active missions. 




## Part 2

### 3a) 
#### SELECT * FROM Agent WHERE city = 'Istanbul' AND country = 'Turkey';

Show me all of the attributes in the `agent` table for agents from Istanbul, Turkey.


|agent_id |  first   | middle |  last  |      address      |   city   | country | salary | clearance_id |               
|---------|----------|--------|--------|-------------------|----------|---------|--------|--------------|
|     115 | George   | Jim    | Bahr   | 1 70th Avenue     | Istanbul | Turkey  |  58075 |            3 |
|     203 | George   |        | Pardy  | 43 31 35th Avenue | Istanbul | Turkey  |  51492 |            3 |                                
|     405 | Marie    |        | Angle  | 4 73th Avenue     | Istanbul | Turkey  |  56730 |            1 |                                 
|     540 | George   |        | Miller | 86 94th Avenue    | Istanbul | Turkey  |  56372 |            3 |                                 
|     830 | Nicholas | M      | Beene  | 15-17 49th Avenue | Istanbul | Turkey  |  77777 |            4 |
 
 
 (5 rows)           
 
### 3b) 
#### SELECT city FROM Agent;

List only the city for every agent in the agent table.

|city          |
|--------------|
|Athens        |
|Paris         |
|New York      |
|Athens        |
|New York      |

(662 rows)

### 3c) 
#### SELECT DISTINCT city FROM Agent;

List all the cities where agents are from, once.

|city          |
|--------------|
| Las Vegas
| Norfolk
| London
| Paris
| Shanghai
 
(46 rows)

### 3d) 
#### SELECT agent_id, city, country FROM Agent WHERE salary > 100000 AND country != 'USA';

Show me the agent id, city and country of all agents making over 100,000 in salary that are not from the USA.   

|agent_id |  city   | country
----------|---------|---------
|      144 | Baghdad | Iraq

(1 row)



### 4a) 
#### SELECT city FROM Agent WHERE salary > 90000;

Show the city of each agent that makes more than 90,000 in salary.

| city                                                                                                                          
|---------------                                                                                                                     
| New York                                                                                                                           
| San Francisco                                                                                                                      
| Baghdad                                                                                                                         
| Baghdad                                                                                                                           
| New York 

(131 rows)

### 4b) 
#### SELECT city FROM Agent <br> WHERE Agent.salary > 90000;

Show the city of each agent that makes more than 90,000 in salary.

| city                                                                                                                          
|---------------                                                                                                                     
| New York                                                                                                                           
| San Francisco                                                                                                                      
| Baghdad                                                                                                                         
| Baghdad                                                                                                                           
| New York 

(131 rows)

### 4c) 
#### SELECT city FROM Agent A WHERE A.salary > 90000;

Show the city of each agent that makes more than 90,000 in salary.

| city                                                                                                                          
|---------------                                                                                                                     
| New York                                                                                                                           
| San Francisco                                                                                                                      
| Baghdad                                                                                                                         
| Baghdad                                                                                                                           
| New York 

(131 rows)

### 5a) 
#### SELECT DISTINCT sc_level FROM SecurityClearance;

Show me the list of the distinct levels of security clearances an agent can hold.

|   sc_level
|--------------
| Secret
| Top Secret
| Magellon
| Majestic
| Unclassified
| Classified
| Presidential

(7 rows)

### 5b) 
####    SELECT * FROM Agent A, SecurityClearance S<br>WHERE A.city = 'London'<br>AND (S.sc_level = 'Top Secret');

For all agents from London, show all information from `agent` table and append all information from the row for `securityclearance.sc_level == 'Top Secret'` in the `securityclearance` table to each row.

|agent_id |  first   | middle |    last    |    address     |  city  | country | salary | clearance_id | sc_id |  sc_level  |          description
|---------|----------|--------|------------|----------------|--------|---------|--------|--------------|-------|------------|--------------------------------
|     138 | Pete     |        | Gupta      |                | London | England |  71246 |            5 |     4 | Top Secret | Fourth highest level of access
|     257 | Nicholas |        | Korn       | 9 71st Avenue  | London | England |  89645 |            4 |     4 | Top Secret | Fourth highest level of access
|     327 | Elias    |        | Breitkreuz | 53 18th Avenue | London | England |  54794 |            5 |     4 | Top Secret | Fourth highest level of access
|     388 | Nickolas |        | Mark       | 7 60th Avenue  | London | England |  54152 |            2 |     4 | Top Secret | Fourth highest level of access
|     414 | Hercules |        | Wadell     | 21 78th Avenue | London | England |  89043 |            1 |     4 | Top Secret | Fourth highest level of access

(9 rows)

### 5c) 
#### SELECT * FROM Agent A, SecurityClearance S <br> WHERE A.city = 'London' <br> AND (S.sc_level = 'Top Secret') <br> AND A.clearance_id = S.sc_id;

Show all information from `agent` and `securityclearance` tables for agents from London who hold a Top Secret security clearance.

|agent_id |  first   | middle |    last    |    address     |  city  | country | salary | clearance_id | sc_id |  sc_level  |          description
|---------|----------|--------|------------|----------------|--------|---------|--------|--------------|-------|------------|--------------------------------
|     257 | Nicholas |        | Korn       | 9 71st Avenue  | London | England |  89645 |            4 |     4 | Top Secret | Fourth highest level of access
|     419 | George   |        | Carter     | 2 83rd Avenue  | London | England |  89465 |            4 |     4 | Top Secret | Fourth highest level of access

(2 rows)

### 6a)
#### SELECT A.agent_id, A.first, A.last, A.city, A.country <br> FROM Agent A, TeamRel TR, Team T <br> WHERE A.agent_id = TR.agent_id <br>AND TR.team_id = T.team_id <br> AND T.name = 'Giraffe';

List the agent ID, first and last name, and agent's city and country for the agents who are members of the 'Giraffe' team.

| agent_id |  first  |   last    |     city      | country
|----------|---------|-----------|---------------|---------
|       80 | Mathew  | Hakanson  | San Francisco | USA
|      131 | Bob     | Foster    | Shanghai      | China
|      141 | Nick    | House     | Baghdad       | Iraq
|      223 | Kate    | Wu        | Madrid        | Spain
|      437 | Ethan   | Adkins    | Athens        | USA

(9 rows)

### 6b)
#### SELECT A1.first, A1.last, A2.city, A2.country <br> FROM Agent A1, Agent A2 <br> WHERE A1.city = A2.city <br> AND A1.country = A2.country <br> AND A1.clearance_id > A2.clearance_id <br> AND A1.salary >= A2.salary;

Show the first and last name and the city and country an agent is from for every instance in which that agent holds a lower level clearance but makes more or equal in salary than another agent in the same location.

|first      |      last       |     city      |  country                                             
|-----------|-----------------|---------------|------------
|Nick       | Black           | Athens        | USA
|Nick       | Black           | Athens        | USA
|Nick       | Black           | Athens        | USA
|Nick       | Black           | Athens        | USA
|Bill       | Bundt           | Paris         | France  

(5227 rows)


## Part 3

### 7) What are the team ID and the meeting frequency for the ShowBiz team?

```sql
SELECT team_id, meeting_frequency 
FROM team
WHERE name = 'ShowBiz';
```
 team_id | meeting_frequency
---------|-------------------
      19 | monthly

(1 row)

### 8) Which countries have agents with Classified or Magellon clearance?

```sql
SELECT DISTINCT country
FROM agent A, securityclearance C
WHERE A.clearance_id = C.sc_id
AND (C.sc_level = 'Classified' OR C.sc_level = 'Magellon');
```

 |country                                                                                                                          
 |------------                                                                                                                        
 |Iraq                                                                                                                               
 |Turkey                                                                                                                             
 |Spain                                                                                                                              
 |England                                                                                                                            
 |Italy 
 
 (20 rows)  
 
 
 ### 9) What are the first name, last name, and city of all agents on at least two teams? 
 
 ```sql
 SELECT DISTINCT A.first, A.last, A.city
 FROM agent A, teamrel T1, teamrel T2
 WHERE T1.agent_id = T2.agent_id
 AND A.agent_id = T1.agent_id
 AND T1.team_id != T2.team_id;
 ```
 

|  first   |      last       |     city
|----------|-----------------|---------------
| Tim      | Brock           | Milan
| Bill     | Zahedi          | Athens
| George   | Byus            | New York
| Pluto    | Herrmann        | Paris
| Tim      | McCracken       | Hong Kong            

(70 rows)


### 10) List the name and status of all missions that have at least one agent with the skill Kung Fu. Don’t repeat missions in your result.

```sql
SELECT DISTINCT M.name, M.mission_status
FROM mission M, teamrel T, agent A, skill S, skillrel SR
WHERE M.team_id = T.team_id
AND T.agent_id = A.agent_id
AND SR.agent_id = A.agent_id
AND SR.skill_id = S.skill_id
AND S.skill = 'Kung Fu';
```

|name                 | mission_status
|---------------------|----------------
|Desk Top             | success
|Melian               | success
|Causeway             | success
|IceT                 | success
|Code Red Worm Attack | failed 

(108 rows)


### 11) Which pairs of agents have the same first and last names? (List each pair only once.)

```sql
SELECT 
    DISTINCT ON (A1.first, A1.last) 
    A1.first, A1.last, 
    A1.agent_id, A2.agent_id 
FROM agent A1, agent A2
WHERE A1.first = A2.first
AND A1.last = A2.last
AND A1.agent_id != A2.agent_id;
```

|first  |   last   | agent_id | agent_id                                                                              
|-------|----------|----------|----------                                                                              
|Anri   | Lazaryan |      306 |      326                                                                               
|George | Carter   |      419 |      429                                                                               
|John   | Miller   |      258 |      432                                                                              

(3 rows)    
