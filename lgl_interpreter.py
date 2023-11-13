import datetime
import sys
import json
import random

# -------- functions for logging -------- #
def legal_input():
    """
    Helperfunction for logging, checks if logging is required

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
        return argv_len
    else:
        assert sys.argv[2] == "--trace", error_message
        return argv_len

ids=list()
def get_id():
    number = random.randint(10000, 100000)
    while number in ids:
        number = random.randint(10000, 100000)
    ids.append(number)
    return number

def logging(func):
    stack=[]
    def log_entry(func_name,status,id):
        with open("trace_file.log", "a") as log:
            log.write(f"{id},{func_name},{status},{str(datetime.datetime.now())}\n")
    def wrapper(envs,args):
        id=get_id()
        if legal_input() == 4:
            if func.__name__ == "class_get_methods":
                func_name=args[1]
            elif func.__name__ =="do_call":
                func_name=args[0]
            else:
                func_name=func.__name__

            stack.append(func_name)
            log_entry(func_name, "start",id)
            result=func(envs, args)
            log_entry(func_name, "stop",id)

            return result

        else:
            return func(envs,args)


    return wrapper

# -------- do_function() and do_call() -------- #
def do_function(envs, args):
    # define function
    assert len(args) == 2
    params = args[0]
    body = args[1]
    return ["function", params, body]

@logging
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

# -------- envs functions -------- #
def envs_get(envs, name, index=None):
    """
    get defined function from the top most possible frame
    """
    assert isinstance(name, str)
    for e in reversed(envs):
        if name in e:
            if index == None:
                return e[name]
            else:
                return e[name][index]

    assert False, f"Error: Unknown variable name {name}"


def envs_set(envs, name, value, i=None):
    """
    save variables and functions to envs
    """
    assert isinstance(name, str)

    if i == None:
        envs[-1][name] = value  # in the most local frame, assign value to key "name"
    else:
        envs[-1][name][i] = value

# -------- do_set() -------- #
def do_set(envs, args):
    assert len(args) == 2
    assert isinstance(args[0], str)
    var_name = args[0]
    value = do(envs, args[1])
    envs_set(envs, var_name, value)
    return value

# -------- do_get() -------- #
def do_get(envs, args):
    assert len(args) == 1
    return envs_get(envs, args[0])

# -------- do_sequence() -------- #
def do_sequence(envs, args):
    assert len(args) > 0
    for operation in args:
        result = do(envs, operation)
    return result

# -------- mathematical functions -------- #
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

def do_multiply(envs, args):
    """
    Multiplication with an arbitrary amount of numbers
    Args:
        envs: list of environments
        args: list of numbers with min length of 2

    Returns:
        product of numbers

    """
    assert len(args)>=2
    prod = 1
    for arg in args:
        assert isinstance(do(envs, arg), int) or isinstance(do(envs,arg),float)
        prod *= do(envs, arg)
    return prod

def do_division(envs, args):
    """
    division between two numbers
    Args:
        envs: list of environments
        args: [number1: int or float, number2: int or float]

    Returns:
        Division of number1 / number2
    """
    assert len(args) == 2
    left = do(envs, args[0])
    right = do(envs, args[1])
    assert right!=0, "Error: Division by zero"
    return left / right

def do_power(envs, args):
    """
    power of two numbers
    Args:
        envs: list of environments
        args: [number1: int or float, number2: int or float]

    Returns:
        number1 ** number2

    """
    assert len(args) == 2
    base = do(envs, args[0])
    exponent = do(envs, args[1])
    return base ** exponent

# -------- do_print() -------- #
def do_print(envs, args):
    """
    prints everything
    Args:
        envs: list of environments
        args: Any input is possible

    Returns:
        print for all given args

    """
    for arg in args:
        print(do(envs, arg))

# -------- do_while() -------- #
def do_while(envs, args):
    """

    Args:
        envs: list of environments
        args: [cond_var: int or float, operator: str, count_var: int or float, statement: sequence]

    Returns:
        None
    """
    assert len(args) == 4
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

# -------- do_array() -------- #
def do_array(envs, args):
    """
    Array operations: create new array of fixed size, get value at index i, set value at index i
    Arrays have name as key and a list ["array", size, list of fixed size ] as value in e in envs
    
    Args:
        envs: list of environments
        args: list of arguments - args[0] = "array", args[1] = operation, args[2] = name, args[3] = value

    
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

# -------- do_dict() -------- #
def do_dict(envs, args):
    """
       dict operations: create new dict, get value of key in dict, set value in key in dict, merge two dicts
    """

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

