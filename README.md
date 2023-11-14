# lgl-interpreter

***

## General description

Our lgl_interpreter.py serves as an interpreter for an imaginative programming language we call The Ultimate Language (TUL). TUL syntax uses English as base language. 

***
## logging():
logging is a decorator which returns a function called wrapper. This function is the main function. First it gets an id with the get_id() function, then it checks if legal_input() is equal to four. If it isn't the function from logging is run normally.
But if it is it first gets the method name by checking which function is called (because the name is not necessarily at the same position). 
Then the first log entry is done with status equal to start. Then the function is run and after this the second log entry is done with status equal to stop.

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
The usage of data structure array in TUL is handled in this function. An array is a list-like data structure with fixed size. do_array() uses introspection to fetch functions that manipulate arrays. All functions that do so are named with prefix "array_". Valid index is of type int and valid value is of type int, float or str.



### array_new():

Creates an empty array of some fixed size. This array is saved to environment. 
Syntax in TUL: ["array","new","array_name","size"]

### array_get():

returns the value of an array at a certain index
Syntax in TUL: ["array","get","array_name","index"]

### array_set():

set the value of an array at a certain index.
Only one value can be set at each call.
Syntax in TUL: ["array","set","array_name","index","value"]




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

Every operation regarding the object system is handled here. The class operations are named with prefix "class_" to support introspection during execution. 

A class in TUL is represented by the following data structure in python:

classname = {
	"_classname": name
	"_attributes": dict of attributes
	"_methods": dict of methods
	"_parent": parent
	}

An instance called "objname" of the class "classname" has a similar structure:

objname = {
	"_classname": classname
	"_attributes": dict of attributes
	"_methods": dict of methods
	"_parent": classname
	}


We implicitly assume that TUL users name instance attributes with a prefix "_" for attributes that should be inherited. If a class inherits another class or if an object of some class is instantiated, then a new dictionary is created. The particular dictionary has a dictionary at key "_attributes", in which attributes with leading "_" in their name will be added to the set of keys. For example, assume class "Shape" has an attribute "_name", then upon defining class "Square" it will have the following structure:

 Square = {
	"_classname": Square
	"_attributes": {"_name": None, ... }
	"_methods": {...}
	"_parent": Shape
	}



### class_instantiate(envs,args):
    input:	envs: list of environments
            args: [instance_name:str, class_name:str,parameters]
Creates a new instance with the class given in the input. It gets he same dictionary as the class has, if any parameters are given then it iterates through the attributes, if an attribute starts with "_" then it is an instance attribute and the value of parameters is assigned to it.
After assigning all attributes the new instance is set in the environment

### class_set_attributes():

Assign values to existing or new attributes, supports setting multiple attribute values with one single call.
Attribute names to be inherited should have a leading "_" character.
Syntax in TUL: ["class","set_attributes","instance_name","attribute_name1", value1, "attribute_name2", value2]


### class_set_methods():

Assign user-defined TUL functions to methods dictionary of an object, supports setting multiple methods with one single call.
Method names to be inherited or make use of polymorphism should have a leading "_" character.
Syntax in TUL: ["class","set_methods","instance_name","method_name1", body1, "method_name2", body2]


### class_get_attributes():

Returns the value of an attribute that belongs to the specified instance.
It searches by using the attribute name as key and looks in the current class/ instance dictionary.
Syntax in TUL: ["class","get_attributes","instance_name","attribute_name"]


### class_get_methods():

Executes the method with specified parameters and returns the computed value. The parameters are passed sequencially.
Since the parameters can be function calls themselves, they will be passed to do() and the return value kept in a list.
Syntax in TUL: ["class","get_methods","instance_name","method_name","param1","param2"]


### class_parent():

Returns the parent of a class or the class of an instance. Returns None if class has no parent.
["class","get_methods","instance_name","method_name","param1","param2"]



***
## do():
Adopted implementation from funcs-demo.py in lecture.
***
## main_in_funcs_demo:
Adopted implementation from funcs-demo.py in lecture.

***


## example .gsc files


### exampe_operations.gsc 

This file showcases the usage of the extended capabilities: multiply, division, power, while, print, array and dictionary operations.
Print calls demonstrates how the values of at indices of arrays and dictionaries get modified. The template is modified such that it works with our interpreter.py.


### example_class.gsc

This file showcases the usage of class operations. It should imitate the example given in the task description.


### example_trace.gsc

This file showcases the usage of tracing. Sequencial, nested and recursive calls are built in.

