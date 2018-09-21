from typing import NewType, Any, Callable, List, Union

A = NewType('A', Any)
B = NewType('B', Any)


def foldl(f: Callable[[A, B], A], a: A, lb: List[B]) -> A:
    """
    Functional left fold

    :param f: function with type a -> b -> a
    :param a: argument with type a
    :param lb: list with elements of type b
    :return: result of left fold of f over list lb starting with a
    """
    return a if len(lb) == 0 else foldl(f, f(a, lb[0]), lb[1:])


def foldr(f: Callable[[A, B], B], b: B, la: List[A]) -> B:
    """
    Functional right fold

    :param f: function with type a -> b -> b
    :param b: argument with type b
    :param la: list with elements of type a
    :return: result of right fold of f over list la starting with b
    """
    return b if len(la) == 0 else foldr(f, f(la[-1], b), la[:-1])


def yes_no(question: str, default: bool = None) -> bool:
    """
    Asks a yes/no input of user.

    :param question: the question to answer with yes or no
    :param default: optional default value (true for yes, false for no)
    :return: true for yes, false for no
    """
    yes = ['y', 'ye', 'yes']
    no = ['n', 'no']
    default_str = "({}/{})".format('y'.upper() if default else 'y',
                                   'n'.upper() if default is not None and not default else 'n')
    answer = input("{} {} > ".format(question, default_str)).lower()
    while answer not in yes + no:
        if len(answer) == 0 and default is not None:
            return default
        answer = input("Please respond with 'yes' or 'no'. > ").lower()
    return answer in yes


def pick_from_list(l: List[A], prompt: str = "Pick from the following list:",
                   to_string: Callable[[A], str] = None,
                   default_index: int = None, return_element=True,
                   auto_return_single_element: bool = True) -> Union[A, int]:
    """
    Lets the user pick an element from a list.

    :param l: list to pick from
    :param to_string: function that converts an element el from l to a string - defaults to el.__str__()
    :param default_index: optional default choice
    :param return_element: will return list element when True (default) or the chosen index when False
    :param auto_return_single_element: if len(l) == 1, return l[0] without promt - defaults to True
    :return: either the chosen list element, or its index when return_element == False
    """
    if default_index is not None and default_index not in range(0, len(l)):
        raise IndexError("Default index outside list range.")

    if auto_return_single_element and len(l) == 1:
        return l[0] if return_element else 0

    print(prompt)
    if to_string is None:
        def to_string(x):
            return x.__str__()
    for i, el in enumerate(l):
        print("\t[{}]: {}".format(i + 1, to_string(el)))

    answer = input("Enter choice (1 to {}) > ".format(1, len(l) + 1))
    while not (answer.isnumeric() and int(answer) in range(1, len(l) + 1)):
        if len(answer) == 0 and default_index is not None:
            answer = default_index + 1
            break
        answer = input("Please enter a number between 1 and {} > ".format(1, len(l) + 1))

    choice = int(answer) - 1
    return l[choice] if return_element else choice


def confirm_input(prompt: str, default: str = None):
    res = input(prompt + (" (default is '{}') > ".format(default) if default else " > "))
    if default and res == "": return default
    while not yes_no("Input will be '{}'. Continue?".format(res), default=True):
        res = input(prompt)
    return res


def dump(data: Any, path_to_file: str = "quick_dump.json") -> None:
    """
    Dumps data into a json file, asks for overwrite confirmation if file 'path_to_file' already exists.

    :param data: data to dump
    :param path_to_file: path to the dump file - defaults to "quick_dump.json" in current directory
    """
    import os
    if os.path.exists(path_to_file) and not yes_no("Overwrite existing file '{}'?".format(path_to_file), default=True):
        return
    with open(path_to_file, 'w') as dump_file:
        import json
        json.dump(data, dump_file)


def load(path_to_file: str = "quick_dump.json") -> Any:
    """
    Loads data from json file.

    :param path_to_file: path to the dump file - defaults to "quick_dump.json" in current directory
    :return: data contained by 'path_to_file'
    """
    with open(path_to_file, 'r') as dump_file:
        import json
        return json.load(dump_file)
