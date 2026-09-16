import streamlit as st

from explorer import explore_website
from test_generator import generate_test_cases
from tests import run_tests
from reporter import generate_report
from ai_agent import analyze_test_results


st.set_page_config(
    page_title="AI Regression Testing Agent",
    page_icon="🧪",
    layout="wide"
)


def main():
    st.title("🧪 AI Regression Testing Agent")
    st.write("Enter a website URL to explore, test, and generate an AI analysis report.")

    url = st.text_input(
        "Enter website URL",
        placeholder="https://www.saucedemo.com/"
    )

    if st.button("Start Regression Testing"):
        if not url:
            st.warning("Please enter a website URL.")
            return

        try:
            with st.spinner("Exploring website..."):
                elements = explore_website(url)

            st.success("Website exploration completed.")

            with st.spinner("Generating test cases..."):
                test_cases = generate_test_cases(elements)

            st.write("Total Generated Test Cases:", len(test_cases))

            with st.spinner("Running regression tests..."):
                results = run_tests(url, test_cases)

            st.success("Regression tests completed.")

            st.subheader("Test Results")
            st.write(results)

            with st.spinner("Analyzing test results with Gemini AI..."):
                try:
                    ai_analysis = analyze_test_results(results)

                    st.subheader("Gemini AI Analysis")
                    st.write(ai_analysis)

                except Exception as error:
                    st.error(f"Gemini analysis failed: {error}")

            with st.spinner("Generating HTML report..."):
                generate_report(results)

            st.success("HTML report created successfully.")

            st.info(
                "The report was generated as report.html. "
                "If the report is not visible online, the report file must be displayed "
                "inside Streamlit or saved using another deployment method."
            )

        except Exception as error:
            st.error(f"Testing failed: {error}")


if __name__ == "__main__":
    main()