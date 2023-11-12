[
    "sequence",
    ["set", "get_cube_power", ["function", "x", ["power", ["get", "x"], 3]]],
    ["set", "add_cubes", ["function", ["a", "b"], ["add", ["call", "get_cube_power", ["get", "a"]],  ["call", "get_cube_power", ["get", "b"]] ]]],
    ["call", "add_cubes", 3, 2],

    ["set", "bizarre_sum", 
        ["function", "x", 
            ["add", 
                ["multiply", ["get", "x"], 3], 
                ["multiply", ["call", "get_cube_power", ["get", "x"]], ["call", "add_cubes", 3, 2]]
            ]
        ]
    ],

    ["set","counter",0],
    ["while",["get","counter"],"<",5,
        [
            "sequence",
            ["print", "In loop nr: "],
            ["print", ["get", "counter"]],
            ["print", ["call", "bizarre_sum", ["get","counter"]]],
            ["set","counter",["add",["get", "counter"],1]]
        ]
    ]
    
]