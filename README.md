# PythonToSMTConverter

PythonToSMTConverter is a Python module for converting Python code to the SMT-LIB2 format.

## Table of Contents
- [Usage](#usage)
- [Example](#example)


## Usage
Here's an example of how to use PythonToSMTConverter with a sample Python code:

```python
from py2smt.PythonToSMTConverter import PythonToSMTConverter

# Convert Python code to SMT-LIB2
python_code = """
def example_function(x, y):
    result = x + y
    if result > 0:
        return result
    else:
        return -result
"""
# Create an instance of the PythonToSMTConverter
converter = PythonToSMTConverter(return_type='Int')

smt_code = converter.python_to_smt(python_code)
print("SMT-LIB2 Code:\n", smt_code)
```
### Running Tests
To run the test file (test_py2smt.py), execute the following command:
```bash
python test_py2smt.py
```

## Example

### Random Test Case 1:

**Python Code:**
```python
def example_function(radius):
    pi = 3.14
    # Calculate the area of the circle
    area = pi * radius * radius
    if area > 50:
        return 50
    else:
        return area
```
**Expected SMT-LIB2 Output:**
```smt
(define-fun example_function ((radius Int)) Int (let pi 3.14)
    (let area (* (* pi radius) radius))
    (ite (> area 50) 50 area))
```

### Random Test Case 2:

**Python Code:**
```python
def example_function_2(x, y):
    result = x + y
    # This is a single-line comment

    if result != 0:
        """This is a multiline comment.
        It spans multiple lines.
        """

        return -10
    elif result >= 15 * x :
        return -result
    return x % y
```
**Expected SMT-LIB2 Output:**
```smt
(define-fun example_function_2 ((x Int) (y Int)) Int (let result (+ x y))
    (ite (not (= result 0)) (- 10) (ite (>= result (* 15 x)) (- result) ))
    (mod x y))
```
Feel free to customize this example to better fit your specific documentation needs.

