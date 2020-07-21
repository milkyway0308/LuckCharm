import json
import random

import requests
from selenium import webdriver
from selenium.webdriver.chrome import options
from time import time

rChars = list(x for x in "abcdefghijklmnopqrstuvwxyz")


def randText():
    vals = ""
    length = random.randint(3, 12)
    while length > 0:
        length -= 1
        vals += rChars[random.randint(0, len(rChars) - 1)]
    return vals


def randEmail():
    email = ""
    length = random.randint(5, 8)
    while length > 0:
        length -= 1
        email += rChars[random.randint(0, len(rChars) - 1)]
    email += "@"
    length = random.randint(2, 5)
    while length > 0:
        length -= 1
        email += rChars[random.randint(0, len(rChars) - 1)]
    email += ".com"
    return email


def collectNext():
    opt = options.Options()
    opt.headless = True
    sel = webdriver.Chrome(options=opt)
    sel.get("https://www.alphavantage.co/support/")
    sel.find_element_by_id("organization-text").send_keys(randText())
    sel.find_element_by_id("email-text").send_keys(randEmail())
    sel.execute_script("""
        // AJAX for posting
    function create_post() {
        $.ajax({
            url : "/create_post/", // the endpoint
            type : "POST", // http method
            data : { first_text : 'deprecated',
                     last_text: 'deprecated',
                     occupation_text: $('#occupation-text').val(),
                     organization_text: $('#organization-text').val(),
                     email_text: $('#email-text').val()}, // data sent with the post request
            // handle a successful response
            success : function(json) {
                $('#occupation-text').val('Investor');
                $('#organization-text').val('');
                $('#email-text').val('');

                $('#talk').text(json.text);
                $('#submit-btn').text("GET FREE API KEY");
                $('#submit-btn').prop("disabled",true);
                grecaptcha.reset();

                if (json.text.includes('Welcome')) {
                    $('#container').show();
                    fireMultiple(5, 300, 500);
                    $('html, body').delay(2500).animate({
                        scrollTop: $("#post-details").offset().top
                    }, 2000, function () {
                      $('#container').hide();
                    });
                }

            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                $('#submit-btn').text("GET FREE API KEY");
                $('#submit-btn').prop("disabled",true);
                grecaptcha.reset();
            }
        });
    };
    create_post()
    """)
    from time import sleep

    va = sel.find_element_by_id("talk")
    txt = va.text
    while len(txt.strip()) is 0:
        sleep(0.01)
        va = sel.find_element_by_id("talk")
        txt = va.text
    sel.close()
    print(txt)
    if "Welcome" in txt:
        txt = txt.split("!")[1].split(".")[0].split(" ")[-1]
    else:
        print(txt)
        print("Failed to get key, retry...")
        return collectNext()
    return txt

    # sel.execute_script("")


class AlphaVentageAPIPool:
    def __init__(self):
        self._currentPool = list()
        self._datas = list()

    def getLastFreeKey(self):
        toRem = list()
        for x in self._currentPool:
            if x.isLimited():
                toRem.append(x)
            elif x.canUse():
                return x
        for x in toRem:
            self._currentPool.remove(x)
            del x
        print("No free key to use. Gathering new one...")
        newOne = collectNext()
        print("Success. Current key: " + newOne)
        self._datas.append(newOne)
        newOne = AlphaVentageAPIKey(newOne)
        self._currentPool.append(newOne)
        return newOne

    def write(self, file):
        file.write()


class AlphaVentageAPIKey:
    def __init__(self, text):
        self._key = text
        self._lastKeyInit = time()
        self._used = 0
        self._totalUsed = 0

    def key(self):
        return self._key

    def check(self):
        if time() - self._lastKeyInit > 70:
            self._used = 0
            self._lastKeyInit = time()
            print("Released.")

    def use(self):
        self.check()
        self._used += 1
        self._totalUsed += 1

    def canUse(self):
        self.check()
        print("Used: " + str(self._used) + " / " + self.key())
        return self._used < 5

    def isLimited(self):
        return self._totalUsed >= 500


if __name__ == '__main__':
    pool = AlphaVentageAPIPool()
    for x in range(1, 17):
        print("Loop.")
        key = pool.getLastFreeKey()
        key.use()
