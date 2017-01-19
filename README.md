# RPi_Translator
Raspberry Pi project created to assist reading books in different languages. The goal of the RPi_Translator is to quickly provide a translation or English definition of a word so that you can spend less time looking up what a word means, and more time reading! 

### Prototype Results

# Configuration and Installation Steps #
### OpenCV ###
* For installing OpenCV on the Raspberry Pi refer to these useful resources:
 * http://docs.opencv.org/trunk/d7/d9f/tutorial_linux_install.html
 * https://github.com/MicrocontrollersAndMore/Raspberry_Pi_2_and_OpenCV_3_Tutorial_Part_1/blob/master/Raspberry%20Pi%202%20%2B%20OpenCV%203%20Cheat%20Sheet.txt
 * http://www.pyimagesearch.com/2015/12/14/installing-opencv-on-your-raspberry-pi-zero/

### Tesseract  ###
Tesseract versions and the minimum version of Leptonica required:

Tesseract     | Leptonica     | Ubuntu
:-----------: | :-----------: | :-----------:
4.00          | 1.74.0        | Must build from source
3.04          | 1.71          | Ubuntu 16.04
3.03          | 1.70          | Ubuntu 14.04
3.02          | 1.69          | Ubuntu 12.04

I wanted to install the most recent version of Tesseract so I built it from source. The Tesseract GitHub page has good instructions (https://github.com/tesseract-ocr/tesseract/wiki/Compiling), but I will show the main steps I took as another reference.
 * Building Leptonica from source: https://tpgit.github.io/UnOfficialLeptDocs/leptonica/README.html#building-leptonica
  * The latest version can be found here : http://www.leptonica.org/download.html
  * cd ~/Downloads
  * wget http://www.leptonica.org/source/leptonica-1.74.1.tar.gz
  * gunzip leptonica-1.74.1.tar.gz
  * tar -xvf leptonica-1.74.1.tar
  * cd leptonica-1.74.1/
  * ./configure [build the makefile]
  * sudo make [builds the library and shared library versions of all the progs (this took a while!)]
  * sudo make install [as root; this puts liblept.a into /usr/local/lib/ and all the progs into /usr/local/bin/ ]
 * In addition to Leptonica, the following libraries are needed:
  * sudo apt-get install autoconf automake libtool 
  * sudo apt-get install autoconf-archive 
  * sudo apt-get install pkg-config 
  * sudo apt-get install libpng12-dev 
  * sudo apt-get install libjpeg8-dev 
  * sudo apt-get install libtiff5-dev 
  * sudo apt-get install zlib1g-dev
 * Steps for tesseract:
  * git clone https://github.com/tesseract-ocr/tesseract.git 
  * cd tesseract 
  * ./autogen.sh 
  * ./configure --enable-debug 
  * LDFLAGS="-L/usr/local/lib" CFLAGS="-I/usr/local/include" make 
  * sudo make install 
  * sudo ldconfig
 * Download the languages you are interested in:
  * Set an environment variable to point to the parent directory of the tessdata directory. The tessdata directory stores the data file(s) of the language(s) you are interested in.
  * sudo nano .bashrc
  * Add a line such as: export TESSDATA_PREFIX=/home/pi/tesseract, and then close/reopen your terminal
  * Download language data, e.g. wget https://github.com/tesseract-ocr/tessdata/raw/4.00/eng.traineddata
  * Move it to the tesdata directory: mv eng.traineddata $TESSDATA_PREFIX/tessdata
 * Test if tesseract was properly downloaded:
  * In the command line try tesseract –list-langs and you should see the languages you downloaded earlier
  * Take a sample image and try: tesseract sample_image.jpg output.txt
 * Python wrapper for the tesseract-ocr API (tesserocr)
  * https://github.com/sirfz/tesserocr
  * Note that Cython is required for building
  
### Microsoft Translate API ###
 * For now Microsoft provides a translate service that is free for public use. Note that subscriptions, up to 2 million characters a month, are free. Translating more than 2 million characters per month requires a payment.
 * Sign up for a Microsoft Azure Marketplace API Key. I chose to store the key as an environment variable. 
 * If you are using python, a useful Microsoft Translate API wrapper can be found here: https://github.com/wronglink/mstranslator

### Merriam-Webster API 
 * The Merriam-Webster Dictionary API is free as long as it is for non-commercial use, usage does not exceed 1000 queries per day per API key, and use is limited to two reference APIs.
 * Create an account here https://www.dictionaryapi.com/
