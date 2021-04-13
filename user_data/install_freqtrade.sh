conda create -n freqtrade python=3.8
conda activate freqtrade
git clone --single-branch --branch stable https://github.com/freqtrade/freqtrade.git
cd freqtrade
chmod 777 setup.sh
./setup.sh --install
