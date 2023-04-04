# Cypher Fundamentals
Cypher is Neo4j’s graph query language that lets you retrieve data from the graph. It is like SQL for graphs.

Cypher uses an ASCII-art type of syntax where `(nodes)-[:ARE_CONNECTED_TO]->(otherNodes)` using rounded brackets for circular `(nodes)`, and `-[:ARROWS]->` for relationships.

## Node Variables
If we later want to refer to the node, we can give it a variable like `(person)`.
If the node is not relevant to your return results, you can specify an anonymous node using empty parentheses (). This means that you will not be able to return this node later in the query.

## Node Labels
You can group similar nodes together by assigning a node label.

```cypher
()                  //anonymous node (no label or variable) can refer to any node in the database
(:Technology)       //no variable, label Technology
(work:Company)      //using variable work and label Company
```

## Relationships
Relationships are represented in Cypher using an arrow --> or <-- between two nodes. Additional information, such as how nodes are connected (relationship type) and any properties pertaining to the relationship, can be placed in square brackets inside of the arrow.
Undirected relationships are represented with no arrow and just two dashes --. This means that the relationship can be traversed in either direction.

```cypher
//data stored with this direction
CREATE (p:Person)-[:LIKES]->(t:Technology)

//query relationship backwards will not return results
MATCH (p:Person)<-[:LIKES]-(t:Technology)

//better to query with undirected relationship unless sure of direction
MATCH (p:Person)-[:LIKES]-(t:Technology)
```

## Relationship Types
Relationship types categorize and add meaning to a relationship, similar to how labels group nodes.

```cypher
[:LIKES]
[:IS_FRIENDS_WITH]
[:WORKS_FOR]
```

## Relationship Variables
Just as we did with nodes, if we want to refer to a relationship later in a query, we can give it a variable like  `[likes]`.

```cypher
-[likes:LIKES]->
```

## Properties
Properties are name-value pairs that provide additional details to our nodes and relationships. To represent these in Cypher, we can use curly braces within the parentheses of a node or the brackets of a relationship.

- Node property: `(p:Person {name: 'Jennifer'})`
- Relationship property: `-[rel:IS_FRIENDS_WITH {since: 2018}]->`

## Patterns
Nodes and relationships make up the building blocks for graph patterns. These building blocks can come together to express simple or complex patterns.

```cypher
(p:Person {name: "Jennifer"})-[rel:LIKES]->(g:Technology {type: "Graphs"})
```

## Queries
The `MATCH` keyword in Cypher is what searches for an existing node, relationship, label, property, or pattern in the database. If you are familiar with SQL, MATCH works pretty much like `SELECT` in SQL.

The `RETURN` keyword in Cypher specifies what values or results you might want to return from a Cypher query. You can tell Cypher to return nodes, relationships, node and relationship properties, or patterns in your query results. RETURN is not required when doing write procedures, but is needed for reads.

Example 1: Find the labeled Person nodes in the graph. Note that we must use a variable like p for the Person node if we want retrieve the node in the RETURN clause.

```cypher
MATCH (p:Person)
RETURN p
LIMIT 1
```

Example 2: Find Person nodes in the graph that have a name of 'Tom Hanks'. Remember that we can name our variable anything we want, as long as we reference that same name later.

```cypher
MATCH (tom:Person {name: 'Tom Hanks'})
RETURN tom
```

Example 3: Find which Movies Tom Hanks has directed.

```cypher
MATCH (:Person {name: 'Tom Hanks'})-[:DIRECTED]->(movie:Movie)
RETURN movie
```

Example 4: Find which Movie Tom Hanks has directed, but this time, return only the title of the movie.

```cypher
MATCH (:Person {name: 'Tom Hanks'})-[:DIRECTED]->(movie:Movie)
RETURN movie.title
```

## Filtering Queries
You can filter query results using the `WHERE` clause:

```cypher
MATCH (p:Person)
WHERE 3 <= p.yearsExp <= 7
RETURN p
```

Checking strings:

