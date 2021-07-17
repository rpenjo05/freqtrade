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
    # Based on a backtesting:
    # - the best perfomance is reached with "max_open_trades" = 2 (in average for any market),
    #   so it is better to increase "stake_amount" value rather then "max_open_trades" to get more profit
    # - if the market is constantly green(like in JAN 2018) the best performance is reached with
    #   "max_open_trades" = 2 and minimal_roi = 0.01
     # ROI table:
    
    """#Sharpe 3.28
    minimal_roi = {
        "0": 0.01801,
        "90": 0.01617,
        "101": 0.01298,
        "156": 0.01085,
        "159": 0.00971,
        "269": 0.00769,
        "367": 0.00621,
        "525": 0.00411,
        "547": 0.00199,
        "591": 0.00182,
        "806": 0
    }

    # Stoploss:
    stoploss = -0.30333
    
    
    # Sharpe = 8.41941
    # ROI table:
    minimal_roi = {
        "0": 0.03266,
        "19": 0.02882,
        "175": 0.02636,
        "344": 0.02409,
        "450": 0.02021,
        "637": 0.01556,
        "791": 0.0106,
        "1089": 0.00833,
        "1243": 0.00398,
        "1533": 0.00232,
        "1704": 0
    }

    # Stoploss:
    stoploss = -0.13996
    
    #Sharpe = -6.95445
    # ROI table:
    minimal_roi = {
        "0": 0.01801,
        "32": 0.01545,
        "81": 0.01343,
        "244": 0.01199,
        "392": 0.0106,
        "538": 0.00939,
        "714": 0.00805,
        "1003": 0.00683,
        "1249": 0.00208,
        "1308": 0.00168,
        "1515": 0
    }

    # Stoploss:
    stoploss = -0.13996
    
    #Sharpe = -7.69751, avg=51.2m
    # ROI table:
    minimal_roi = {
        "0": 0.02095,
        "28": 0.01602,
        "260": 0.01431,
        "481": 0.01326,
        "664": 0.01168,
        "713": 0.01017,
        "777": 0.00609,
        "829": 0.00508,
        "990": 0.00369,
        "1266": 0.0021,
        "1554": 0
    }

    # Stoploss:
    stoploss = -0.21781 
    
    # ROI table:
    minimal_roi = {
        "0": 0.03697,
        "58": 0.03269,
        "87": 0.02786,
        "380": 0.02401,
        "398": 0.02027,
        "513": 0.01853,
        "631": 0.01553,
        "823": 0.01319,
        "1044": 0.00854,
        "1072": 0.00364,
        "1226": 0
    }

    # Stoploss:
    stoploss = -0.3164
    
    # ROI table:
    minimal_roi = {
        "0": 0.03612,
        "230": 0.03225,
        "298": 0.02784,
        "545": 0.02297,
        "752": 0.01822,
        "950": 0.01381,
        "1066": 0.00974,
        "1257": 0.00843,
        "1389": 0.00675,
        "1615": 0.00195,
        "1893": 0
    } 
    
    # ROI table:
    minimal_roi = {
        "0": 0.03287,
        "127": 0.03025,
        "185": 0.02531,
        "351": 0.02233,
        "642": 0.01784,
        "818": 0.01542,
        "1023": 0.01111,
        "1062": 0.0073,
        "1150": 0.00363,
        "1366": 0.0034,
        "1649": 0
    } """
    # ROI table:
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
