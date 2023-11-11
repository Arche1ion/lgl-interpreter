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
    ["set", "densitySquare", ["class", "get_methods", "sq1", "_density", "weight"]],
    ["set", "densityCircle", ["class", "get_methods", "cir1", "_density", "weight"]],
    ["add", ["get", "densitySquare"], ["get", "densityCircle"]]
    

]