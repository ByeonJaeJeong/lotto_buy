from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
loginUrl='https://dhlottery.co.kr/user.do?method=login&returnUrl='
chrome='C:/Users/Jeong/AppData/Local/Programs/Python/Python38/lotto_onefile/chromedriver.exe'
browser =webdriver.Chrome(chrome)
browser.get(loginUrl)
print(chrome)


#id password 값 입력
f= open('login.txt','r')
id= f.readline().rstrip('\n')
pw= f.readline().rstrip('\n')
value=f.readline()




#동행복권 아이디 입력
elem_login= browser.find_element_by_id('userId')
elem_login.send_keys(id)

#동행복권 비밀번호 입력
elem_login =browser.find_element_by_name('password')
elem_login.clear()
elem_login.send_keys(pw)

#로그인 버튼 클릭

LOGIN_XPATH= '//*[@id="article"]/div[2]/div/form/div/div[1]/fieldset/div[1]/a'
browser.find_element_by_xpath(LOGIN_XPATH).click()

time.sleep(1)

#동행복권 구매링크
link='https://el.dhlottery.co.kr/game/TotalGame.jsp?LottoId=LO40'
browser.get(link)

#자동구매 클릭
browser.switch_to.frame('ifrm_tab')
browser.find_element_by_xpath('//*[@id="num2"]').click()

#로또 구매 개수 선택
select= Select(browser.find_element_by_xpath('//*[@id="amoundApply"]'))
select.select_by_value(value)

#구매 확인 버튼 클릭
browser.find_element_by_xpath('//*[@id="btnSelectNum"]').click()

#구매하기
browser.find_element_by_xpath('//*[@id="btnBuy"]').click()

#확인버튼 클릭
alert= browser.switch_to.alert
alert.accept()

#프로그램 종료
browser.quit()


            
               
