from flask import Flask, render_template, request, jsonify
import re
import ast
import operator
import math

app = Flask(__name__)

# Allowed math functions
ALLOWED_FUNCTIONS = {
    'sqrt': math.sqrt,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'log': math.log10,
    'ln': math.log
}

# Allowed constants
ALLOWED_CONSTANTS = {
    'pi': math.pi,
    'e': math.e
}

# Allowed operators
operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg
}


def safe_eval(node):

    if isinstance(node, ast.Num):
        return node.n

    elif isinstance(node, ast.BinOp):
        left = safe_eval(node.left)
        right = safe_eval(node.right)
        op = operators[type(node.op)]
        return op(left, right)

    elif isinstance(node, ast.UnaryOp):
        operand = safe_eval(node.operand)
        op = operators[type(node.op)]
        return op(operand)

    # function calls (sin, sqrt, log...)
    elif isinstance(node, ast.Call):
        func_name = node.func.id

        if func_name in ALLOWED_FUNCTIONS:
            args = [safe_eval(arg) for arg in node.args]
            return ALLOWED_FUNCTIONS[func_name](*args)

        else:
            raise ValueError("Function not allowed")

    # constants (pi, e)
    elif isinstance(node, ast.Name):

        if node.id in ALLOWED_CONSTANTS:
            return ALLOWED_CONSTANTS[node.id]

        else:
            raise ValueError("Constant not allowed")

    else:
        raise ValueError("Invalid expression")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    expression = request.json.get("expression", "")

    expression = re.sub(r'\b0+(\d+)', r'\1', expression)

    try:
        node = ast.parse(expression, mode='eval').body
        result = safe_eval(node)
        return jsonify({"result": result})
    except:
        return jsonify({"result": "Error"})


if __name__ == '__main__':
    app.run(debug=True)