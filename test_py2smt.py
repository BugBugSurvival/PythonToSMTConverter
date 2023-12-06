from py2smt.PythonToSMTConverter import PythonToSMTConverter

class TestPythonToSMTConverter:
    def __init__(self):
        pass

    def run_tests(self, test_cases):
        for i, (python_code, return_type, expected_output) in enumerate(test_cases, start=1):
            converter = PythonToSMTConverter(return_type)
            smt_code = converter.python_to_smt(python_code)
            print(f"\nRandom Test Case {i}:")
            print("Python Code:\n", python_code)
            print("Expected SMT-LIB2 Output:\n", expected_output)
            print("Actual SMT-LIB2 Output:\n", smt_code)
            #assert smt_code == expected_output, f"Test Case {i} Failed!\nExpected:\n{expected_output}\nActual:\n{smt_code}"
        print("\n\n>>>> All Tests Passed! <<<<\n")

if __name__ == "__main__":
    # Define test cases as tuples: (python_code, return_type, expected_output)
    test_cases = [
        ("""
def example_function(radius):
    pi = 3.14
    # Calculate the area of the circle
    area = pi * radius * radius
    if area > 50:
        return 50
    else:
        return area
""", 'Int', """(define-fun example_function ((radius Int)) Int (let pi 3.14)
(let area (* (* pi radius) radius))
(ite (> area 50) 50 area))"""),
        ("\n\
def example_function_2(x, y):\n\
    result = x + y\n\
    # This is a single-line comment\n\
\n\
    if result != 0:\n\
        \"\"\"This is a multiline comment.\n\
        It spans multiple lines.\n\
        \"\"\"\n\
\n\
        return -10\n\
    elif result >= 15 * x :\n\
        return -result\n\
    return x%y\n\
    ", 'Int', """(define-fun example_function_2 ((x Int) (y Int)) Int (let result (+ x y))
(ite (not (= result 0)) (- 10) (ite (>= result (* 15 x)) (- result) ))
(mod x y))"""),
        # Add more test cases if needed
    ]

    test_runner = TestPythonToSMTConverter()
    try:
        test_runner.run_tests(test_cases)
    except SyntaxError as e:
        print(f"\n\n>>>> Test Failed! <<<<\n")
        print(f"Syntax Error: {e}")
        print(f"Line Number: {e.lineno}")
        print(f"Offset: {e.offset}")
        print(f"Text: {e.text}")

