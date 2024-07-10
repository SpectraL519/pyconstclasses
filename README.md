# PyConstClasses

[![tests](https://github.com/SpectraL519/pyconstclasses/actions/workflows/tests.yaml/badge.svg)](https://github.com/SpectraL519/pyconstclasses/actions/workflows/tests)
[![format](https://github.com/SpectraL519/pyconstclasses/actions/workflows/format.yaml/badge.svg)](https://github.com/SpectraL519/pyconstclasses/actions/workflows/format)
[![coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/SpectraL519/f6cec4c4c8e1733cfe45f807918a128a/raw/covbadge.json)]()

<br />

## Overview

`PyConstClasses` is a python package containing const class decorators and utility. It allows for the creation constant and static constant classes by utilizing the annotations of the class definition.

<br />
<br />

## Table of contents

* Installation
* [Tutorial](#tutorial)
    * [Basic usage](#basic-usage)
    * [Common parameters](#common-parameters)
    * [Decorator-specific parameters](#decorator-specific-parameters)
* Examples
* [Dev notes](#dev-notes)
* [Licence](#licence)

<br />
<br />

## Tutorial

After installing the package, you have to import it to your python program:
```python
import constclasses as cc
```

### Basic usage

The core of the PyConstClasses package are the `const_class` and `static_const_class` decorators. Both of these decorators override the default behaviour of the `__setattr__` magic method for the decorated class so that it thors `cc.ConstError` when trying to modify the constant attribute of an instance.

* The `const_class` decorator allows you to define a class structure and create constant instances of the defined class:

    ```python
    # const_class_basic.py

    @cc.const_class
    class Person:
        first_name: str
        last_name: str

        def __repr__(self) -> str:
            return f"{self.first_name} {self.last_name}"


    if __name__ == "__main__":
        john = Person("John", "Doe")
        print(f"{john = }")

        try:
            john.first_name = "Bob"
        except cc.ConstError as err:
            print(f"Error: {err}")

        try:
            john.last_name = "Smith"
        except cc.ConstError as err:
            print(f"Error: {err}")
    ```

    This program will produce the following output:
    ```
    john = John Doe
    Error: Cannot modify const attribute `first_name` of class `Person`
    Error: Cannot modify const attribute `last_name` of class `Person`
    ```

* The `static_const_class` deacorator allows you to define a pseudo-static resource with const members (it creates an instance of the decorated class):

    ```python
    # static_const_class_basic.py

    @cc.static_const_class
    class ProjectConfiguration:
        name: str = "MyProject"
        version: str = "alpha"

        def __repr__(self):
            return f"Project: {self.name}\nVersion: {self.version}"


    if __name__ == "__main__":
        print(f"Project configuration:\n{ProjectConfiguration}")

        try:
            ProjectConfiguration.name = "NewProjectName"
        except cc.ConstError as err:
            print(f"Error: {err}")

        try:
            ProjectConfiguration.version = "beta"
        except cc.ConstError as err:
            print(f"Error: {err}")
    ```

    This program will produce the following output:
    ```
    Project configuration:
    Project: MyProject
    Version: alpha
    Error: Cannot modify const attribute `name` of class `ProjectConfiguration`
    Error: Cannot modify const attribute `version` of class `ProjectConfiguration`
    ```

> [!IMPORTANT]
> In the current version of the package the constant attributes have to be defined using annotations, i.e. the `member: type (= value)` syntax of the class member declaration is required

<br />

### Common parameters

Both const decorators - `const_class` and `static_const_class` - have the following parameters:

* `with_strict_types: bool`

    If this parameter's value is set to
    * `False` - the decorators will use the `attribute_type(given_value)` conversion, so as long as the given value's type is convertible to the desired type, the decorators will not raise any errors.
    * `True` - the decorators will perform an `isinstance(given_value, attribute_type)` check, the failure of which will result in raising a `TypeError`

    Example:
    ```python
    # common_with_strict_types.py

    @cc.const_class
    class Person:
        first_name: str
        last_name: str
        age: int

        def __repr__(self) -> str:
            return f"{self.first_name} {self.last_name} [age: {self.age}]"

    @cc.const_class(with_strict_types=True)
    class PersonStrictTypes:
        first_name: str
        last_name: str
        age: int

        def __repr__(self) -> str:
            return f"{self.first_name} {self.last_name} [age: {self.age}]"


    if __name__ == "__main__":
        john = Person("John", "Doe", 21.5)
        print(john)

        try:
            # invalid as 21.5 is not an instance of int
            john_strict = PersonStrictTypes("John", "Doe", 21.5)
        except TypeError as err:
            print(f"Error:\n{err}")

        john_strict = PersonStrictTypes("John", "Doe", 21)
        print(john_strict)
    ```

    This program will produce the following output:
    ```
    John Doe [age: 21]
    Error:
    Attribute value does not match the declared type:
            attribute: age, declared type: <class 'int'>, actual type: <class 'float'>
    John Doe [age: 21]
    ```

* `include: set[str]`

    This parameter defines a set of attribute names which are supposed to be treated as constant. If the parameter is not set (or set to `None`) all attributes will be treaded as constant.

    Example:
    ```python
    # common_include.py

    @cc.const_class(include=["first_name", "last_name"])
    class Person:
        first_name: str
        last_name: str
        age: int

        def __repr__(self) -> str:
            return f"{self.first_name} {self.last_name} [age: {self.age}]"


    if __name__ == "__main__":
        john = Person("John", "Doe", 21)
        print(f"{john = }")

        try:
            john.first_name = "Bob"
        except cc.ConstError as err:
            print(f"Error: {err}")

        try:
            john.last_name = "Smith"
        except cc.ConstError as err:
            print(f"Error: {err}")

        # valid modification as the `age` parameter is not in the include set
        john.age = 22
        print(f"{john = }")
    ```

    This program will produce the followig output:
    ```
    john = John Doe [age: 21]
    Error: Cannot modify const attribute `first_name` of class `Person`
    Error: Cannot modify const attribute `last_name` of class `Person`
    john = John Doe [age: 22]
    ```

* `exclude: set[str]`

    This parameter defines a set of attribute names which are supposed to be treated as mutable. If the parameter is not set (or set to `None`) all attributes will be treaded as constant.

    Example:
    ```python
    # common_exclude.py

    @cc.const_class(exclude=["age"])
    class Person:
        first_name: str
        last_name: str
        age: int

        def __repr__(self) -> str:
            return f"{self.first_name} {self.last_name} [age: {self.age}]"


    if __name__ == "__main__":
        john = Person("John", "Doe", 21)
        print(f"{john = }")

        try:
            john.first_name = "Bob"
        except cc.ConstError as err:
            print(f"Error: {err}")

        try:
            john.last_name = "Smith"
        except cc.ConstError as err:
            print(f"Error: {err}")

        # valid modification as the `age` parameter is in the exclude set
        john.age = 22
        print(f"{john = }")
    ```

    The class defined in this example has the behaviour equivalent to the `include` example.

> [!IMPORTANT]
> Simultaneous usage of the `incldue` and `exclude` parameters will result in raising a configuration error.

<br />

### Decorator-specific parameters

> [!NOTE]
> In the current version of the package only the `const_class` decorator has it's own specific parameters.

* `with_kwargs: bool`

    By default the `const_class` decorator adds a constructor which uses positional arguments to create a constant instance of the class. However if this parameter is set to `True`, the decorator will use the keyword arguments for this purpose.

    Example:
    ```python
    # const_class_with_kwargs.py

    @cc.const_class
    class PersonArgs:
        first_name: str
        last_name: str

        def __repr__(self) -> str:
            return f"{self.first_name} {self.last_name}"


    @cc.const_class(with_kwargs=True)
    class PersonKwargs:
        first_name: str
        last_name: str

        def __repr__(self) -> str:
            return f"{self.first_name} {self.last_name}"


    if __name__ == "__main__":
        john_args = PersonArgs("John", "Doe")
        print(f"{john_args = }")

        try:
            john_args = PersonArgs(first_name="John", last_name="Doe")
        except cc.InitializationError as err:
            print(f"Error: {err}")

        john_kwargs = PersonKwargs(first_name="John", last_name="Doe")
        print(f"{john_kwargs = }")
    ```

    This program will produce the following output:
    ```
    john_args = John Doe
    Error: Invalid number of arguments: expected 2 - got 0
    john_kwargs = John Doe
    ```

* `inherit_constructor: bool`

    By default the `const_class` decorator defines a constructor which manually assigns values to attributes. However if this parameter is set to `True` the class will be initialized using the user defined `__init__` function of the decorated class.

    Example:
    ```python
    # const_class_inherit_constructor.py

    @cc.static_const_class
    class ProjectConfiguration:
        name: str = "MyProject"
        version: str = "alpha"

        def __repr__(self):
            return f"Project: {self.name}\nVersion: {self.version}"


    if __name__ == "__main__":
        print(f"Project configuration:\n{ProjectConfiguration}")

        try:
            ProjectConfiguration.name = "NewProjectName"
        except cc.ConstError as err:
            print(f"Error: {err}")

        try:
            ProjectConfiguration.version = "beta"
        except cc.ConstError as err:
            print(f"Error: {err}")
    ```

    This program will produce the following output:
    ```
    john = John Doe
    Error: Cannot modify const attribute `first_name` of class `Person`
    Error: Cannot modify const attribute `last_name` of class `Person`
    ```


<br />
<br />

## Dev notes
<!-- TODO: extract to sepparate file -->

* export requirements: `pip freeze > requirements-dev.txt`
* install requirements: `pip install -r requirements-dev.txt`
* build distribution: `python -m build` (`pip install build`)
* project venv: `cc_venv`, `test_cc_venv` (for local package installation tests)
* install package in test venv: `pip install dist/pyconstclasses-<version>-py3-none-any.whl --force-reinstall`
* test with coverage: `pytest -v constclasses/test/ --cov=constclasses --cov-report=xml --cov-report=html` or `tox`
* format:
    * `black .` or `python -m black .` (`--check`)
    * `isort .` or `python -m isort .` (`--check`)

<br />
<br />

## Licence

The `PyConstClasses` project uses the [MIT Licence](https://opensource.org/license/mit/)
