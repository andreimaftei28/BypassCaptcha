import os
import sys
import speech_recognition as sr
import urllib
import pydub
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
from thug_life import thug_life

# do the bindings
# set the path where you have downloaded ffmpeg bindings
pydub.AudioSegment.converter = "C:\\ffmpeg\\bin\\ffmpeg.exe"
pydub.AudioSegment.ffmpeg = "C:\\ffmpeg\\bin\\ffmpeg.exe"
pydub.AudioSegment.ffprobe = "C:\\ffmpeg\\bin\\ffmpeg.exe"

# Check if the current version of chromedriver exists
# and if it doesn't exist, download it automatically,
# then add chromedriver to path
chromedriver_autoinstaller.install()

#create driver
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.get("https://www.google.com/recaptcha/api2/demo")
# comment the next line out if you are using only one display
driver.set_window_position(1601, 0)
driver.maximize_window()
driver.implicitly_wait(15)
#click on the check box
frames = driver.find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[0])
driver.find_element_by_class_name("recaptcha-checkbox-border").click()
#change to audio
driver.switch_to.default_content()
frames = driver.find_element_by_xpath("/html/body/div[2]/div[4]").find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[0])
driver.find_element_by_id("recaptcha-audio-button").click()
#click the play button
driver.switch_to.default_content()
frames = driver.find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[-1])
driver.find_element_by_xpath("/html/body/div/div/div[3]/div/button").click()
#get and record the audio file
src = driver.find_element_by_id("audio-source").get_attribute("src")

file_path = os.path.join(os.getcwd(), "sample.mp3")
urllib.request.urlretrieve(src, file_path)

sound = pydub.AudioSegment.from_mp3(file_path)
sound.export(file_path.replace("mp3", "wav"), format="wav")
sample_audio = sr.AudioFile(file_path.replace("mp3", "wav"))
rec = sr.Recognizer()
with sample_audio as source:
    audio = rec.record(source)
key = rec.recognize_google(audio)
print(f"Info\tRecaptcha Passcode: {key}")
#click the submit button
driver.find_element_by_id("audio-response").send_keys(key.lower())
time.sleep(5)
driver.find_element_by_id("audio-response").send_keys(Keys.RETURN)
driver.switch_to.parent_frame()
driver.find_element_by_css_selector('#recaptcha-demo-submit').click()
time.sleep(3)
driver.quit()

#thug_life
thug_life()
