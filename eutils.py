from typing import NewType, Any, Callable, List, Union, Dict

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
    # return a if len(lb) == 0 else foldl(f, f(a, lb[0]), lb[1:])
    for b in lb: a = f(a, b)
    return a


def foldr(f: Callable[[A, B], B], b: B, la: List[A]) -> B:
    """
    Functional right fold

    :param f: function with type a -> b -> b
    :param b: argument with type b
    :param la: list with elements of type a
    :return: result of right fold of f over list la starting with b
    """
    return b if len(la) == 0 else f(la[0], foldr(f, b, la[1:]))


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
                   default_index: int = -1, return_element=True,
                   auto_return_single_element: bool = True) -> Union[A, int]:
    """
    Lets the user pick an element from a list.

    :param l: list to pick from
    :param prompt: optional extra information about what to pick
    :param to_string: function that converts an element el from l to a string - defaults to el.__str__()
    :param default_index: optional default choice
    :param return_element: will return list element when True (default) or the chosen index when False
    :param auto_return_single_element: if len(l) == 1, return l[0] without promt - defaults to True
    :return: either the chosen list element, or its index when return_element == False
    """
    if default_index != -1 and default_index not in range(0, len(l)):
        raise IndexError("Default index outside list range.")

    if auto_return_single_element and len(l) == 1:
        return l[0] if return_element else 0

    print(prompt)
    if to_string is None:
        def to_string(x):
            return x.__str__()
    for i, el in enumerate(l):
        print("\t[{}]: {}".format(i + 1, to_string(el)))

    default_str = "" if default_index == -1 else ", default is {}".format(default_index + 1)
    answer = input("Enter choice (1 to {}{}) > ".format(len(l), default_str))
    while not (answer.isnumeric() and int(answer) in range(1, len(l) + 1)):
        if len(answer) == 0 and default_index != -1:
            answer = default_index + 1
            break
        answer = input("Please enter a number between 1 and {} > ".format(len(l)))

    choice = int(answer) - 1
    return l[choice] if return_element else choice


def confirm_input(prompt: str, default: str = None) -> str:
    """
    Asks for user input and confirmation of the entered input

    :param prompt: the question to answer
    :param default: optional default answer
    :return: confirmed correct user input
    """
    res = input(prompt + (" (default is '{}') > ".format(default) if default else " > "))
    if default and res == "": return default
    while not yes_no("Input will be '{}'. Continue?".format(res), default=True):
        res = input(prompt + ' > ')
    return res


def typed_input(prompt: str, t: type, default: A = None) -> A:
    """
    Asks user input of specific type (int, float, etc)

    :param prompt: the question to answer
    :param t: the specified type
    :param default: optional default value
    :return: user input of type t
    """
    if default: assert t == type(default)
    answer = input(prompt + (" (default is '{}') > ".format(default) if default else " > "))
    if default and answer == "": return default
    while True:
        if t == type(float): answer = answer.replace(',', '.')
        try:
            return t(answer)
        except ValueError:
            answer = input("Please enter something of type '{}' > ".format(str(t.__name__)))


def dump(data: Any, path_to_file: str = "quick_dump.json", overwrite=False) -> None:
    """
    Dumps data into a json file, asks for overwrite confirmation if file 'path_to_file' already exists.

    :param data: data to dump
    :param path_to_file: path to the dump file - defaults to "quick_dump.json" in current directory
    :param overwrite: overwrite any existing file
    """
    import os

    def rec_rename(path):
        new_path = path + "_old"
        if os.path.exists(new_path): rec_rename(new_path)
        os.rename(path, new_path)

    if not overwrite and os.path.exists(path_to_file):
        choice = pick_from_list(["Append with '_old'", "Overwrite", "Do nothing"],
                                "File exists. What to do?")
        if choice == 0:
            rec_rename(path_to_file)
        elif choice == 1:
            pass
        elif choice == 2:
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


def interleave(*l: List[Any]) -> List[Any]:
    """
    Interleaves an arbitrary amount of lists

    :param l: an arbitrary amount of lists
    :return: an interleaved list
    """
    return [x for t in zip(*l) for x in t]


def dict_append(d: Dict[A, List[B]], k: A, v: B):
    """
    Appends value v to the list of d[k]

    :param d: the dict
    :param k: the key
    :param v: the value to append
    """
    try:
        d[k].append(v)
    except KeyError:
        d[k] = [v]


def dict_remove(d: Dict[A, List[B]], k: A, v: B):
    """
    Removes value v from the list of d[k]

    :param d: the dict
    :param k: the key
    :param v: the value to remove
    """
    d[k].remove(v)
    if len(d[k]) == 0:
        del d[k]


def flatten(l: List[List[Any]]) -> List[Any]:
    """
    Flattens a list of lists

    :param l: a list of lists
    :return: a list containing the elements from l's sublists
    """
    return [l2 for l1 in l for l2 in l1]
