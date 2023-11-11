[

    "sequence",
        ["multiply",5,2],
        ["division",12,3],
        ["power",12,3],
        ["print",12],
        ["print", "result: ", ["multiply",5,2]],

        ["set","counter",0],
        ["while",["get","counter"],"<",5,
            [
                "sequence",
                ["print", "In loop nr: "],
                ["print",["get", "counter"]],
                ["set","counter",["add",["get", "counter"],1]]
            ]
        ],

        ["array", "new", "array1", 2],
        ["array", "set", "array1", 0, 1],
        ["array", "set", "array1", 1, 65],
        ["print", ["array", "get", "array1", 1]],

        ["dict", "new", "dict1"],
        ["dict", "set_value", "dict1", "key1", 1],
        ["dict", "set_value", "dict1", "key2", "two"],
        ["dict", "set_value", "dict1", "key3", 5.55],
        ["print", ["dict", "get_value", "dict1", "key3"]],

        ["dict", "new", "dict2"],
        ["dict", "set_value", "dict2", "key1", -3],
        ["dict", "set_value", "dict2", "age", 58],
        ["print",
            "dict2 before merge:",
            ["dict", "get_value", "dict2", "key1"],
            ["dict", "get_value", "dict2", "age"]
        ],
        
        ["dict", "merge", "dict2", "dict2","dict1"],

        ["print", "dict2 after merge: "],
        ["print", ["dict", "get_value", "dict2", "key1"]],
        ["print", ["dict", "get_value", "dict2", "key2"]],
        ["print", ["dict", "get_value", "dict2", "key3"]],
        ["print", ["dict", "get_value", "dict2", "age"]]
             
]
