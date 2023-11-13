# lgl-interpreter

***
## logging():
logging is a decorator which returns a function called wrapper. This function is the main function. First it gets an id with the get_id() function, then it checks if legal_input() is equal to four. If it isn't the function from logging is run normally.
But if it is it first gets the method name by checking which function is called (because the name is not necessarily at the same position). 
Then it calles the second function with status=start in logging which is called log_entry() where the entry into the log file is done. Then the function is run.
After that log_entry is called again, but with the status=end

### legal_input():
This is a helper function for logging that checks if --trace is in the input which would mean that it needs logging.
If the length is 2 then no logging is aquired and it returns 2, if not it checks if "--trace" is the additional input and then returns 4.

### get_id():
This function generates a random id between the number 10000 and 100000. This id is then added into the ids list, if the generated id is already in the list then it generates a new id until it is not in the list anymore.
This is also a helper function for logging and returns an unnique id
***
## math functions:
***
## do_array(envs,args):
***
## do_dict(envs,args):
is an upper function in which specified functions for dict operations are defined. This is useful for using introspection in the function itself by using locals().
### dict_new(envs,args):
    input: 	envs: environment
            args: ["name"]
creates a new dictionary and sets it in the environment using envs_set
	
### dict_get_value(envs,args):
    input: 	envs: environment
            args: ["name","key"]
gets the dict out of the environment and returns the value of the given key. If the key is not in the dictionary a Error message is printed.

### dict_set_value(envs,args):
    input:	env: environment
            args: ["name","key","value"]
gets the dict out of the environment and sets a new key value pair in the dictionary

### dict_merge(envs,args):
    input:	env: environment
            args: ["name", "dict1","dict2"]
Takes two dictionarys as input, merges them under the new dictionary name and sets the new dictionary with envs_set()
***
## do_class(envs,args):

### class_instantiate(envs,args):
    input:	envs: list of environments
            args: [instance_name:str, class_name:str,parameters]
Creates a new instance with the class given in the input. It gets he same dictionary as the class has, if any parameters are given then it iterates through the attributes, if an attribute starts with "_" then it is an instance attribute and the value of parameters is assigned to it.
After assigning all attributes the new instance is set in the environment

***
## do():
***
## main_in_funcs_demo:
***