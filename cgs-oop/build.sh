echo "INSTALLING DEPENDENCIES"
pip3 install matplotlib
pip3 install pillow
pip3 install numpy
pip3 install pandas
pip3 install requests
pip3 install scipy
pip3 install setuptools
pip3 install scikit-image
pip3 install deap

echo "DOWNLOADING NLTK CORPUS OF WORDS"
python3 download_nltk.py
echo "DOWNLOADED NLTK WORDS"