```cypher
//check if a property starts with 'M'
MATCH (p:Person)
WHERE p.name STARTS WITH 'M'
RETURN p.name;

//check if a property contains 'a'
MATCH (p:Person)
WHERE p.name CONTAINS 'a'
RETURN p.name;

//check if a property ends with 'n'
MATCH (p:Person)
WHERE p.name ENDS WITH 'n'
RETURN p.name;
```

List of values:

```cypher
MATCH (p:Person)
WHERE p.yearsExp IN [1, 5, 6]
RETURN p.name, p.yearsExp
```

## Inserting Data
You can use `CREATE` to insert nodes, relationships, and patterns into Neo4j.
Let's create two nodes labeled Person:

```cypher
CREATE (friend:Person {name: 'Jennifer'})
CREATE (friend:Person {name: 'Mark'})
```

Now we can add a new `IS_FRIENDS_WITH` relationship between the existing Jennifer and Mark nodes:

```cypher
MATCH (jennifer:Person {name: 'Jennifer'})
MATCH (mark:Person {name: 'Mark'})
CREATE (jennifer)-[rel:IS_FRIENDS_WITH]->(mark)
```

We can also create both nodes and the relationship at the same time:

```cypher
CREATE (j:Person {name: 'Jennifer'})-[rel:IS_FRIENDS_WITH]->(m:Person {name: 'Mark'})
```

## Avoiding Duplicate Data Using MERGE
`MERGE` does a "select-or-insert" operation that first checks if the data exists in the database. If it exists, then Cypher returns it as is or makes any updates you specify on the existing node or relationship. If the data does not exist, then Cypher will create it with the information you specify.

```chypher
MATCH (j:Person {name: 'Jennifer'})
MATCH (m:Person {name: 'Mark'})
MERGE (j)-[r:IS_FRIENDS_WITH]->(m)
RETURN j, r, m
```

Notice that we used MATCH here to find both Mark’s node and Jennifer’s node before we used MERGE to find or create the relationship. Why did we not use a single statement? MERGE looks for an entire pattern that you specify to see whether to return an existing one or create it new. If the entire pattern (nodes, relationships, and any specified properties) does not exist, Cypher will create it.

```cypher
//this statement will create duplicate nodes for Mark and Jennifer
MERGE (j:Person {name: 'Jennifer'})-[r:IS_FRIENDS_WITH]->(m:Person {name: 'Mark'})
RETURN j, r, m
```

Perhaps you want to use MERGE to ensure you do not create duplicates, but you want to initialize certain properties if the pattern is created and update other properties if it is only matched. In this case, you can use ON CREATE or ON MATCH with the SET keyword to handle these situations.

```cypher
MERGE (m:Person {name: 'Mark'})-[r:IS_FRIENDS_WITH]-(j:Person {name:'Jennifer'})
  ON CREATE SET r.since = date('2018-03-01')
  ON MATCH SET r.updated = date()
RETURN m, r, j
```

## Updading Data
You can modify node and relationship properties by matching the pattern you want to find and using the SET keyword to add, remove, or update properties.

```cypher
MATCH (:Person {name: 'Jennifer'})-[rel:WORKS_FOR]-(:Company {name: 'Neo4j'})
SET rel.startYear = date({year: 2018})
RETURN rel
```

## Deleting Data
Deleting a node:

```cypher
MATCH (m:Person {name: 'Mark'})
DELETE m
```

Deleting a relationship:

```cypher
MATCH (j:Person {name: 'Jennifer'})-[r:IS_FRIENDS_WITH]->(m:Person {name: 'Mark'})
DELETE r
```

Neo4j is ACID-compliant so it doesn’t allow us to delete a node if it still has relationships. Using the DETACH DELETE syntax tells Cypher to delete any relationships the node has, as well as remove the node itself.

```cypher
MATCH (m:Person {name: 'Mark'})
DETACH DELETE m
```

Deleting properties:

```cypher
//delete property using REMOVE keyword
MATCH (n:Person {name: 'Jennifer'})
REMOVE n.birthdate

//delete property with SET to null value
MATCH (n:Person {name: 'Jennifer'})
SET n.birthdate = null
```

## References
https://neo4j.com/developer/cypher/
