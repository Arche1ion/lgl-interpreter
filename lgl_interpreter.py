import sys
import json


# ---from funcs-demo in session 4---
def do_function(envs, args):
    # define function
    assert len(args) == 2
    params = args[0]
    body = args[1]
    return ["function", params, body]


def do_call(envs, args):
    # call function
    assert len(args) >= 1
    name = args[0]
    arguments = args[1:]
    # eager evaluation
    values = [do(envs, arg) for arg in arguments]

    func = envs_get(envs, name)
    assert isinstance(func, list)
    assert func[0] == "function"
    func_params = func[1]
    assert len(func_params) == len(values)  # assert values passed to func is same as values required by definition

    local_frame = dict(zip(func_params, values))  # dict of param name and values
    envs.append(local_frame)  # push this local frame/ dict to top of envs
    body = func[2]
    result = do(envs, body)
    envs.pop()

    return result


def envs_get(envs, name, index=None):
    # get defined function from the top most possible frame
    assert isinstance(name, str)
    for e in reversed(envs):
        if name in e:
            if index == None:
                return e[name]
            else:
                return e[name][index]

    assert False, f"Unknown variable name {name}"


def envs_set(envs, name, value, i=None):
    # save variables and functions to
    # paul adds the possibility to add lists and dictionaries
    # variables have name as key and default data type value as value
    # functions have name as key and a list ["Funktion", "params", "body"] as value
    # arrays have name as key and a list ["array", size, list of fixed size ] as value

    assert isinstance(name, str)

    if i == None:
        envs[-1][name] = value  # in the most local frame, assign value to key "name"
    else:
        envs[-1][name][i] = value


def do_set(envs, args):
    assert len(args) == 2
    assert isinstance(args[0], str)
    var_name = args[0]
    value = do(envs, args[1])
    envs_set(envs, var_name, value)
    return value


def do_get(envs, args):
    assert len(args) == 1
    return envs_get(envs, args[0])


def do_add(envs, args):
    assert len(args) == 2
    left = do(envs, args[0])
    right = do(envs, args[1])
    return left + right


def do_abs(envs, args):
    assert len(args) == 1
    value = do(envs, args[0])
    return abs(value)


def do_subtract(envs, args):
    assert len(args) == 2
    left = do(envs, args[0])
    right = do(envs, args[1])
    return left - right


def do_sequence(envs, args):
    assert len(args) > 0
    for operation in args:
        result = do(envs, operation)
    return result


# --- end of funcs-demo in session 4---

# ----------to implement in 1---------------
def do_multiply(envs, args):
    #Input:
    #Parameters:    envs: Environment which keeps track of all variables
    #               args: arbitrary amount of integers, but at least two
    #Output:        Product of all given ints in args
    prod = 1
    for arg in args:
        assert isinstance(do(envs, arg), int)
        prod *= do(envs, arg)
    return prod


def do_division(envs, args):
    # Input:
    # Parameters:    envs: Environment which keeps track of all variables
    #                args: two integers
    # Output:        Division of first arg by second arg
    assert len(args) == 2
    left = do(envs, args[0])
    right = do(envs, args[1])
    return left / right


def do_power(envs, args):
    # Input:
    # Parameters:    envs: Environment which keeps track of all variables
    #                args: two integers
    # Output:        First arg to the power of second arg
    assert len(args) == 2
    base = do(envs, args[0])
    exponent = do(envs, args[1])
    return base ** exponent


def do_print(envs, args):
    # note: have to check how to print class/obj
    # Input:
    # Parameters:    envs: Environment which keeps track of all variables
    #                args: an arbitrary amount of vars with any type works
    # Output:        print of all given args
    for arg in args:
        print(do(envs, arg))


def do_while(envs, args):
    # Input:
    # Parameters:   envs: Environment which keeps track of all variables
    #               args: first arg is conditional variable, second arg is operator, third arg is var that the conditional variable is compared to, fourth arg is statement inside the while loop
    # Output:       no return, except the statement returns something, loop through this statement
    # ["while","cond_var", "operator","count_var","statement"]
    # while count_var operator cond_var: statement
    # ex:
    #   while size <= count_var:
    #       print("size")
    #       size += 1
    assert len(args) == 4
    # assert isinstance(args[0],int)
    # assert isinstance(args[1],str)
    # assert isinstance(args[2],int)
    # assert isinstance(args[3],list)
    if args[1] == "==":
        while do(envs, args[0]) == args[2]:
            do(envs, args[3])
    elif args[1] == "!=":
        while do(envs, args[0]) != args[2]:
            do(envs, args[3])
    elif args[1] == ">=":
        while do(envs, args[0]) >= args[2]:
            do(envs, args[3])
    elif args[1] == "<=":
        while do(envs, args[0]) <= args[2]:
            do(envs, args[3])
    elif args[1] == "<":
        while do(envs, args[0]) < args[2]:
            do(envs, args[3])
    elif args[1] == ">":
        while do(envs, args[0]) > args[2]:
            do(envs, args[3])
    else:
        assert False, f'Unknown operator "{args[0]}"'


