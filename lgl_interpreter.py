import sys
import json

#---from funcs-demo in session 4---
def do_funktion(envs,args):
    assert len(args) == 2
    params = args[0]
    body = args[1]
    return ["funktion",params,body]

def do_aufrufen(envs,args):
    assert len(args) >= 1
    name = args[0]
    arguments = args[1:]
    # eager evaluation
    values = [do(envs,arg) for arg in arguments]

    func = envs_get(envs,name)
    assert isinstance(func,list)
    assert func[0] == "funktion"
    func_params = func[1]
    assert len(func_params) == len(values)

    local_frame = dict(zip(func_params,values))
    envs.append(local_frame)
    body = func[2]
    result = do(envs,body)
    envs.pop()

    return result

def envs_get(envs, name):
    assert isinstance(name,str)
    for e in reversed(envs):
        if name in e:
            return e[name]
        
    # python like version
    # if name in envs[-1]:
    #    return e[name]
    #if name in envs[0]:
    #    return e[name]
    assert False, f"Unknown variable name {name}"

def envs_set(envs,name,value):
    assert isinstance(name,str)
    # for e in reversed(envs):
    #     if name in e:
    #         e[name] = value
    #         return
    envs[-1][name] = value
        


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
    pass

def do_array():
    """
    Array operations: create new array of fixed size, get value at index i, set value at index i
    
    Args:
        
    
    Returns:
        arr: the array if a new array is created
        val: the value at index i
        None: set new value at index i
    """

    pass

def do_dictionary(env,args):
    def dict_new(env, args):
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
        envs_set(env, dict_name, {})

    def dict_get_value(env, args):
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
        dict = envs_get(env, dict_name)
        if key not in dict:
            print(f"Error: key {key} not in dictionary {dict_name}")
        else:
            value = dict[key]
            return value

    def dict_set_value(env, args):
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
        dict = envs_get(env, dict_name)
        dict[key] = value

    def dict_merge(env, args):
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
        dict1 = envs_get(env, dict_name1)
        dict2 = envs_get(env, dict_name2)
        merged = dict1 | dict2
        envs_set(env, new_dict, merged)

    variables = locals().copy()
    OPERATIONS_DICT = {}
    for k in variables:
        if k.startswith("dict_"):
            OPERATIONS_DICT[k.replace("dict_", "")] = variables[k]


    assert args[0] in OPERATIONS_DICT, f"Unknown operation: {args[0]}"
    func = OPERATIONS_DICT[args[0]]
    return func(env, args[1:])




#---------end of 1, put over do() when done?-----




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
    legal_input()
    #continue implementation

if __name__ == "__main__":
    main()