from datetime import datetime
import html
import os


def generate_report(results):

    total = len(results)

    passed = sum(
        1 for _, result in results
        if result == "PASS"
    )

    failed = total - passed

    report_rows = ""

    for test_name, result in results:

        if result == "PASS":

            status_class = "pass"
            status_text = "PASS"
            screenshot_cell = "Not required"

        else:

            status_class = "fail"
            status_text = "FAIL"

            screenshot_name = (
                test_name.replace(" ", "_") + ".png"
            )

            screenshot_path = os.path.join(
                "failure screenshots",
                screenshot_name
            )

            if os.path.exists(screenshot_path):

                screenshot_cell = f"""
                <a href="{html.escape(screenshot_path)}"
                   target="_blank">
                    View Screenshot
                </a>
                """

            else:

                screenshot_cell = "Screenshot not found"

        report_rows += f"""
        <tr>
            <td>{html.escape(test_name)}</td>
            <td class="{status_class}">{status_text}</td>
            <td>{screenshot_cell}</td>
        </tr>
        """

    report_content = f"""
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <title>AI Regression Testing Report</title>

    <style>

        body {{
            font-family: Arial, sans-serif;
            background: #f4f6f8;
            padding: 30px;
        }}

        .container {{
            max-width: 1000px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
        }}

        h1 {{
            color: #222;
        }}

        .summary {{
            display: flex;
            gap: 20px;
            margin: 20px 0;
        }}

        .card {{
            padding: 20px;
            border-radius: 8px;
            background: #eef2f7;
            flex: 1;
        }}

        .pass {{
            color: green;
            font-weight: bold;
        }}

        .fail {{
            color: red;
            font-weight: bold;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
        }}

        th,
        td {{
            padding: 12px;
            border-bottom: 1px solid #ddd;
            text-align: left;
        }}

        th {{
            background: #222;
            color: white;
        }}

        a {{
            color: blue;
            font-weight: bold;
        }}

    </style>

</head>

<body>

    <div class="container">

        <h1>AI Regression Testing Report</h1>

        <p>
            Generated on:
            {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        </p>

        <div class="summary">

            <div class="card">
                <h2>{total}</h2>
                <p>Total Tests</p>
            </div>

            <div class="card">
                <h2 class="pass">{passed}</h2>
                <p>Passed</p>
            </div>

            <div class="card">
                <h2 class="fail">{failed}</h2>
                <p>Failed</p>
            </div>

        </div>

        <h2>Test Results</h2>

        <table>

            <tr>
                <th>Test Name</th>
                <th>Status</th>
                <th>Evidence</th>
            </tr>

            {report_rows}

        </table>

    </div>

</body>

</html>
"""

    with open(
        "report.html",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(report_content)

    print("\nHTML report generated successfully!")

    print("Report file: report.html")

    print("\n================================")
    print("SUMMARY")
    print("================================")

    print("Total Tests:", total)
    print("Passed:", passed)
    print("Failed:", failed)