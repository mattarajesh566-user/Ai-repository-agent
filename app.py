
import streamlit as st
import os
from explorer import explore_website
from test_generator import generate_test_cases
from tests import run_tests
from reporter import generate_report
from ai_agent import analyze_test_results

st.set_page_config(
    page_title="AI Regression Testing Agent",
    page_icon="🤖"
)

st.title("🤖 AI Regression Testing Agent")
st.write("Enter a website URL to run automated regression tests.")

url = st.text_input(
    "Website URL",
    placeholder="https://www.saucedemo.com/"
)

if st.button("Start Regression Testing"):

    if not url.strip():
        st.warning("Please enter a website URL.")
    else:
        try:
            with st.spinner("Exploring website..."):
                elements = explore_website(url)

            with st.spinner("Generating test cases..."):
                test_cases = generate_test_cases(elements)

            st.write("Total Generated Test Cases:", len(test_cases))

            with st.spinner("Running regression tests..."):
                results = run_tests(url, test_cases)

            st.subheader("Test Results")

            for test_name, result in results:
                if result == "PASS":
                    st.success(f"{test_name}: PASS")
                else:
                    st.error(f"{test_name}: FAIL")

            with st.spinner("Generating HTML report..."):
                generate_report(results)

            st.success("Testing completed! Report generated.")

            if os.path.exists("report.html"):
                with open("report.html", "r", encoding="utf-8") as file:
                    report_html = file.read()

                st.components.v1.html(
                    report_html,
                    height=800,
                    scrolling=True
                )

            with st.spinner("Analyzing results with Gemini AI..."):
                try:
                    ai_analysis = analyze_test_results(results)
                    st.subheader("Gemini AI Analysis")
                    st.write(ai_analysis)
                except Exception as error:
                    st.warning(f"Gemini analysis failed: {error}")

        except Exception as error:
            st.error(f"Testing failed: {error}")