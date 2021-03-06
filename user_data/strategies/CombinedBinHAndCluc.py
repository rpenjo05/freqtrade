# --- Do not remove these libs ---
import freqtrade.vendor.qtpylib.indicators as qtpylib
import numpy as np
# --------------------------------
import talib.abstract as ta
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame


def bollinger_bands(stock_price, window_size, num_of_std):
    rolling_mean = stock_price.rolling(window=window_size).mean()
    rolling_std = stock_price.rolling(window=window_size).std()
    lower_band = rolling_mean - (rolling_std * num_of_std)
    return np.nan_to_num(rolling_mean), np.nan_to_num(lower_band)


class CombinedBinHAndCluc(IStrategy):
	# ROI table:
	minimal_roi = {
	"0": 0.02068,
	"74": 0.01778,
	"142": 0.01453,
	"226": 0.01207,
	"231": 0.00739,
	"352": 0.00603,
	"386": 0.0048,
	"443": 0.00368,
	"572": 0.00251,
	"663": 0.00038,
	"798": 0
	}

	# Stoploss:
	stoploss = -0.346

	use_sell_signal = True
	sell_profit_only = True
	ignore_roi_if_buy_signal = False

	def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
		# strategy BinHV45
		mid, lower = bollinger_bands(dataframe['close'], window_size=40, num_of_std=2)
		dataframe['lower'] = lower
		dataframe['bbdelta'] = (mid - dataframe['lower']).abs()
		dataframe['closedelta'] = (dataframe['close'] - dataframe['close'].shift()).abs()
		dataframe['tail'] = (dataframe['close'] - dataframe['low']).abs()
		# strategy ClucMay72018
		bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
		dataframe['bb_lowerband'] = bollinger['lower']
		dataframe['bb_middleband'] = bollinger['mid']
		dataframe['ema_slow'] = ta.EMA(dataframe, timeperiod=50)
		dataframe['volume_mean_slow'] = dataframe['volume'].rolling(window=30).mean()
		
		bollinger1 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=1)
		dataframe['bb_lowerband1'] = bollinger1['lower']
		dataframe['bb_middleband1'] = bollinger1['mid']
		dataframe['bb_upperband1'] = bollinger1['upper']
		
		bollinger2 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=40, stds=2)
		dataframe['bb_lowerband2'] = bollinger2['lower']
		dataframe['bb_middleband2'] = bollinger2['mid']
		dataframe['bb_upperband2'] = bollinger2['upper']
		
		bollinger3 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=40, stds=3)
		dataframe['bb_lowerband3'] = bollinger3['lower']
		dataframe['bb_middleband3'] = bollinger3['mid']
		dataframe['bb_upperband3'] = bollinger3['upper']
		
		
		dataframe['sell-rsi'] = ta.RSI(dataframe)
		dataframe['buy-rsi_b'] = ta.RSI(dataframe)
		dataframe['buy-rsi_c'] = ta.RSI(dataframe)
		dataframe['buy-rsi'] = ta.RSI(dataframe)

		return dataframe

	def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
		dataframe.loc[
			(  # strategy BinHV45
				dataframe['lower'].shift().gt(0) &
				dataframe['bbdelta'].gt(dataframe['close'] * 0.008) &
				dataframe['closedelta'].gt(dataframe['close'] * 0.0175) &
				dataframe['tail'].lt(dataframe['bbdelta'] * 0.25) &
				dataframe['close'].lt(dataframe['lower'].shift()) &
				dataframe['close'].le(dataframe['close'].shift())
			) |
			(  # strategy ClucMay72018
				(dataframe['close'] < dataframe['ema_slow']) &
				(dataframe['close'] < 0.985 * dataframe['bb_lowerband']) &
				(dataframe['volume'] < (dataframe['volume_mean_slow'].shift(1) * 20))
			),
			'buy'
		] = 1
		return dataframe

	def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
		"""
		"""
		dataframe.loc[
			(qtpylib.crossed_below(dataframe['sell-rsi'], 83) ) &
			(dataframe['close'] > dataframe['bb_middleband2'])
			
			,
			'sell'
		] = 1
		return dataframe
