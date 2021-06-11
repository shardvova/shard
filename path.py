from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome
import os


from applitools.selenium import (
    logger,
    VisualGridRunner,
    Eyes,
    Target,
    BatchInfo,
    BrowserType,
    DeviceName,
)


def set_up(eyes):

    eyes.configure.set_api_key("VpEXwHtKENoxwxc7njHv2AJVzJp4Lqt8uGsr103Etp4Ss110")


    eyes.configure.set_batch(BatchInfo("flaticon"))

    (
        eyes.configure.add_browser(800, 600, BrowserType.CHROME)
        .add_browser(700, 500, BrowserType.FIREFOX)
        .add_browser(1600, 1200, BrowserType.IE_11)
        .add_browser(1024, 768, BrowserType.EDGE_CHROMIUM)
        .add_browser(800, 600, BrowserType.SAFARI)
        .add_device_emulation(DeviceName.iPhone_X)
        .add_device_emulation(DeviceName.Pixel_2)
    )


def ultra_fast_test(web_driver, eyes):
    try:

        web_driver.get("https://odore.ml/")

        eyes.open(
            web_driver, "register", "main2", {"width": 800, "height": 600}
        )

        # check the login page with fluent api, see more info here
        # https://applitools.com/docs/topics/sdk/the-eyes-sdk-check-fluent-api.html
        eyes.check("", Target.window().fully().with_name("main page"))

        web_driver.find_element_by_name("Sign in").click #find_element_by_id("Sign in").click()

        # Check the app page
        eyes.check("", Target.window().fully().with_name("App page"))

        # Call Close on eyes to let the server know it should display the results
        eyes.close_async()
    except Exception as e:
        eyes.abort_async()
        print(e)


def tear_down(web_driver, runner):
    # Close the browser
    web_driver.quit()

    # we pass false to this method to suppress the exception that is thrown if we
    # find visual differences
    all_test_results = runner.get_all_test_results(False)
    print(all_test_results)


# Create a new chrome web driver
web_driver = Chrome(ChromeDriverManager().install())

# Create a runner with concurrency of 1
runner = VisualGridRunner(1)

# Create Eyes object with the runner, meaning it'll be a Visual Grid eyes.
eyes = Eyes(runner)

set_up(eyes)

try:
    # ⭐️ Note to see visual bugs, run the test using the above URL for the 1st run.
    # but then change the above URL to https://id.freepikcompany.com/login?client_id=flaticon
    # (for the 2nd run)
    ultra_fast_test(web_driver, eyes)
finally:
    tear_down(web_driver, runner)