def do_array(envs, args):
    """
    Array operations: create new array of fixed size, get value at index i, set value at index i
    Arrays have name as key and a list ["array", size, list of fixed size ] as value in e in envs
    
    Args:
        args: list of arguments - args[0] = "array", args[1] = operation, args[2] = name, args[3] = value
        envs: environment that keeps track of all variables

    
    Returns:
        new: returns a list ["array", size, list of fixed size]
        get: returns value at index i of array
        set: returns value set to index i of array
        
    """

    def array_new(envs, args):
        """
        Creates array called name of size n
        equivalent to do_function and do_set

        Args: 
            envs: list of environments
            args: [name: str, n: int]
        Return:
            empty array with name and size n
        """
        assert len(args) == 2
        assert isinstance(args[0], str) and isinstance(args[1], int)

        res = [None] * args[1]
        envs_set(envs, args[0], res)
        return ["array", args[1], res]

    def array_get(envs, args):
        """
        get the value of array at certain index
        equivalent to do_get

        Args: 
            envs: list of environments
            args: [name: str, i: int]
        Return:
            int - value at name[i]
        """
        assert len(args) == 2
        assert isinstance(args[0], str) and isinstance(args[1], int)
        return envs_get(envs, args[0], args[1])

    def array_set(envs, args):
        """
        set the value of array at certain index
        Equivalent to do_set

        Args: 
            envs: list of environments
            args: [name: str, i: int, val: value]
        Return:
            int - value at name[i]
        """
        assert len(args) == 3
        assert isinstance(args[0], str) and isinstance(args[1], int)
        array_name = args[0]
        i = args[1]
        value = do(envs, args[2])
        envs_set(envs, array_name, value, i)  # check index passed to envs_set
        return value

    # introspection in do_array()
    d = locals().copy()
    OPERATIONS_ARRAY = {}
    for k in d:
        if k.startswith("array_"):
            OPERATIONS_ARRAY[k.replace("array_", "")] = d[k]

    assert args[0] in OPERATIONS_ARRAY, f"Unknown operation {args[0]}"
    func = OPERATIONS_ARRAY[args[0]]
    return func(envs, args[1:])


def do_dict(envs, args):
    def dict_new(envs, args):
        '''
        creates dictionary called name ->Do dictionary names have to be strings?
        args:
            envs: environment
            args: ["name"]
        return:
            None
            '''
        dict_name = args[0]
        assert len(args) == 1
        assert isinstance(dict_name, str)
        envs_set(envs, dict_name, {})

    def dict_get_value(envs, args):
        '''
        get value of a key in dict
        args:
            envs: environment
            args: ["name","key"]
        return:
            value of key
        '''
        dict_name = args[0]
        key = args[1]
        assert len(args) == 2
        assert isinstance(dict_name, str)
        dict = envs_get(envs, dict_name)
        if key not in dict:
            print(f"Error: key {key} not in dictionary {dict_name}")
        else:
            value = dict[key]
            return value

    def dict_set_value(envs, args):
        '''
        set value of key in dict name
        args:
            env: environment
            args: ["name","key","value"]
        return:
            None
        '''
        dict_name = args[0]
        key = args[1]
        value = args[2]
        assert len(args) == 3
        assert isinstance(dict_name, str)
        dict = envs_get(envs, dict_name)
        dict[key] = value

    def dict_merge(envs, args):
        """
        this function merges two dictionarys -> should we delete the merged dictionarys?
        args:
            env: environment
            agrs: ["name", "dict1","dict2"]
        return:
            None or new dictionary
        """
        new_dict = args[0]
        dict_name1 = args[1]
        dict_name2 = args[2]
        assert len(args) == 3
        assert isinstance(new_dict, str) and isinstance(dict_name1, str) and isinstance(dict_name2, str)
        dict1 = envs_get(envs, dict_name1)
        dict2 = envs_get(envs, dict_name2)
        merged = dict1 | dict2
        envs_set(envs, new_dict, merged)

    # -----introspection in dict----------------------------
    variables = locals().copy()
    OPERATIONS_DICT = {}
    for k in variables:
        if k.startswith("dict_"):
            OPERATIONS_DICT[k.replace("dict_", "")] = variables[k]

    assert args[0] in OPERATIONS_DICT, f"Unknown operation: {args[0]}"
    func = OPERATIONS_DICT[args[0]]
    return func(envs, args[1:])