# -------- do_class -------- #
def do_class(envs, args):


    def class_define(envs, args):
        """
        Define new class
        Args:
            envs: list of environments
            args: [classname:str, attributes:list, methods:list, parent:string(default=None]
        Returns:
            None
        """
        assert args[0] not in envs, f"Class {args[0]} already exists!"
        assert (len(args) >= 3), "Missing arguments!"
        assert isinstance(args[1], list)
        assert isinstance(args[2], list)
        class_dict = {
            "_classname": args[0],
            "_attributes": {attr: None for attr in args[1]},
            "_methods": {method: None for method in args[2]},
            "_parent": args[3] if args[3]!="null" else None
            # Sets the value of parent to None, if no other value is added, so that it is possible to check for val later
        }
        if class_dict["_parent"] != None:  # If "parent"!=None
            parent = envs_get(envs, args[3])

            parent_atrr_dict = {att_list: value for att_list, value in parent["_attributes"].items() if att_list.startswith("_")}
            current_atrr_dict=class_dict["_attributes"]
            merged_attributes = parent_atrr_dict | current_atrr_dict

            parent_methods_dict = {met_list: value  for met_list, value in parent["_methods"].items() if met_list.startswith("_")}
            current_methods_dict=class_dict["_methods"]
            merged_methods= parent_methods_dict | current_methods_dict

            class_dict["_attributes"] = merged_attributes  # merge parent and child attributes
            class_dict["_methods"] = merged_methods  # merge parent and child methods

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
                if key.startswith("_"):
                    attributes[key] = parameters[i]
                    i += 1

        envs_set(envs,instance_name,data_c)

    def class_set_attributes(envs, args):
        """
        set attributes of a given instance of class
        Can set multiple values with one call
        

        Args: 
            envs: list of environments
            args: [instance_name: str, attribute_name_1, value1, ...]
        Return:
            to be determined, temporarily None
        """
        maxlen = len(args[1:])
        assert maxlen%2==0, "invalid syntax: set_attributes requires attribute-value pairs"
        for i in range(1,maxlen,2):
            att = do(envs, args[i])
            value = do(envs, args[i+1])
            data = envs_get(envs,args[0])#get the dictionary containing data of the instance variable, assert in envs_get
            name = args[0] #instance name

            assert type(data["_attributes"])==dict, f"{args[0]} has no attribute"
            copy = data.copy()
            if att in data["_attributes"].keys(): #if it is an existing attribute:
                copy["_attributes"][att] = value #set value in attributes dictionary at index attribute_name (att)
                envs_set(envs,name,copy)
            else: #if it is a new attribute
                copy["_attributes"][att] = value #append value in attributes dictionary at index attribute_name (att)
                envs_set(envs,name,copy)

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
            body = do(envs,args[i+1]) # body = list ["function",[params],body]
            assert body[0] == "function", f"{methodname} should be defined as a function"

            name = args[0] #place holder for class_name
            data = envs_get(envs,name) #get the dictionary containing data of the instance variable, assert in envs_get
            assert type(data) == dict, f"{name} doesnt have methods"

            copy = data.copy()
            copy["_methods"][methodname] = body #set value in methods dictionary at index method_name (att)
            envs_set(envs,name,copy)


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
        data=envs_get(envs,name)

        assert type(data["_attributes"]) == dict, f"{args[0]} has no attribute"
        assert att in data["_attributes"].keys(), f"invalid syntax: No attribute {att} found in {args[0]}"
        return data["_attributes"][att]

    @logging
    def class_get_methods(envs, args):
        """
        get method of a given instance of class
        Executes the method with provided input parameters
        returns the value that is produced

        Args: 
            envs: list of environments
            args: [instance_name: str, method_name: str, args: values]
        Return:
            to be determined, temporarily method body of the method
        """
        name = args[0]  # instance name
        method_name = args[1]
        data= envs_get(envs,name)

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
        get parent class of a class or the class of an instance

        params:
            envs: list of dicts, stack (list) of frames with dictionary as element
            args: list of arguments ["objname"]

        return:
            "parent": str, parent class name

        '''
        name = args[0]
        data = envs_get(envs, name)
        return data["_parent"]

    # introspection in do_class()
    d = locals().copy()
    OPERATIONS_CLASS = {}
    for k in d:
        if k.startswith("class_"):
            OPERATIONS_CLASS[k.replace("class_", "")] = d[k]

    assert args[0] in OPERATIONS_CLASS, f"Unknown operation {args[0]}"
    func = OPERATIONS_CLASS[args[0]]
    return func(envs, args[1:])

# -------- introspection with do_ -------- #
OPERATIONS = {
    func_name.replace("do_", ""): func_body
    for (func_name, func_body) in globals().items()
    if func_name.startswith("do_")
}

# -------- do() -------- #
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

# -------- main --------- #
def main_in_funcs_demo():
    with open(sys.argv[1], "r") as source_file:
        program = json.load(source_file)
    assert isinstance(program, list)
    envs = [{}]
    result = do(envs, program)
    print(f"=> {result}")


def main():

    with open("trace_file.log","w") as f:
        f.write("id,function_name,event,timestamp\n")
    main_in_funcs_demo()


if __name__ == "__main__":
    main()
