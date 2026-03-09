from flask import Flask, render_template, request, jsonify
import re
import ast
import operator
app = Flask(__name__)
operators = {
    ast.Add : operator.add,
    ast.Sub : operator.sub,
    ast.Mult : operator.mul,
    ast.Div : operator.truediv,
    ast.USub : operator.neg
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
        return jsonify({"result":result})
    except:
        return jsonify({"result":"Error"})




if __name__ == '__main__':
    app.run(debug=True)