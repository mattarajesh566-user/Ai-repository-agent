def generate_test_cases(elements):

    test_cases = []

    print("\n================================")
    print("       TEST CASE GENERATOR")
    print("================================")

    if elements["inputs"] > 0:
        test_cases.append("Check form input fields")

    if elements["buttons"] > 0:
        test_cases.append("Check whether buttons are clickable")

    if elements["links"] > 0:
        test_cases.append("Check whether links work correctly")
        test_cases.append("Check website navigation")

    if elements["forms"] > 0:
        test_cases.append("Check whether forms are available")

    test_cases.append("Check whether the page loads successfully")

    test_cases.append("Check whether the page has visible content")

    print("\nGenerated Test Cases:")

    for number, test_case in enumerate(test_cases, start=1):
        print(f"{number}. {test_case}")

    return test_cases