{theme=documentation}

\include{"../include.md"}

MiniFlask modules need to be declared in their ``\_\_init\_\_.py`` by calling the `register(mf)` function. The register function offers a range of ways to declare local and global variables. 


# Module declaration
Register (local) Variables For the Module

## Local variables
MiniFlask offers the possibility to declare local variables with default values that are listed upon loading the module and can be overwritten by commando-line arguments.

**Example File:** `modules/module1/__init__.py`
```python
def register(mf):
    mf.register_defaults({
        "variableA": 42,
        "variableB": "Hello",
        "variableC": True,
        "variableD": [1,2,3,5,8,13] # only lists of same type are supported
    })
```

Local variables can be called inside a module by `state["variableA"]` or outside a module by `state.all["module1.variableA"]` (see [State](../05-State/index.md)).

**Note:** Multiple calls to `register_defaults` are allowed.
---

## Helper Variables
If local variables are never to be overwritten by cli-arguments or printed when launching MiniFlask, helper variables come handy.

**Example File:** `modules/module2/__init__.py`
```python
def register(mf):

    class A():
        pass
    mf.register_helpers({
        "variable": A(), # cannot be changed using argument parsers
    })
```
Helper variables can be called just as local variables.
## Global Variables
Global variables behave similar to local variables, but live in a global namespace. 

**Example File:** `modules/module2/__init__.py`
```python
def register(mf):
    mf.register_globals({
        "global_var": "this variable is global",
    })
```
Global variables can be accessed from any module by calling `state.all[global_var]`.

**Note**: `mf.register_globals(...)` is equivalent to a call of `mf.register_defaults(...,scope="")`.  
\n



**Note**: `mf.register_helpers(...)` is equivalent to a call of `mf.register_defaults(...,cliargs=False)`.  
\n

## Required local Arguments
Set any base type (`str`, `bool`, `int`, `float`) or list of any base type as default to register an argument that has to be specified by the user.
```python
def register(mf):
    mf.register_defaults({
        "variableA": int,
        "variableB": str,
        "variableC": bool,
        "variableD": [float] # only lists of same type are supported
    })
```


### Argument Parser
Whenever we load `module1`, e.g. by using 
```shell
python main.py module1
```
we also load these variables into the argument parser of miniflask.  
For the example above, we list all arguments that can be used for `module1`:
```shell
> python main.py module1 -h
usage: main.py modulelist [optional arguments]

optional arguments:
  -h, --help            show this help message and exit
  --module1.variableA 	int
  --module1.variableB 	string
  --module1.variableC
  --no-module1.variableC
  --module1.variableD	[int]
```

Thus, to turn `variableC` off, we can just add `--no-module1.variableC` to the above command.

### Argument Types
For a boolean typed variable, the following arguments are possible:

| **Set to True**  | **Set to False** |
| ---------------- | ---------------- |
| \block[
```
--module.var
--module.var true
--module.var TrUe (well, boolean values are case insensitive)
--module.var yes
--module.var y
--module.var t
--module.var 1
```
] | \block[
```
--no-module.var
--module.var false
--module.var FalSE (well, boolean values are case-insensitive)
--module.var no
--module.var n
--module.var f
--module.var 0
```
] |

List arguments are just as easy as
```
--module.var 1 2 3 4 5
```

### Common Scopes
Groups of Modules often share variables. (Either by functionality, or, by conceptional classification).  
The method `register_defaults` has the optional argument `scope`. This variable defaults to the unique module id of the current module.
Overwriting the variable allows for shared or global settings.

**Example File:** `modules/module2/__init__.py`
```python
def register(mf):
    mf.set_sccope("common")
    mf.register_defaults({
        "varA": 42,
    })
```
This variable is identified in the global scope by `common.varA` instead of `module2.varA`.
**Note**: `mf.set_scope()` sets the scope globally (also in the event states).

**Alternative**:
```python
    mf.register_defaults({
        "varA": 42,
    }, scope="common")
```
This variable is identified in the global scope by `common.varA` instead of `module2.varA`.

\n



### Overwrite Settings of other Modules
A module can be used as a preset of other modules with predefined settings.  

**Example File:** `modules/module2/__init__.py`
```python
def register(mf):
    mf.load("module1") # module dependency
    mf.overwrite_defaults({
        "module1.variableB": "overwrites variable of module1",
    })
```

**Note**: `mf.overwrite_defaults(...)` is equivalent to a call of `mf.register_defaults(...,overwrite=True)`.  
In case any variable to overwrite is not known, the method will throw an Exception (`ValueError`).
**Note**: `mf.register_defaults` would also overwrite variables, however, it would not raise an Exception if the variable is not known.
\n




### Settings-Dependent Settings
On variable definition, all variables can be initialized using a lambda. This lambda retrieves the global `state`- and `event`-Objects to allow for settings dependdent settings

**Example File:** `modules/module2/__init__.py`
```python
def register(mf):
    mf.register_defaults({
        # unless anything is overwritten in the cli, this variable would be 420
        "variable": lambda state,event: state["module1.variableA"] * 10
    })
```
