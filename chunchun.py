#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import datetime
import urllib2
import json
from requests_oauthlib import OAuth1Session
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED

class Configuration(object):
    FILENAME = 'conf.json'

    def __init__(self):
        with open(self.FILENAME, 'r') as f:
            conf = json.load(f)
            self.CK = conf['conf']['account']['CK']
            self.CS = conf['conf']['account']['CS']
            self.AT = conf['conf']['account']['AT']
            self.AS = conf['conf']['account']['AS']
            self.lat = conf['conf']['location']['lat']
            self.lon = conf['conf']['location']['lon']
            self.locname = conf['conf']['location']['name']

            print('%s %s %s' % (self.lat, self.lon, self.locname))

class Chunchun(object):
    next_sunrise = None

    def __init__(self, conf):
        self.conf = conf

    def get_sunrise(self, url):
        r = urllib2.urlopen(url)
        js = r.read()
        return self.parse(js)
        
    def parse(self, js):
        data = json.loads(js)
        for event in data['result']['event']:
            t = event['type']
            b = event['boundary']
            if t == u'daytime' and b == u'start':
                time = event['time'].split('+')[0]
                return datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M')

    def tweet(self):
        url = 'https://api.twitter.com/1.1/statuses/update.json'
        time = self.next_sunrise.strftime('%Y/%m/%d %H:%M')
        params = {'status': '(・8・)ﾁｭﾝﾁｭﾝ 南ことりが日の出をお知らせします♪ - %s %s' % (time, self.conf.locname.encode('utf-8'))}
        CK = self.conf.CK
        CS = self.conf.CS
        AT = self.conf.AT
        AS = self.conf.AS
        tw = OAuth1Session(CK, CS, AT, AS)
        req = tw.post(url, params=params)
        if req.status_code == 200:
            print('OK')
        else:
            print('Error: %s' % req)

    def update_sunrise(self):
        URL = 'http://www.finds.jp/ws/movesun.php?jsonp=&y=%s&m=%s&d=%s&lat=%s&lon=%s&tz=9'
        dt = datetime.date.today() + datetime.timedelta(days=1)
        request_url = URL % (dt.year, dt.month, dt.day, self.conf.lat, self.conf.lon)
        self.next_sunrise = self.get_sunrise(request_url)
        print('next_sunrise:' + self.next_sunrise.strftime('%Y/%m/%d %H:%M'))

    def do_post(self):
        self.tweet()
        self.update_sunrise()

    running = False

    def start_schedule(self):
        sched = BackgroundScheduler()
        job = sched.add_job(self.do_post, 'date', run_date=chun.next_sunrise)
        sched.add_listener(self.job_executed_listener, EVENT_JOB_EXECUTED)
        sched.start()
        try:
            while True:
                self.running = True
                while self.running:
                    time.sleep(10)
                job.remove()
                job = sched.add_job(self.do_post, 'date', run_date=self.next_sunrise)
        except (KeyboardInterrupt, SystemExit):
            sched.shutdown()

    def job_executed_listener(self, event):
        self.running = False


if __name__ == '__main__':
    chun = Chunchun(Configuration())
    chun.update_sunrise()
    chun.start_schedule()
