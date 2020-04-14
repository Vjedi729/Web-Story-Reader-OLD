## Search Queries

### Version 2

#### Individual Queries
These generic queries work with any of the four traits types that a story (or other object) might have.
They are built to be generic and easily translate to a conditional statement
```JavaScript
{
  "text query (The name of the variable should go here)": {
    "text": "This is the text you want to search for. It can be any string.",
    "type": "{KEYWORD,CONTAINS,EXACT}"
      // KEYWORD = Contains any word in the string
      // CONTAINS = Contains the whole string
      // EXACT = Has the equal string
  },
  "numeric query (variable name goes here)": {
    "value": 1,
    "type": "{GT,LT,GTE,LTE,EQ,NEQ}"
      // GT = Greater than; LTE = Less than or equal to
      // GTE = Greater than or equal to; LT = Less than
      // EQ = equal to; NEQ = not equal to
  },
  "tag query (variable name here)": {
    "tags": ["A list of tags", "tag1", "tag2"],
    "type": "{ALL,ANY,NONE}"
      // ALL = Contains every tag in the tags list
      // ANY = Contains at least one tag in the tags list
      // NONE = Contains none of the tags in the tags list
  },
  "state query (variable name here)": {
    "states": ["A list of states", "state1"],
    "type": "{INC,EXC}",
      // INC = Is in any of the states listed above
      // EXC = Is NOT is any of the states listed above
  }
}
```
#### Query Structure
The overall query does not need to include every part.
```JavaScript
{
  "title": "text query",
  "author": "text query",
  "rating": "state query",
  "language": "state query",
  "status": "state query",

  "fandom": "tag query",
  "characters": "tag query",
  "relationships": "tag query",
  "other tags": "tag query",

  "word count": "numeric query",
  "chapter count": "numeric query",

  "publish date": "numeric query",
  "update date": "numeric query",

  "like count": "numeric query",
  "follow count": "numeric query"
  "comment count": "numeric query"
}
```

### Version 1
#### Query Structure
This older query structure works fairly well for stories, but is less flexible and somewhat inelegant.
```JavaScript
{
// STORY DATA
  "title": "Example Title to Search For",
  "title_type": "{CONTAINS/EXACT/KEYWORD}",

  "author": "Example Author Username",
  "author_type": "{CONTAINS/EXACT/KEYWORD}",

  "rating": "Maximum Rating",
  "languages": ["Language to include", "Another language to include"],
  "status": ["Status to include", "Another status to include"],
  // Each status is "{COMPLETE/INCOMPLETE}", with others to be added

// TAGS
  "fandoms":{
    "include_all": ["tag1", "tag2"], // Must include all of these
    "include_any": ["tag3", "tag4"], // Must include at least one of these
    "include_none": ["tag5", "tag6"], // Must not include any of these
  },
  "characters":{
    "include_all": ["character1", "character2"],
    "include_any": ["character3", "character4"],
    "include_none": ["character5", "charcter6"],
  },
  "relationships":{
    "include_all": [
      // Will also count multi-person relationships including all of these characters
      ["character1", "character2"],
      ["character3", "character4"]
    ],
    "include_any": [
      ["character5", "character6"]
    ],
    "include_none": [
      // Will also block multi-person relationships including these characters in a group
      ["character5", "character6"]
    ],
  },
  "other tags":{
    "include_all": ["tag1", "tag2"],
    "include_any": ["tag3", "tag4"],
    "include_none": ["tag5", "tag6"]
  },

## NUMERICS
  "word_count": 0,
  "word_query_type": "{GREATER/LESS}",
  "chapter_count": 0,
  "chapter_query_type": "{GREATER/LESS}",
  "publish_date": "1970-1-1",
  "publish_date_query_type": "{GREATER/LESS}",
  "update_date": "1970-1-1",
  "update_date_query_type": "{GREATER/LESS}",
  "like_count": 0,
  "like_query_type": "{GREATER/LESS}",
  "follow_count": 0,
  "follow_query_type": "{GREATER/LESS}",
  "comment_count": 0,
  "comment_query_type": "{GREATER/LESS}",
}

```
