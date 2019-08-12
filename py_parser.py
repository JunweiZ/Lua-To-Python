# Covert AST to Python AST

import ast


def ast_to_py_ast(nodes):
    ast_ = parse_nodes(nodes)

    bootstrap = [
        ast.ImportFrom(
            module='core', names=[
                ast.alias(name='*', asname=None)
            ],
            level=0
        )
    ]

    ast_ = bootstrap + ast_

    tree = ast.Module(ast_)
    tree = ast.fix_missing_locations(tree)
    return tree


def parse_nodes(nodes):
    out = []
    while len(nodes) > 0:
        node = nodes.pop(0)

        if node["type"] == "table":
            argument_nodes = []
            keyword_nodes = []

            for x in node["value"]:
                if not (x["type"] == "call" and x["name"] == "="):
                    argument_nodes.append(x)
                    continue

                keyword_nodes.append(x)

            key_nodes = [x["args"][0] for x in keyword_nodes]
            # Convert name references to strings
            key_nodes = [
                {"type": "string", "value": x["name"]}
                    if x["type"] == "name" else x
                for x in key_nodes
            ]

            value_nodes = [x["args"][1] for x in keyword_nodes]
            value_nodes = [x[0] for x in value_nodes]
            value_nodes = parse_nodes(value_nodes)

            keywords = []
            for x in (zip(key_nodes, value_nodes)):
                name_node, value_node = x
                name = name_node["value"]

                # Apply __ to make sure its casted in Table
                if name_node["type"] == "number":
                    name = "__{0}".format(name)

                keywords.append(
                    ast.keyword(arg=name, value=value_node)
                )

            out.append(
                ast.Call(
                    func=ast.Name(id='Table', ctx=ast.Load()),
                    args=parse_nodes(argument_nodes),
                    keywords=keywords,
                )
            )
            continue


        if node["type"] == "string":
            out.append(ast.Str(s=node["value"]))
            continue

        if node["type"] == "boolean":
            value = node["value"]
            value = True if value == "true" else value
            value = False if value == "false" else value
            out.append(ast.NameConstant(value=value))
            continue

        if node["type"] == "number":
            value = node["value"]
            value = float(value) if "." in value else int(value)

            out.append(ast.Num(n=value))
            continue

        if node["type"] == "nil":
            out.append(ast.NameConstant(value=None))
            continue

        if node["type"] == "return":
            out.append(
                ast.Return(value=parse_nodes(node["value"])[0])
            )
            continue

        if node["type"] == "assign":
            out.append(
                ast.Assign(
                    targets=[
                        ast.Name(id=node["name"], ctx=ast.Store())
                    ],
                    value=parse_nodes(node["value"])[0],
                )
            )
            continue

        if node["type"] == "name":
            out.append(
                ast.Name(id=node["name"], ctx=ast.Load())
            )
            continue

        if node["type"] == "expr":
            out.append(
                ast.Expr(
                    value=parse_nodes(node["value"])[0]
                )
            )
            continue

        if node["type"] == "function":
            body_nodes = parse_nodes(node["body"])
            out.append(
                ast.FunctionDef(
                    name=node["name"],
                    args=ast.arguments(
                        args=[
                            ast.arg(
                                arg=x["name"],
                                annotation=None,
                            ) for x in node["args"]
                        ],
                        vararg=None,
                        kwonlyargs=[],
                        kw_defaults=[],
                        kwarg=None,
                        defaults=[]
                    ),
                    body=body_nodes,
                    decorator_list=[],
                )
            )
            continue

        if node["type"] == "if":
            test_nodes = parse_nodes(node["test"])
            body_nodes = parse_nodes(node["body"])
            else_nodes = parse_nodes(node["else"])

            out.append(
                ast.If(
                    test=test_nodes[0],
                    body=body_nodes,
                    orelse=else_nodes,
                )
            )
            continue

        if node["type"] == "while":
            test_nodes = parse_nodes(node["test"])
            body_nodes = parse_nodes(node["body"])

            out.append(
                ast.While(
                    test=test_nodes[0],
                    body=body_nodes,
                    orelse=[],
                )
            )

        if node["type"] == "else":
            body_nodes = parse_nodes(node["body"])
            out = out + body_nodes
            continue

        if node["type"] == "call":
            if node["name"] == "#":
                out.append(
                    ast.Call(
                        func=ast.Name(id='len', ctx=ast.Load()),
                        args=parse_nodes(node["args"]),
                        keywords=[],
                    )
                )
                continue

            if node["name"] == "[":
                value_node = node["args"][0]

                if value_node["type"] == "call":
                    value_expression = parse_nodes([value_node])[0]
                else:
                    value_expression = ast.Name(
                        id=value_node["name"],
                        ctx=ast.Load(),
                    )

                out.append(
                    ast.Subscript(
                        value=value_expression,
                        slice=ast.Index(
                            value=parse_nodes(node["args"][1])[0]
                        ),
                        ctx=ast.Load(),
                    )
                )

                continue

            if node["name"] == "=":
                name_arg = node["args"][0]

                out.append(
                    ast.Assign(
                        targets=[
                            ast.Name(id=name_arg["name"], ctx=ast.Store())
                        ],
                        value=parse_nodes(node["args"][1])[0],
                    )
                )
                continue

            if node["name"] in ["-", "%", "+", "..", "*", "/"]:
                ops = node["name"]

                arg_left = parse_nodes([node["args"][0]])
                arg_right = parse_nodes(node["args"][1])

                ops_ref = {
                    "-": ast.Sub,
                    "%": ast.Mod,
                    "+": ast.Add,
                    "..": ast.Add,
                    "*": ast.Mult,
                    "/": ast.Div,
                }

                out.append(
                    ast.BinOp(
                        left=arg_left[0],
                        op=ops_ref[ops](),
                        right=arg_right[0],
                    )
                )
                continue

            if node["name"] in ["and", "or"]:
                ops = node["name"]

                arg_left = parse_nodes([node["args"][0]])
                arg_right = parse_nodes(node["args"][1])

                ops_ref = {
                    "and": ast.And,
                    "or": ast.Or,
                }

                out.append(
                    ast.BoolOp(
                        op=ops_ref[ops](),
                        values=[
                            arg_left[0],
                            arg_right[0],
                        ]
                    )
                )
                continue

            if node["name"] in [">", "<", "~=", "==", "<=", ">="]:
                ops = node["name"]

                arg_left = parse_nodes([node["args"][0]])
                arg_right = parse_nodes(node["args"][1])

                ops_ref = {
                    ">": ast.Gt,
                    ">=": ast.GtE,
                    "<": ast.Lt,
                    "<=": ast.LtE,
                    "~=": ast.NotEq,
                    "==": ast.Eq,
                }

                out.append(
                    ast.Compare(
                        left=arg_left[0],
                        ops=[ops_ref[ops]()],
                        comparators=arg_right,
                    )
                )
                continue

            if node["name"] == "not":
                out.append(
                    ast.UnaryOp(
                        op=ast.Not(),
                        operand=parse_nodes(node["args"])[0]
                    )
                )
                continue

            out.append(
                ast.Call(
                    func=ast.Name(id=node["name"], ctx=ast.Load()),
                    args=parse_nodes(node["args"]),
                    keywords=[]
                )
            )
            continue

    return out
