from binance.client import Client
import matplotlib.pyplot as plt
import numpy as np
import time

api_key = ""
api_secret = ""
client = Client(api_key=api_key, api_secret=api_secret)

class 데이터가공:
    def __init__(self,종목코드,시간단위,시작시간,끝시간):
        self.데이터= np.array(client.futures_historical_klines(symbol=종목코드,interval=시간단위,start_str=시작시간,end_str=끝시간),dtype=float)[:,[1,2,3,4,5]]
        self.시가=self.데이터[:,0]
        self.고가=self.데이터[:,1]
        self.저가=self.데이터[:,2]
        self.종가=self.데이터[:,3]
        self.거래량=self.데이터[:,4]

class 초기자산:
    def __init__(self,초기자산):
        self.초기자산=초기자산
        self.기준자산=초기자산
        self.거래대금=0
        self.거래량=0
        self.총수량=0   
        self.총수량가격=0
        self.수수료=0 
        self.시간=0
        self.가격=0
        self.수익=0
        self.기준수익=self.수익
        self.지표수익=self.수익-self.기준수익
        self.자산=0
        self.매수매도상태=0
        self.진입가격=0
        self.진입수량=0
        self.포지션="무포지션"
        self.매수가용자산=초기자산
        self.매도가용자산=초기자산
        self.수익률=0
        self.누적수익률=0
        self.매매실패횟수=0
        self.매수가용자산리스트=[]
        self.매도가용자산리스트=[]
        self.누적수익률리스트=[]
        self.가격리스트=[]
        self.수익리스트=[]
        self.자산리스트=[]
        self.매수인덱스=[]
        self.매수가격=[]
        self.매도인덱스=[]
        self.매도가격=[]
        self.손절인덱스=[]
        self.손절가격=[]
        self.익절인덱스=[]
        self.익절가격=[]
        self.매수진입인덱스=[]
        self.매수진입가격리스트=[]
        self.매도진입인덱스=[]
        self.매도진입가격리스트=[]
        self.진입인덱스=[]
        self.진입가격리스트=[]
        self.청산인덱스=[]
        self.청산가격=[]
        self.청산자산=[]
        
    def 실시간데이터(self,시간,가격):
        self.시간=시간
        self.가격=가격 
        self.수익=self.가격*self.총수량-self.총수량가격
        self.자산=self.초기자산+self.수익-self.수수료
        if self.총수량>0:
            self.포지션="매수포지션"
            self.매수가용자산=self.자산-self.진입가격*self.총수량
            self.매도가용자산=self.자산+self.진입가격*self.총수량
            self.진입수량=self.총수량
        elif self.총수량<0:
            self.포지션="매도포지션"
            self.매수가용자산=self.자산-self.진입가격*self.총수량
            self.매도가용자산=self.자산+self.진입가격*self.총수량
            self.진입수량=-self.총수량
        else:
            self.포지션="무포지션"
            self.매수가용자산=self.자산
            self.매도가용자산=self.자산
            self.진입수량=0  

        self.지표수익=self.수익-self.기준수익
        self.수익률=(self.자산-self.기준자산)/self.기준자산*100
        self.누적수익률=(self.자산-self.초기자산)/self.초기자산*100

    def 실시간데이터누적(self):    
        self.누적수익률리스트.append(self.누적수익률)
        self.가격리스트.append(self.가격)
        self.수익리스트.append(self.수익)
        self.자산리스트.append(self.자산)
        self.매수가용자산리스트.append(self.매수가용자산)
        self.매도가용자산리스트.append(self.매도가용자산)
        if self.진입가격!=0:
            self.진입인덱스.append(self.시간)
            self.진입가격리스트.append(self.진입가격)
            if self.포지션=="매수포지션":
                self.매수진입인덱스.append(self.시간)
                self.매수진입가격리스트.append(self.진입가격)
            elif self.포지션=="매도포지션":
                self.매도진입인덱스.append(self.시간)
                self.매도진입가격리스트.append(self.진입가격)

    def 매수(self,수량):
        if self.매수가용자산/self.가격>=수량:
            print("-----------------------------------") 
            print("매수합니다")
            self.거래대금+=self.가격*수량
            self.거래량+=수량
            self.총수량+=수량
            self.총수량가격+=self.가격*수량
            self.수수료+=self.가격*0.0006*수량
            self.매수인덱스.append(self.시간)
            self.매수가격.append(self.가격)
            if self.포지션=="무포지션":
                self.진입가격=self.가격
            elif self.포지션=="매도포지션":
                if self.총수량>0:
                    self.진입가격=self.가격
                elif self.총수량==0:
                    self.진입가격=0
            else:
                self.진입가격=(self.진입가격*self.진입수량+self.가격*수량)/(self.진입수량+수량)
        else:
            print("-----------------------------------") 
            print("매수 자산이 부족합니다:",수량-self.매수가용자산/self.가격)    
            self.매매실패횟수+=1
            
    def 매도(self,수량):
        if self.매도가용자산/self.가격>=수량:
            print("-----------------------------------")       
            print("매도합니다")
            self.거래대금+=self.가격*수량
            self.거래량+=수량
            self.총수량-=수량
            self.총수량가격-=self.가격*수량
            self.수수료+=self.가격*0.0006*수량
            self.매도인덱스.append(self.시간)
            self.매도가격.append(self.가격)
            if self.포지션=="무포지션":
                self.진입가격=self.가격
            elif self.포지션=="매수포지션":
                if self.총수량<0:
                    self.진입가격=self.가격
                elif self.총수량==0:
                    self.진입가격=0
            else:
                self.진입가격=(self.진입가격*self.진입수량+self.가격*수량)/(self.진입수량+수량)
        else:
            print("-----------------------------------")   
            print("매도 자산이 부족합니다:",수량-self.매도가용자산/self.가격)   
            self.매매실패횟수+=1

    def 손절(self,실제):
        self.손절인덱스.append(self.시간) 
        self.손절가격.append(self.가격)
        if 실제==True:   
            if self.포지션=="매수포지션":
                self.매도(self.진입수량) 
                print("-----------------------------------")   
                print("매수포지션 손절합니다")            
            elif self.포지션=="매도포지션":
                self.매수(self.진입수량)  
                print("-----------------------------------")   
                print("매도포지션 손절합니다")  

    def 익절(self,실제):
        self.익절인덱스.append(self.시간) 
        self.익절가격.append(self.가격)
        if 실제==True:   
            if self.포지션=="매수포지션":
                self.매도(self.진입수량)      
                print("-----------------------------------")   
                print("매수포지션 익절합니다")            
            elif self.포지션=="매도포지션":
                self.매수(self.진입수량)
                print("-----------------------------------")    
                print("매도포지션 익절합니다")  

    def 청산(self,실제):
        self.청산인덱스.append(self.시간) 
        self.청산가격.append(self.가격)   
        self.청산자산.append(self.자산)
        if 실제==True:   
            if self.포지션=="매수포지션":
                self.매도(self.진입수량)      
                print("-----------------------------------")   
                print("청산합니다")            
            elif self.포지션=="매도포지션":
                self.매수(self.진입수량)
                print("-----------------------------------")    
                print("청산합니다")    

    def 수익률리셋(self):
        self.기준자산=self.자산

    def 지표수익리셋(self):
        self.기준수익=self.수익

    def 백테스트(self,실시간데이터,로직데이터=False,로직데이터변환=False,매수로직=False,매도로직=False,익절로직=False,손절로직=False,청산로직=False,실행과정=True,실행속도=1):
        for 시간,가격 in enumerate(실시간데이터):
            self.실시간데이터(시간,가격)
            if 로직데이터변환 != False:
                로직데이터변환(로직데이터)
            if 청산로직 != False:
                청산로직(로직데이터)
            self.실시간데이터(시간,가격)  
            if 익절로직 != False:
                익절로직(로직데이터)
            self.실시간데이터(시간,가격)
            if 손절로직 != False:
                손절로직(로직데이터)
            self.실시간데이터(시간,가격)
            if 매수로직 != False:
                매수로직(로직데이터)
            self.실시간데이터(시간,가격)
            if 매도로직 != False:
                매도로직(로직데이터)
            self.실시간데이터(시간,가격)
            self.실시간데이터누적()
            if 실행과정==True:
                print("-----------------------------------") 
                print("진행경과:",(시간+1)/len(실시간데이터)*100,"%") 
                print("익절횟수:",len(self.익절인덱스),"손절횟수:",len(self.손절인덱스))
                print("포지션:",self.포지션)
                print("현재가격:",가격)
                print("진입가격:",self.진입가격)
                print("진입수량:",self.진입수량)
                print("수익:",self.수익-self.수수료)
                print("지표수익:",self.지표수익)
                print("자산:",self.자산)
                print("매수가용자산:",self.매수가용자산)
                print("매도가용자산:",self.매도가용자산)
                print("수익률:",self.수익률,"%")
                print("누적수익률:",self.누적수익률,"%")
            else:
                print("-----------------------------------")   
                print("진행경과:",(시간+1)/len(실시간데이터)*100,"%") 
            if self.누적수익률<-100:
                print("-----------------------------------")
                print(          "청산되었습니다:")
                print("-----------------------------------")
                return self.자산  
            time.sleep(실행속도)
        return self.자산

    def 그래프(self,실시간데이터):
        if len(self.가격리스트)==0:
            plt.title("Chart")
            plt.plot(실시간데이터,color="k")
            plt.show()
        if len(self.가격리스트)>0: 
            plt.title("Target")
            plt.plot(self.가격리스트,color="k")
            plt.plot(self.매수진입인덱스,self.매수진입가격리스트,color="r",linestyle="--")
            plt.plot(self.매도진입인덱스,self.매도진입가격리스트,color="b",linestyle="--")
            # plt.plot(self.진입인덱스,self.진입가격리스트,color="g",linestyle="--")  
            plt.scatter(self.매수인덱스,self.매수가격,color="r",s=20)
            plt.scatter(self.매도인덱스,self.매도가격,color="b",s=20)
            plt.scatter(self.손절인덱스,self.손절가격,color="m",s=100)
            plt.scatter(self.익절인덱스,self.익절가격,color="g",s=100)
            plt.scatter(self.청산인덱스,self.청산가격,color="y",s=300,marker="*")
            plt.show()
            plt.title("Asset")
            plt.plot(self.자산리스트,color="g")
            plt.scatter(self.청산인덱스,self.청산자산,color="y",s=300,marker="*")
            plt.show()

    def 백테스트상세정보(self):
        if len(self.가격리스트)>0: 
            print("-----------------------------------")
            print(         "백테스트 상세정보")
            print("-----------------------------------")
            print("매수평균가격:",round(np.nanmean(self.매수가격),5),"매도평균가격:",round(np.nanmean(self.매도가격),5))
            print("총매수횟수:",len(self.매수인덱스),"총매도횟수:",len(self.매도인덱스)) 
            print("거래대금:",self.거래대금) 
            print("거래량:",self.거래량)      
            print("총수수료:",self.수수료)
            print("최저매수가용자산:",np.nanmin(self.매수가용자산리스트))
            print("최저매도가용자산:",np.nanmin(self.매도가용자산리스트))
            print("매매실패횟수:",self.매매실패횟수)
            print("최고누적수익률:",round(np.nanmax(self.누적수익률리스트),3),"%")
            print("최저누적수익률:",round(np.nanmin(self.누적수익률리스트),3),"%")
            if (len(self.익절인덱스)+len(self.손절인덱스))>0:
                print("승률:",len(self.익절인덱스)/(len(self.익절인덱스)+len(self.손절인덱스))*100,"%")
        else:
            print("백테스트 정보가 없습니다.")