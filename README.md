# Lua to Python

This is a project where I attempt to convert Lua to Python, by transforming Lua into Python AST and then running it.


## Current status
- Variable assignments, basic datatypes and comparisons, if statements, while loops and functions are working.


## Getting started

- `pip install -r requirements.txt`

```
Usage: compile.py [OPTIONS] SOURCE_FILE

Options:
  --strip_comments INTEGER  Remove comments from tokens
  --tokens INTEGER          Show tokens generated by lexer
  --ast INTEGER             Show the internal AST (later transformed to Python
                            AST
  --py_ast INTEGER          Show Python AST
  --py_code INTEGER         Show generated Python code
  --help                    Show this message and exit.
```

Example: `./compile.py --strip-comments=1 examples/functions.lua`


## Roadmap
- [x] Single line comments
- [x] Multiline comments
- [x] Numbers
- [x] Strings
- [x] Nil types
- [x] Variable assignments
- [x] Addition
- [x] Multiplication
- [x] If statements
- [x] Nested if statements
- [x] `~=`  operator
- [x] `==`  operator
- [x] `while` keyword
- [x] Concat strings with `..`
- [x] Subtract values
- [x] `>=` operator
- [x] `<=` operator
- [x] Boolean types
- [x] `function` declarations
- [x] `return`
- [x] `not` logical operator
- [x] `bool` expression in comparison
- [x] `%` operator
- [x] `/` operator
- [x] `or` logical operator
- [x] `and` logical operator
- [x] Assign function return to variable
- [x] Double number support
- [x] Negative values
- [x] Anonymous functions
- [ ] `_G` for globals access
- [ ] Table datatype
- [ ] `for` keyword
- [ ] `repeat` keyword
- [ ] Short circuit / tenary operator
- [ ] `local` variables
- [ ] Numbers beginning with `.` (ex `.123`)
- [ ] Undefined variables should return nil
- [ ] `#` operator for retrieving Table/String length
- [x] Add multiline line support to anonymous functions


## References
- https://drew.ltd/blog/posts/2020-7-18.html - Many thanks for Drew and his excellent articles on how to build a programming language
- https://greentreesnakes.readthedocs.io/en/latest/
- https://github.com/python/cpython/blob/master/Lib/ast.py
- https://learnxinyminutes.com/docs/lua/
