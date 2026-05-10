import pytest
from config.environment import config

@pytest.mark.ui
def test_launch_application(driver):

    driver.get(config.base_url)

    assert "Notes" in driver.title