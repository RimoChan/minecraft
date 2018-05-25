import datetime

class clock():
    def tick(self):
        try:
            now=datetime.datetime.now()
            dif=now-self.pre
            ans=dif.seconds+dif.microseconds/(10**6)
            self.bp=self.pre
            self.pre=now
            return ans
        except Exception as e: 
            # print(e)
            self.pre=datetime.datetime.now()
            return 0
    def back(self):
        try:
            self.pre=self.bp
        except Exception as e:
            return  
            # print(e)
