from selenium import webdriver
browser = webdriver.Chrome()

url = 'https://www.lexisnexis.com/hottopics/lnacademic/?verb=sf&amp;sfi=AC00NBGenSrch'
browser.get(url)
browser.switch_to_frame('mainFrame')
browser.find_element_by_id('terms').clear()
browser.find_element_by_id('terms').send_keys('Lê Mạnh Chức')

# element_show = browser.find_element_by_id('terms')
# browser.execute_script("arguments[0].setAttribute('class','ShowModal')", element_show)


browser.find_element_by_id('lblAdvancDwn').click()

browser.find_element_by_xpath('//*[@id="ddlSegment"]/option[3]').click()

browser.find_element_by_css_selector('input[type=\"submit\"]').click()

