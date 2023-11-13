[
    "sequence",
    ["class", "define", "Shape", ["_name"], ["_density"], null],
    ["class", "define", "Square", ["_side"],["_area"], "Shape"],
    ["class", "define", "Circle", ["_radius"],["_area"], "Shape"],

    ["class", "instantiate", "sq1", "Square", "sq", 3],
    ["class", "set_methods", "sq1", "_area",
        ["function", 
            ["num"], 
            ["multiply",["get", "num"],["get", "num"]]
        ]
    ],
    ["class", "set_methods", "sq1", "_density",
        ["function", 
            ["weight"], 
            ["division",["get", "weight"],["class","get_methods", "sq1","_area",["class","get_attributes","sq1","_side"]]]
        ]
    ],

    ["class", "instantiate", "cir1", "Circle", "ci", 2],
    ["class", "set_methods", "cir1", "_area",
        ["function", 
            ["num"], 
            ["multiply",["get", "num"],["get", "num"], 3.14]
        ]
    ],
    ["class", "set_methods", "cir1", "_density",
        ["function", 
            ["weight"], 
            ["division",["get", "weight"],["class","get_methods", "cir1","_area",["class","get_attributes","cir1","_radius"]]]
        ]
    ],

    ["set", "weight", 5],
    ["class","set_attributes","sq1","color", "blue", "_name", "temp"],
    ["print", ["class","get_attributes","sq1","color"]],
    ["print", ["class","get_attributes","sq1","_name"]],
    ["print", ["class","parent","sq1"]],
    ["print", ["class","parent","Square"]],
    ["print", ["class","parent","Shape"]],
    ["class","set_attributes","sq1", "_name", "sq1"],
    ["set", "densitySquare", ["class", "get_methods", "sq1", "_density", ["get","weight"]]],
    ["set", "densityCircle", ["class", "get_methods", "cir1", "_density", ["get","weight"]]],
    ["add", ["get", "densitySquare"], ["get", "densityCircle"]]
    

]