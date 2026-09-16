from playwright.sync_api import sync_playwright


def explore_website(url):

    elements = {
        "links": 0,
        "buttons": 0,
        "inputs": 0,
        "forms": 0
    }

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("\n================================")
        print("       WEBSITE EXPLORER")
        print("================================")

        print("Opening:", url)

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=30000
        )

        print("Page Title:", page.title())
        print("Page URL:", page.url)

        # Find links
        links = page.locator("a")
        link_count = links.count()

        elements["links"] = link_count

        print("\n========== LINKS ==========")
        print("Links Found:", link_count)

        # Find buttons and button-like inputs
        buttons = page.locator(
            "button, input[type='button'], input[type='submit']"
        )

        button_count = buttons.count()

        elements["buttons"] = button_count

        print("\n========== BUTTONS ==========")
        print("Buttons Found:", button_count)

        # Find input fields
        inputs = page.locator(
            "input, textarea, select"
        )

        input_count = inputs.count()

        elements["inputs"] = input_count

        print("\n========== INPUT FIELDS ==========")
        print("Input Fields Found:", input_count)

        # Find forms
        forms = page.locator("form")
        form_count = forms.count()

        elements["forms"] = form_count

        print("\n========== FORMS ==========")
        print("Forms Found:", form_count)

        browser.close()

    return elements