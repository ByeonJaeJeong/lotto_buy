import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import urllib.request
import time
import os
import requests

#현재 폴더 경로 찾기
chrome=os.getcwd()+'/chromedriver.exe'
#로그인페이지
loginUrl='https://dhlottery.co.kr/user.do?method=login&returnUrl='
#구매보관 페이지
mypageUrl='https://www.dhlottery.co.kr/myPage.do?method=lottoBuyListView'
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
browser=webdriver.Chrome(chrome,chrome_options=options)
browser.implicitly_wait(3)

#메인 프레임
class lottoApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.protocol("WM_DELETE_WINDOW",self.on_exit) #닫기 재선언
        self.switch_frame(LoginPage)
    #종료시 브라우저도 같이 닫음
    def on_exit(self):
        self.destroy()
        browser.quit()
    def switch_frame(self,frame_class):
        new_frame =frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame= new_frame
        self._frame.pack()
#로그인 프레임
class LoginPage(tk.Frame):
    def __init__(self,master):
        master.title("로그인페이지")
        master.resizable(False,False)
        def loginClick():
            id=tk.Entry.get(IDentry)
            pw=tk.Entry.get(PWentry)
            if(id=='' or pw==''):
               messagebox.showinfo("로그인 실패","아이디나 패스워드를 확인해주세요")
            else:
                #로그인창 출력
        
                browser.get(loginUrl)

    
                #동행복권 아이디 입력
                elem_login= browser.find_element_by_id('userId')
                elem_login.clear()
                elem_login.send_keys(id)

                #동행복권 비밀번호 입력
                elem_login =browser.find_element_by_name('password')
                elem_login.clear()
                elem_login.send_keys(pw)
    
                #로그인 버튼 클릭
    
                LOGIN_XPATH= '//*[@id="article"]/div[2]/div/form/div/div[1]/fieldset/div[1]/a'
                browser.find_element_by_xpath(LOGIN_XPATH).click()
                #로그인 여부 확인
                try:
                
                    alert= browser.switch_to.alert
                    alert.accept()
            
                    time.sleep(1)
                    messagebox.showinfo("로그인 실패","아이디나 패스워드를 확인해주세요")
            
                except:
                    master.switch_frame(buyPage).pack()
        tk.Frame.__init__(self,master)
        IDlabel=tk.Label(self,text="ID : ")
        IDlabel.grid(row=0,column=0)
        IDentry=tk.Entry(self)
        IDentry.grid(row=0,column=1)
        PWlabel=tk.Label(self,text="PW : ")
        PWlabel.grid(row=1,column=0)
        PWentry=tk.Entry(self,show="*")
        PWentry.grid(row=1,column=1)
        LoginButton=tk.Button(self,text="로그인",width=10,height=2 ,command=loginClick)
        LoginButton.grid(row=0,column=2,rowspan=2,padx=3)
#로그인후 페이지
class buyPage(tk.Frame):
    def __init__(self,master):
        master.geometry("700x300")
        master.title("구매 페이지")
        master.resizable(False,False)
        tk.Frame.__init__(self,master)
        
        #구매한 로또
        def getLottoInfo():
            
            browser.get(mypageUrl)
            browser.switch_to.frame('lottoBuyList')
            html=browser.page_source
            soup=BeautifulSoup(html,'html.parser')
            table=soup.find('table',{'class':'tbl_data_col'})
            tbody=table.find('tbody')
            trs=tbody.find_all('tr')
            for idx,tr in enumerate(trs):
                tds= tr.find_all('td')
                buy_date=tds[0].text.strip()
                lotto_type=tds[1].text.strip()
                round=tds[2].text.strip()
                lotto_number=tds[3].text.strip()
                lotto_count=tds[4].text.strip()
                lotto_rank=tds[5].text.strip()
                lotto_money=tds[6].text.strip()
                lotto_drawdate=tds[7].text.strip()
                #데이터 
                buy_date_label=tk.Label(self,text=buy_date)
                buy_date_label.grid(row=4+idx,column=0)
                lotto_type_label=tk.Label(self,text=lotto_type)
                lotto_type_label.grid(row=4+idx,column=1)
                round_label=tk.Label(self,text=round)
                round_label.grid(row=4+idx,column=2)
                lotto_number_label=tk.Label(self,text=lotto_number)
                lotto_number_label.grid(row=4+idx,column=3)
                lotto_count_label=tk.Label(self,text=lotto_count)
                lotto_count_label.grid(row=4+idx,column=4)
                lotto_rank_label=tk.Label(self,text=lotto_rank)
                lotto_rank_label.grid(row=4+idx,column=5)
                lotto_money_label=tk.Label(self,text=lotto_money)
                lotto_money_label.grid(row=4+idx,column=6)
                lotto_drawdate_label=tk.Label(self,text=lotto_drawdate)
                lotto_drawdate_label.grid(row=4+idx,column=7)
                
            
        def buyClick():
            value=tk.Entry.get(comboBox)
            #동행복권 구매링크
            time.sleep(1)
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
            try:
                browser.find_element_by_xpath('//*[@id="recommend720Plus"]/div')
                messagebox.showinfo("구매실패","이번주 구매한도 5천원을 모두 채우셨습니다.")
            except:
                #프로그램 종료
                messagebox.showinfo("구매성공","정상적으로 구매되었습니다.")
        #로또구매정보
        getLottoInfo()
        #매수버튼
        comboBox=ttk.Combobox(self,values=['1','2','3','4','5'],state="readonly",width=15)
        comboBox.grid(row=0,column=0 ,pady=10,columnspan=3,sticky='e')
        comboBox.current(0)

        #구매버튼
        buyButton=tk.Button(self,text="구매",width=10,command=buyClick)
        buyButton.grid(row=0,column=3,columnspan=3,sticky='W')

        #구분선
        blankLabel_1= tk.Label(self,text="==========================================================================")
        blankLabel_1.grid(row=2,column=0,columnspan=8)
        
        time.sleep(1)
        #label
        buy_date_label=tk.Label(self,text="구매날짜")
        buy_date_label.grid(row=3,column=0)
        lotto_type_label=tk.Label(self,text="복권명")
        lotto_type_label.grid(row=3,column=1)
        round_label=tk.Label(self,text="회차")
        round_label.grid(row=3,column=2)
        lotto_number_label=tk.Label(self,text="선택번호")
        lotto_number_label.grid(row=3,column=3)
        lotto_count_label=tk.Label(self,text="구입매수")
        lotto_count_label.grid(row=3,column=4)
        lotto_rank_label=tk.Label(self,text="당첨결과")
        lotto_rank_label.grid(row=3,column=5)
        lotto_money_label=tk.Label(self,text="당첨금")
        lotto_money_label.grid(row=3,column=6)
        lotto_drawdate_label=tk.Label(self,text="추첨일")
        lotto_drawdate_label.grid(row=3,column=7)
        
if __name__ == "__main__":
    app = lottoApp()
    app.mainloop()
         



            
               