# -----end of dict-----------------------------------------


# ---------end of 1---------------------


# --------- 2 Object System ------------

# define Shape, Square, Circle, see session 2


"""
our_class={
    "_classname": name
    "_attributes": dict of attributes
    "_methods": dict of methods
    "_parent": parent
}

our_instance={
    "_parent": "Shape"
    "attributes": {}
    "methods": {}
} 
"""


def do_class(envs, args):
    def class_define(envs, args):
        #["class","define","classname","attributes","methods","parent"=None]
        #If "parent!=None", we just take "attributes" and "methods" from "parent"
        """
                Define new class
                Args:
                    envs: list of environments
                    args: [classname:str, attributes:list, methods:list, parent:string(default=None]
                Returns:
                    None
                """
        class_dict = {
            "_classname": args[0],
            "_attributes": args[1],
            "_methods": args[2],
            "_parent": args[3]
        }
        assert isinstance(args[1], list)
        assert isinstance(args[2], list)
        if args[3] != None: #If "parent"!=None
            assert envs_get(envs, args[0]) == None, f"Class {args[0]} already exists!"
            parent = envs_get(envs, args[3])
            class_dict["_attributes"] = parent["_attributes"]
            class_dict["_methods"] = parent["_methods"]
        envs_set(envs, args[0], class_dict)

    def class_instantiate(envs, args):
        """
        instantiate new object
        Args:
            envs: list of environments
            args: [instance_name:str, class_name:str,parameters]
        Returns:
            None
        """
        instance_name = args[0]
        class_name = args[1]
        data = envs_get(envs, class_name)
        data_c = data.copy()
        data_c["_parent"] = class_name

        if len(args) > 2:
            parameters = args[2:]
            attributes=data_c["_attributes"]
            i = 0
            for key in attributes.keys():
                if attributes[key].startswith("_"):
                    attributes[key] = parameters[i]
                    i += 1

        envs_set(envs,instance_name,data_c)


