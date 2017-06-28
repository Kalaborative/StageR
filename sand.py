from selenium import webdriver

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get('http://localhost:5000')
someName = driver.find_element_by_class_name("message")
someName.click()
loadedName = driver.find_element_by_id("currentSinger")
print loadedName.text