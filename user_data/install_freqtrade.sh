conda create -n freqtrade python=3.8
conda activate freqtrade
git clone https://github.com/freqtrade/freqtrade.git
git clone https://github.com/rpenjo05/freqtrade_strategies.git
#git clone --single-branch --branch stable https://github.com/freqtrade/freqtrade.git
cd freqtrade
chmod 777 setup.sh
./setup.sh --install
wget https://raw.githubusercontent.com/rpenjo05/freqtrade/develop/user_data/config.json
mv config.json user_data/
wget https://raw.githubusercontent.com/rpenjo05/freqtrade/develop/user_data/hyperopts/combine_opt.py
mv combine_opt.py user_data/hyperopts/
wget https://raw.githubusercontent.com/rpenjo05/freqtrade/develop/user_data/strategies/CombinedBinHAndCluc.py
mv CombinedBinHAndCluc.py user_data/strategies/