# ------------ combine set and append ------------------

    def class_combine_attributes(envs, args):
        """
        set attributes of a given instance of class
        implementation of option 2
        

        Args: 
            envs: list of environments
            args: [instance_name: str, attribute_name_1, value1, ...]
        Return:
            to be determined, temporarily None
            
        """ 

        maxlen = len(args[1:])
        assert maxlen%2==0, "invalid syntax: set_attributes requires attribute-value pairs"
        for i in range(1,maxlen,2):
            att = do(args[i])
            value = do(args[i+1])
            data = envs_get(envs,args[0])#get the dictionary containing data of the instance variable, assert in envs_get
            name = args[0] #instance name
            while (not (att in data.keys())) and (data["_parent"] != None):
                name = data["_parent"] #name is class name or parent class name
                data = envs_get(envs,name) #get dict containing data of class or parent class
            assert type(data["_attributes"])==dict, f"{args[0]} has no attribute"
            if att in data["_attributes"].keys(): #if it is an existing attribute:
                copy = data.copy()
                copy["_attributes"][att] = value #set value in attributes dictionary at index attribute_name (att)
                envs_set(envs,name,copy)
            else: #if it is a new attribute
                data = envs_get(envs,args[0])#get information of the instance
                copy["_attributes"][att] = value #append value in attributes dictionary at index attribute_name (att)
                envs_set(envs,name,copy)

            

        return None

    def class_combine_methods(envs, args):
        """
        set methods of a given instance of class
        implementation of option 2
        

        Args: 
            envs: list of environments
            args: [instance_name: str, methodname1: str, methodbody: function object, ...]
        Return:
            to be determined, temporarily None
            
        """

        maxlen = len(args[1:])
        assert maxlen%2==0, "invalid syntax: set_methods requires method name - method body pairs"
        for i in range(1,maxlen,2):
            methodname = args[i]
            assert type(methodname)==str, "invalid syntax: invalid data type for method name"
            body = do(args[i+1]) # body = list ["function",[params],body]
            assert body[0] == "function", f"{methodname} should be defined as a function"
            name = args[0] #place holder for class_name to check up
            data = envs_get(envs,name) #get the dictionary containing data of the instance variable, assert in envs_get
            while (not (methodname in data.keys())) and (data["_parent"] != None): #while current instance or class doesnt have method
                name = data["_parent"] #name is class name or parent class name
                data = envs_get(envs,name) #get dict containing data of class or parent class
            assert type(data) == dict, f"{name} doesnt have methods"
            if methodname in copy["methods"].keys(): #if it is an existing method
                copy = data.copy()
                copy["_methods"][methodname] = body #set value in methods dictionary at index method_name (att)
                envs_set(envs,name,copy)
            else: #if it is a new method
                data = envs_get(envs,args[0])
                copy = data.copy()
                copy["_methods"][methodname] = body #append value in methods dictionary at index method_name (att)
                envs_set(envs,name,copy)


        return None
    #------ end of combine append and set -------------------------

    def class_append_attributes(envs, args):
        # ["class", "append_attributes", "class_name", {dict of attributes}]
        class_name = args[0]
        data = envs_get(envs, class_name)
        data_c = data.copy()
        data_c["_attributes"] = data_c["_attributes"] | args[1]
        envs_set(envs, class_name, data_c)

    def class_append_methods(envs, args):
        # ["class", "append_methods", "class_name", {dict of methods}]
        class_name = args[0]
        data = envs_get(envs, class_name)
        data_c = data.copy()
        data_c["_methods"] = data_c["_methods"] | args[1]
        envs_set(envs, class_name, data_c)

    def class_set_attributes(envs, args):
        """
        set attributes of a given instance of class
        implementation of option 2
        

        Args: 
            envs: list of environments
            args: [instance_name: str, attribute_name_1, value1, ...]
        Return:
            to be determined, temporarily None
        """


        maxlen = len(args[1:])
        assert maxlen % 2 == 0, "invalid syntax: set_attributes requires attribute-value pairs"
        for i in range(1, maxlen, 2):
            att = do(args[i])
            value = do(args[i + 1])
            data = envs_get(envs,
                            args[0])  # get the dictionary containing data of the instance variable, assert in envs_get
            name = args[0]  # instance name
            while (not (att in data.keys())) and (data["_parent"] != None):
                name = data["_parent"]  # name is class name or parent class name
                data = envs_get(envs, name)  # get dict containing data of class or parent class
            assert type(data["_attributes"]) == dict, f"{args[0]} has no attribute"
            assert att in data["_attributes"].keys(), f"invalid syntax: No attribute {args[i]} found in {args[0]}"
            copy = data.copy()
            copy["_attributes"][att] = value  # set value in attributes dictionary at index attribute_name (att)
            envs_set(envs, name, copy)

        return None

    def class_set_methods(envs, args):
        """
        set methods of a given instance of class
        implementation of option 2
        

        Args: 
            envs: list of environments
            args: [instance_name: str, methodname1: str, methodbody: function object, ...]
        Return:
            to be determined, temporarily None
            
        """

        maxlen = len(args[1:])
        assert maxlen%2==0, "invalid syntax: set_methods requires method name - method body pairs"
        for i in range(1,maxlen,2):
            methodname = args[i]
            assert type(methodname)==str, "invalid syntax: invalid data type for method name"
            body = do(args[i+1]) #body is a list ["function",["params"],body]
            assert body[0] == "function", f"{methodname} should be defined as a function"
            name = args[0] #place holder for class_name to check up
            data = envs_get(envs,name) #get the dictionary containing data of the instance variable, assert in envs_get
            while (not (methodname in data.keys())) and (data["_parent"] != None): #while current instance or class doesnt have method
                name = data["_parent"] #name is class name or parent class name
                data = envs_get(envs,name) #get dict containing data of class or parent class
            assert type(data) == dict, f"{name} doesnt have methods"
            assert methodname in copy["methods"].keys(), f"invalid syntax: {args[0]} has no method {args[i]}"
            copy = data.copy()
            copy["_methods"][methodname] = body  # set value in attributes dictionary at index attribute_name (att)
            envs_set(envs, name, copy)

        return None

    def class_get_attributes(envs, args):

        """
        get attribute of a given instance of class
        implementation of option 2
        

        Args: 
            envs: list of environments
            args: [instance_name: str, attribute_name: str]
        Return:
            to be determined, temporarily the value of the attribute
            
        """
        assert len(args) == 2, "Invalid syntax: expected 2 arguments for get_attributes"
        name = args[0]  # instance name
        att = args[1]
        while (not (att in data.keys())) and (data["_parent"] != None):
            name = data["_parent"]  # name is class name or parent class name
            data = envs_get(envs, name)  # get dict containing data of class or parent class
        assert type(data["_attributes"]) == dict, f"{args[0]} has no attribute"
        assert att in data["_attributes"].keys(), f"invalid syntax: No attribute {att} found in {args[0]}"
        return data["_attributes"][att]

    def class_get_methods(envs, args):

        """
        get method of a given instance of class
        implementation of option 2
        1108: when we want to call a method in TUL, the do_call function
        is not available, this method returns the value that is produced with
        given input parameters
        

        Args: 
            envs: list of environments
            args: [instance_name: str, method_name: str, args: values]
        Return:
            to be determined, temporarily method body of the method
            
        """

        assert len(args) == 2, "Invalid syntax: expected 2 arguments for get_methods"
        name = args[0]  # instance name
        method_name = args[1]
        while (not (method_name in data.keys())) and (data["_parent"] != None):
            name = data["_parent"]  # name is class name or parent class name
            data = envs_get(envs, name)  # get dict containing data of class or parent class
        assert type(data["_methods"]) == dict, f"{args[0]} has no method"
        assert method_name in data["_methods"].keys(), f"invalid syntax: No method {method_name} found in {args[0]}"
        func = data["_methods"][method_name] # func is list ["function",[params],body]
        assert isinstance(func, list)

        #copy code from do_call because do_call gets functions from envs,
        #but methods are embedded inside instance_name, not directly accessable from envs

        arguments = args[2:]
        # eager evaluation
        values = [do(envs, arg) for arg in arguments]
        assert func[0] == "function"
        func_params = func[1]
        assert len(func_params) == len(values)  # assert values passed to func is same as values required by definition

        local_frame = dict(zip(func_params, values))  # dict of param name and values
        envs.append(local_frame)  # push this local frame/ dict to top of envs
        body = func[2]
        result = do(envs, body)
        envs.pop()

        return result
    
        

        
    def class_parent(envs, args):
        '''
        set parent class, make current class inherit from class "parent"

        params:
            envs: list of dicts, stack (list) of frames with dictionary as element
            args: list of arguments ["parent", "classname", "parent_name"]

        return:
            ["class", "classname", dictionary], dictionary is updated to inherit from parent_name

        '''
        assert args[0] == "parent"
        classname = args[1]
        parentname = args[2]
        envs_set(envs, classname, parentname, "parent")
        return ["class", classname, envs_get(envs, classname)]

    # introspection in do_dict()
    d = locals().copy()
    OPERATIONS_CLASS = {}
    for k in d:
        if k.startswith("class_"):
            OPERATIONS_CLASS[k.replace("class_", "")] = d[k]

    assert args[0] in OPERATIONS_CLASS, f"Unknown operation {args[0]}"
    func = OPERATIONS_CLASS[args[0]]
    return func(envs, args[1:])


