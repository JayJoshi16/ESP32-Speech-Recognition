# Simplest ESP32 offline Speech Recognition using MEMS SPM1423 I2S microphone

  
  
**STEP 1** : First open the **FIRMWARE** folder and upload the `speech-commands-firmware.bin` Firmware into the ESP32 Board.  
  
  
  
 **STEP 2** : Train your model for the WORDS you want to recognise, at https://www.tinkerdoodle.cc/user/junfeng/speech-commands.html . Click on `Add audio samples` to add audio samples of your words(like Lighton,hello,....).  
  
  

**STEP 3** : click on `Train Model` to train and after that then click on `Download Model`. Now you will have a `speech_model.py` python file.This will works as a library (trained speech model) for your code.  
(In My case i renamed this downloaded model into `speech_model_library.py` inside the **LIBRARY** folder in my repo).  

**STEP 4** : Upload this `speech_model.py` file onto ESP32 board.  

**STEP 5** : Connect the "SPM1423" microphone to the ESP32.  ![Screenshot (8)](https://user-images.githubusercontent.com/86542830/161415619-2a52a82b-5a9b-4643-9a7e-5c9a1656dda8.png)  

**STEP 6** : Upload the `main.py` code to ESP32.  
(Note that here you have to change the **LABEL** words (and logic too) according to your model.Eg change the Wake Up word "RIGHT" to whatever you've trained.)
