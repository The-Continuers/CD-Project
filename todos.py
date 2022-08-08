class Todo:
    left_behind_tests = [
        'Arrays/t134-array-13.d'
    ]
    issues = [
        """
            most expression code generation sections need type-safety and also type evaluation,
            to generate the code correctly
        """,
        """
            we have implemented dynamic scoping, not static scoping. 
            1. we need to check static scoping.
            2. if a variable wasn't in the scope, we need to look for the global scope, not the parent.
        """,
    ]
    pass
