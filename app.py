from flask import Flask, render_template, request, jsonify
import re
import ast
import operator
import math

app = Flask(__name__)

ALLOWED_FUNCTIONS = {
    'sqrt': math.sqrt,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'log': math.log10,
    'ln': math.log,
    'abs': abs,
}

ALLOWED_CONSTANTS = {
    'pi': math.pi,
    'e': math.e,
}

OPERATORS = {
    ast.Add:  operator.add,
    ast.Sub:  operator.sub,
    ast.Mult: operator.mul,
    ast.Div:  operator.truediv,
    ast.Pow:  operator.pow,
    ast.Mod:  operator.mod,      # ← fixes % button
    ast.USub: operator.neg,
}


def safe_eval(node):
    # Python 3.8+ uses ast.Constant; ast.Num is deprecated/removed
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    elif isinstance(node, ast.BinOp):
        left  = safe_eval(node.left)
        right = safe_eval(node.right)

        if isinstance(node.op, ast.Div) and right == 0:
            raise ValueError("Division by zero")

        op = OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError("Unsupported operator")
        return op(left, right)

    elif isinstance(node, ast.UnaryOp):
        operand = safe_eval(node.operand)
        op = OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError("Unsupported unary operator")
        return op(operand)

    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Invalid function call")
        func_name = node.func.id
        if func_name not in ALLOWED_FUNCTIONS:
            raise ValueError(f"Function '{func_name}' is not allowed")
        args = [safe_eval(arg) for arg in node.args]
        return ALLOWED_FUNCTIONS[func_name](*args)

    elif isinstance(node, ast.Name):
        if node.id not in ALLOWED_CONSTANTS:
            raise ValueError(f"Name '{node.id}' is not allowed")
        return ALLOWED_CONSTANTS[node.id]

    else:
        raise ValueError(f"Unsupported expression type: {type(node).__name__}")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"result": "Error", "message": "Invalid JSON"}), 400

    expression = data.get("expression", "").strip()
    if not expression:
        return jsonify({"result": "Error", "message": "Empty expression"}), 400

    # Strip leading zeros that would cause SyntaxError (e.g. 07 → 7)
    expression = re.sub(r'\b0+(\d+)', r'\1', expression)

    try:
        tree = ast.parse(expression, mode='eval')
        result = safe_eval(tree.body)

        # Guard against inf / NaN
        if isinstance(result, float):
            if math.isnan(result) or math.isinf(result):
                return jsonify({"result": "Error", "message": "Undefined result"})
            result = round(result, 10)      # suppress float noise
            # Convert clean floats to int (e.g. 4.0 → 4)
            if result == int(result):
                result = int(result)

        return jsonify({"result": result})

    except ValueError as e:
        return jsonify({"result": "Error", "message": str(e)})
    except (KeyError, TypeError) as e:
        return jsonify({"result": "Error", "message": "Invalid expression"})
    except ZeroDivisionError:
        return jsonify({"result": "Error", "message": "Division by zero"})
    except SyntaxError:
        return jsonify({"result": "Error", "message": "Syntax error in expression"})
    except Exception:
        return jsonify({"result": "Error", "message": "Unexpected error"})


if __name__ == '__main__':
    app.run(debug=True)