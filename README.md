# json-compactor
Sometimes there is a need to figure out what is the part of json is actually used for data, and how much it is needed for schema.
Also, sometimes with schemaless json there is a need to compress it (as compression may be too expensive).

In order to figure out what is happening with json in this case, this test tool was created - it assembles the schema of json data and writes it as a type information, and tries to store data in json in a more optimal way. Below one can find description of the format. 

## The simple way is to write schema and data in the json file separately. 

The root compacted object is 
```json
{"v": "0.0.1","t": [],"d": []}
```
where:
 - `t` - types information
 - `v` - version information
 - `d` - data of compacted json

Type defines the content of the object, and contains the names of the values stored in data.
For example, 
```
"t":[["name","value"],["name2","value"]]
```
means that there are 2 types defined. Type with index `0` contains 2 properties: `name` and `value`. Type with index `1` also contains 2 properties: `name2` and `value`. As the type ids are positive value, the specific type id of `-1` means array. 

`d` object contains actual data. Actual data contains of arrays. First element of array is type id, other values of array are the values of type elemetnts. 

For example the following json: 
```
{
  "v":"0.0.1",
  "t":[
    ["name","value"],
    ["name2","value"]
  ],
  "d":[
    -1,
    [
      0,
      "test",
      "test2"
    ],[
      1,
      "yyy",
      [
        0,
        "xxx",
        2
      ]
    ]
  ]
}
```
Will be decompressed to:
```
[
  {
    "name": "test",
    "value": "test2"
  },
  {
    "name2": "yyy",
    "value": {
      "name": "xxx",
      "value": 2
    }
  }
]
```

In case of of arrays of uniform objects the proposed format gives significant decrease of space used.

Comparison of size in the case above:
```
{"v":"0.0.1","t":[["name","value"],["name2","value"]],"d":[-1,[0,"test","test2"],[1,"yyy",[0,"xxx",2]]]}
[{"name": "test","value": "test2"},{"name2": "yyy","value": {"name": "xxx","value": 2}}]
```

