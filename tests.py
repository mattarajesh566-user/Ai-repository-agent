
from playwright.sync_api import sync_playwright
import os
from urllib.parse import urljoin


def save_screenshot(page, test_name):
    try:
        if page.is_closed():
            print("Screenshot skipped because the page is closed.")
            return

        os.makedirs("failure screenshots", exist_ok=True)

        file_name = test_name.replace(" ", "_") + ".png"
        file_path = os.path.join("failure screenshots", file_name)

        page.screenshot(path=file_path, full_page=True)

        print("Screenshot saved:", file_path)

    except Exception as screenshot_error:
        print("Could not save screenshot:", screenshot_error)


def run_tests(url, test_cases):

    results = []

    with sync_playwright() as p:

         print("TESTS FILE:", __file__)
         print("HEADLESS MODE: TRUE")

    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )

    request_context = p.request.new_context()

    for test_case in test_cases:

            print("\n================================")
            print("RUNNING:", test_case)
            print("================================")

            page = None

            try:
                page = browser.new_page()

                if test_case == "Check form input fields":

                    page.goto(url, wait_until="domcontentloaded", timeout=30000)

                    inputs = page.locator("input, textarea, select")
                    input_count = inputs.count()

                    print("Input fields found:", input_count)

                    if input_count > 0:
                        print("FORM INPUT TEST: PASS")
                        results.append(("Form Input Test", "PASS"))
                    else:
                        print("FORM INPUT TEST: FAIL")
                        save_screenshot(page, "Form_Input_Test")
                        results.append(("Form Input Test", "FAIL"))

                elif test_case == "Check whether buttons are clickable":

                    page.goto(url, wait_until="domcontentloaded", timeout=30000)

                    buttons = page.locator(
                        "button, input[type='submit'], input[type='button']"
                    )

                    button_count = buttons.count()
                    print("Buttons found:", button_count)

                    all_buttons_work = True

                    for index in range(button_count):

                        button = buttons.nth(index)

                        if not button.is_visible():
                            print("Button", index + 1, "is not visible")
                            continue

                        if not button.is_enabled():
                            print("Button", index + 1, "is disabled")
                            all_buttons_work = False
                            break

                        print(
                            "Button",
                            index + 1,
                            "is visible and enabled"
                        )

                    if all_buttons_work:
                        print("BUTTON TEST: PASS")
                        results.append(("Buttons Test", "PASS"))
                    else:
                        print("BUTTON TEST: FAIL")
                        save_screenshot(page, "Buttons_Test")
                        results.append(("Buttons Test", "FAIL"))

                elif test_case == "Check whether links work correctly":

                    page.goto(url, wait_until="domcontentloaded", timeout=30000)

                    links = page.locator("a")
                    link_count = links.count()

                    print("Total links found:", link_count)

                    broken_links = []

                    for index in range(link_count):

                        link = links.nth(index)
                        href = link.get_attribute("href")

                        if href is None or href.strip() == "":
                            continue

                        if href.startswith("#"):
                            continue

                        complete_url = urljoin(page.url, href)

                        print("Checking link:", complete_url)

                        try:
                            response = request_context.get(
                                complete_url,
                                timeout=10000
                            )

                            status_code = response.status

                            print("HTTP Status:", status_code)

                            if status_code >= 400 and status_code != 403:
                                broken_links.append(
                                    f"{complete_url} - HTTP {status_code}"
                                )

                        except Exception as link_error:
                            broken_links.append(
                                f"{complete_url} - {link_error}"
                            )

                    if len(broken_links) == 0:
                        print("LINK TEST: PASS")
                        results.append(("Links Test", "PASS"))
                    else:
                        print("LINK TEST: FAIL")

                        for broken_link in broken_links:
                            print("Broken link:", broken_link)

                        save_screenshot(page, "Links_Test")
                        results.append(("Links Test", "FAIL"))

                elif test_case == "Check website navigation":

                    page.goto(url, wait_until="domcontentloaded", timeout=30000)

                    links = page.locator("a")
                    link_count = links.count()

                    print("Navigation links found:", link_count)

                    navigation_failures = []

                    for index in range(link_count):

                        link = links.nth(index)
                        href = link.get_attribute("href")

                        if href is None or href.strip() == "":
                            continue

                        if href.startswith("#"):
                            continue

                        complete_url = urljoin(page.url, href)

                        print("Checking navigation:", complete_url)

                        try:
                            response = request_context.get(
                                complete_url,
                                timeout=10000
                            )

                            status_code = response.status

                            print(
                                "Navigation HTTP Status:",
                                status_code
                            )

                            if status_code >= 400 and status_code != 403:
                                navigation_failures.append(
                                    f"{complete_url} - HTTP {status_code}"
                                )

                        except Exception as navigation_error:
                            navigation_failures.append(
                                f"{complete_url} - {navigation_error}"
                            )

                    if len(navigation_failures) == 0:
                        print("NAVIGATION TEST: PASS")
                        results.append(("Navigation Test", "PASS"))
                    else:
                        print("NAVIGATION TEST: FAIL")

                        for failure in navigation_failures:
                            print("Navigation failure:", failure)

                        save_screenshot(page, "Navigation_Test")
                        results.append(("Navigation Test", "FAIL"))

                elif test_case == "Check whether forms are available":

                    page.goto(url, wait_until="domcontentloaded", timeout=30000)

                    forms = page.locator("form")
                    form_count = forms.count()

                    print("Forms found:", form_count)

                    if form_count > 0:
                        print("FORM AVAILABILITY TEST: PASS")
                        results.append(("Form Availability Test", "PASS"))
                    else:
                        print("FORM AVAILABILITY TEST: FAIL")
                        save_screenshot(page, "Form_Availability_Test")
                        results.append(("Form Availability Test", "FAIL"))

                elif test_case == "Check whether the page loads successfully":

                    page.goto(url, wait_until="domcontentloaded", timeout=30000)

                    if page.title():
                        print("PAGE LOAD TEST: PASS")
                        results.append(("Page Load Test", "PASS"))
                    else:
                        print("PAGE LOAD TEST: FAIL")
                        save_screenshot(page, "Page_Load_Test")
                        results.append(("Page Load Test", "FAIL"))

                elif test_case == "Check whether the page has visible content":

                    page.goto(url, wait_until="domcontentloaded", timeout=30000)

                    body_text = page.locator("body").inner_text().strip()

                    print("Visible text length:", len(body_text))

                    if len(body_text) > 0:
                        print("VISIBLE CONTENT TEST: PASS")
                        results.append(("Visible Content Test", "PASS"))
                    else:
                        print("VISIBLE CONTENT TEST: FAIL")
                        save_screenshot(page, "Visible_Content_Test")
                        results.append(("Visible Content Test", "FAIL"))

            except Exception as error:

                print("TEST ERROR:", error)

                safe_name = test_case.replace(" ", "_")

                if page is not None:
                    save_screenshot(page, safe_name)

                results.append((test_case, "FAIL"))

            finally:

                if page is not None:
                    try:
                        if not page.is_closed():
                            page.close()
                    except Exception:
                        pass

            request_context.dispose()
            browser.close()

    return results