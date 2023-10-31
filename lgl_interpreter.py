import sys
import json

#---from funcs-demo in session 4---
def do_funktion(envs,args):
    #define function
    assert len(args) == 2
    params = args[0]
    body = args[1]
    return ["funktion",params,body]

def do_aufrufen(envs,args):
    #call function
    assert len(args) >= 1
    name = args[0]
    arguments = args[1:]
    # eager evaluation
    values = [do(envs,arg) for arg in arguments]

    func = envs_get(envs,name)
    assert isinstance(func,list)
    assert func[0] == "funktion"
    func_params = func[1]
    assert len(func_params) == len(values) #assert values passed to func is same as values required by definition

    local_frame = dict(zip(func_params,values)) # dict of param name and values
    envs.append(local_frame) #push this local frame/ dict to top of envs
    body = func[2] 
    result = do(envs,body)
    envs.pop()

    return result

def envs_get(envs, name, index = None):
    #get defined function from the top most possible frame
    assert isinstance(name,str)
    for e in reversed(envs):
        if name in e:
            if index == None:
                return e[name]
            else:
                return e[name][index]
        
    assert False, f"Unknown variable name {name}"

def envs_set(envs,name,value, i = None):
    #save variables and functions to 
    #paul adds the possibility to add lists and dictionaries
    #variables have name as key and default data type value as value
    #functions have name as key and a list ["Funktion", "params", "body"] as value
    #arrays have name as key and a list ["array", size, list of fixed size ] as value

    assert isinstance(name,str)

    if i==None:
        envs[-1][name] = value #in the most local frame, assign value to key "name"
    else:
        envs[-1][name][i] = value


def do_setzen(envs,args):
    assert len(args) == 2
    assert isinstance(args[0],str)
    var_name = args[0]
    value = do(envs,args[1])
    envs_set(envs,var_name, value)
    return value

def do_abrufen(envs,args):
    assert len(args) == 1
    return envs_get(envs,args[0])

def do_addieren(envs,args):
    assert len(args) == 2
    left = do(envs,args[0])
    right = do(envs,args[1])
    return left + right

def do_absolutwert(envs,args):
    assert len(args) == 1
    value = do(envs,args[0])
    return abs(value)

def do_subtrahieren(envs,args):
    assert len(args) == 2
    left = do(envs,args[0])
    right = do(envs,args[1])
    return left - right

def do_abfolge(envs,args):
    assert len(args) > 0
    for operation in args:
        result = do(envs,operation)
    return result




#--- end of funcs-demo in session 4---

#----------to implement in 1---------------

def do_multiply():
    pass

def do_division():
    pass

def do_power():
    pass

def do_print():
    pass

def do_while():
    #Exercise in book, book says use python while or recursion
    #==, !=, <, >
    pass

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
        equivalent to do_funktion and setzen

        Args: 
            envs: environment
            args: [name: str, n: int]
        Return:
            None
        """
        assert len(args) == 2
        assert isinstance(args[0], str) and isinstance(args[1], int)

        res = [None]*args[1]
        envs_set(envs, args[0], res)
        return ["array", args[1], res]

    
    def array_get(envs, args):
        """
        get the value of array at certain index
        equivalent to do_abrufen

        Args: 
            envs: environment
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
        Equivalent to do_setzen

        Args: 
            envs: environment
            args: [name: str, i: int, val: value]
        Return:
            int - value at name[i]
        """
        assert len(args) == 3
        assert isinstance(args[0], str) and isinstance(args[1], int)
        array_name = args[0]
        i = args[1]
        value = do(envs,args[2])        
        envs_set(envs, array_name, value, i) #check index passed to envs_set
        return value


    #introspection in do_array()
    d = locals().copy()
    OPERATIONS_ARRAY = {}
    for k in d:
        if k.startswith("array_"):
            OPERATIONS_ARRAY[k.replace("array_","")] = d[k]

   
    assert args[0] in OPERATIONS_ARRAY, f"Unknown operation {args[0]}"
    func = OPERATIONS_ARRAY[args[0]]
    return func(envs, args[1:])




def do_dictionary():
    pass



#---------end of 1, put over do() when done?-----


#-----OPERATIONS and do() from funcs-demo.py in session 4------------

OPERATIONS = {
    func_name.replace("do_",""): func_body
    for (func_name, func_body) in globals().items()
    if func_name.startswith("do_")
}


def do(envs,expr):
    if isinstance(expr,int):
        return expr
   
    assert isinstance(expr,list)
    assert expr[0] in OPERATIONS, f"Unknown operation {expr[0]}"
    func = OPERATIONS[expr[0]]
    return func(envs, expr[1:])

#----end OPERATIONS and do() -----------------------

#--------- 2 Object System ------------

#define Shape, Square, Circle, see session 2

#------------------------------



#--------- 3 Logging -----------

#Use decorator in chapter 9

#-----------------------------



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
    assert argv_len%2==0, error_message
    assert (argv_len == 2 or argv_len == 4), error_message
    if argv_len == 2:
        print("argv_len == 2")
        return argv_len
    else:
        print("argv_len == 4")
        assert sys.argv[2] == "--trace", error_message
        return argv_len

        

    


def main_in_funcs_demo():

    assert len(sys.argv) == 2, "Usage: funcs-demo.py filename.gsc"
    with open(sys.argv[1], "r") as source_file:
        program = json.load(source_file)
    assert isinstance(program,list)
    envs = [{}]
    result = do(envs,program)
    print(f"=> {result}")

def main():
    #legal_input()
    #continue implementation
    main_in_funcs_demo()



if __name__ == "__main__":
    main()