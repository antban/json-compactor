# json-compactor
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
