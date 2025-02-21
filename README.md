# python-example
This is a sample project with Python

## What is a Python Package?

A Python package is a way of organising related modules into a single directory hierarchy. It allows you to structure your Python code in a logical and manageable way. A package typically contains an `__init__.py` file, which can be empty or execute initialization code for the package. Packages enable modular programming and code reuse, making it easier to maintain and scale your projects.

### Example

Here is a simple example of a Python package structure:

```
my_package/
    __init__.py
    module1.py
    module2.py
```

In this example, `my_package` is the package, and it contains two modules: `module1.py` and `module2.py`. You can import these modules in your code as follows:

```python
from my_package import module1
from my_package import module2
```

Using packages helps keep your code organized and improves readability, especially for larger projects.