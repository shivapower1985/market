class parser:
    def __init__(self, dt,url):
        self.dt=dt
        self.url=url
    
    def parse_url(self):
        return self.url.replace("{date}",self.dt)
