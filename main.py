from explorer import explore_website
from test_generator import generate_test_cases
from tests import run_tests
from reporter import generate_report
from ai_agent import analyze_test_results


def main():

    print("\n================================")
    print("      AI REGRESSION TESTING AGENT")
    print("================================")

    url = input("\nEnter website URL: ")

    print("\nStarting website exploration...")

    elements = explore_website(url)

    print("\nGenerating test cases...")

    test_cases = generate_test_cases(elements)

    print("\nTotal Generated Test Cases:", len(test_cases))

    print("\nStarting regression tests...")

    results = run_tests(url, test_cases)

    print("\n================================")
    print("       GEMINI AI ANALYSIS")
    print("================================")

    try:
        ai_analysis = analyze_test_results(results)

        print("\nAI Testing Analysis:\n")
        print(ai_analysis)

    except Exception as error:
        print("\nGemini analysis failed.")
        print("Error:", error)

    print("\nGenerating HTML report...")

    generate_report(results)

    print("\n================================")
    print("       PROCESS COMPLETED")
    print("================================")

    print("\nHTML report created: report.html")


if __name__ == "__main__":
    main()