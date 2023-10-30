[
    "seq",
    ["set", "get_cube_power", ["func", "x", ["power", ["get", "x"], 3]]],
    ["set", "add_cubes", ["func", ["a", "b"], ["add", ["call", "get_cube_power", ["get", "a"]],  ["call", "get_cube_power", ["get", "b"]] ]]],
    ["call", "add_cubes", 3, 2]
]