# ------------------------------


# --------- 3 Logging -----------

# Use decorator in chapter 9

# -----------------------------


# -----OPERATIONS and do() from funcs-demo.py in session 4------------

OPERATIONS = {
    func_name.replace("do_", ""): func_body
    for (func_name, func_body) in globals().items()
    if func_name.startswith("do_")
}


def do(envs, expr):
    if isinstance(expr, int):
        return expr
    if isinstance(expr, str):
        return expr
    if isinstance(expr, float):
        return expr

    assert isinstance(expr, list)
    assert expr[0] in OPERATIONS, f"Unknown operation {expr[0]}"
    func = OPERATIONS[expr[0]]
    return func(envs, expr[1:])


# ----end OPERATIONS and do() -----------------------


def legal_input():
    """
    Handles correct usage of command line input.
    
    Args:
    
    Returns:
        int = 2: call with FILENAME.gsc
        int = 4: call with --trace
    """

    error_message = "Usage: lgl_interpreter.py FILENAME.gsc;\nUsage: lgl_interpreter.py FILENAME.gsc --trace trace_file.log"
    argv_len = len(sys.argv)
    assert argv_len % 2 == 0, error_message
    assert (argv_len == 2 or argv_len == 4), error_message
    if argv_len == 2:
        print("argv_len == 2")
        return argv_len
    else:
        print("argv_len == 4")
        assert sys.argv[2] == "--trace", error_message
        return argv_len


def main_in_funcs_demo():
    assert len(sys.argv) == 2, "Usage: lgl_interpreter.py filename.gsc"
    with open(sys.argv[1], "r") as source_file:
        program = json.load(source_file)
    assert isinstance(program, list)
    envs = [{}]
    result = do(envs, program)
    print(f"=> {result}")


def main():
    # legal_input()
    # continue implementation
    main_in_funcs_demo()


if __name__ == "__main__":
    main()
