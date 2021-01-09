import talib.abstract as ta
from pandas import DataFrame
from typing import Dict, Any, Callable, List
from functools import reduce

from skopt.space import Categorical, Dimension, Integer, Real

import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.optimize.hyperopt_interface import IHyperOpt

class_name = 'CombinedBinHAndClucOpt'


class CombinedBinHAndClucOpt(IHyperOpt):


		
	@staticmethod
	def buy_strategy_generator(params: Dict[str, Any]) -> Callable:
		"""
		Define the buy strategy parameters to be used by hyperopt
		"""
		def populate_buy_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
			"""
			Buy strategy Hyperopt will build and use.
			"""
			conditions = []

			# GUARDS AND TRENDS
			if 'BinHV45' in params and params['BinHV45']:
				conditions.append(	dataframe['lower'].shift().gt(0) &
				    dataframe['bbdelta'].gt(dataframe['close'] * 0.008) &
				    dataframe['closedelta'].gt(dataframe['close'] * 0.0175) &
				    dataframe['tail'].lt(dataframe['bbdelta'] * 0.25) &
				    dataframe['close'].lt(dataframe['lower'].shift()) &
				    dataframe['close'].le(dataframe['close'].shift())	)
			if 'ClucMay72018' in params and params['ClucMay72018']:
				conditions.append(	(dataframe['close'] < dataframe['ema_slow']) &
				    (dataframe['close'] < 0.985 * dataframe['bb_lowerband']) &
				    (dataframe['volume'] < (dataframe['volume_mean_slow'].shift(1) * 20))	)
			# TRIGGERS
			# if 'trigger' in params:
			#    if params['trigger'] == 'bb_lower':
			#        conditions.append(dataframe['close'] < dataframe['bb_lowerband'])
			#    if params['trigger'] == 'macd_cross_signal':
			#        conditions.append(qtpylib.crossed_above(
			#            dataframe['macd'], dataframe['macdsignal']
			#        ))
			#    if params['trigger'] == 'sar_reversal':
			#        conditions.append(qtpylib.crossed_above(
			#            dataframe['close'], dataframe['sar']
			#        ))

			# Check that volume is not 0
			conditions.append(dataframe['volume'] > 0)

			if conditions:
				dataframe.loc[
				    reduce(lambda x, y: x | y, conditions),
				    'buy'] = 1

			return dataframe

		return populate_buy_trend
		
	@staticmethod
	def indicator_space() -> List[Dimension]:
		"""
		Define your Hyperopt space for searching buy strategy parameters.
		"""
		return [
		    Categorical([True, False], name='BinHV45'),
		    Categorical([True, False], name='ClucMay72018'),
		    # Categorical([True, False], name='rsi-enabled'),
		    # Categorical(['bb_lower', 'macd_cross_signal', 'sar_reversal'], name='trigger')
		]
		
	@staticmethod
	def sell_strategy_generator(params: Dict[str, Any]) -> Callable:
		"""
		Define the sell strategy parameters to be used by hyperopt
		"""
		def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
		    """
		    Sell strategy Hyperopt will build and use
		    """
		    # print(params)
		    conditions = []
		    # GUARDS AND TRENDS
		    #if 'sell-rsi-enabled' in params and params['sell-rsi-enabled']:
		    #    conditions.append(dataframe['sell-rsi'] > params['sell-rsi-value'])

		    # TRIGGERS
		    if 'sell-trigger' in params:
		        if params['sell-trigger'] == 'sell-bb_middleband1':
		            conditions.append(dataframe['close'] > dataframe['bb_middleband1'])
		        if params['sell-trigger'] == 'sell-bb_middleband2':
		            conditions.append(dataframe['close'] > dataframe['bb_middleband2'])
		        if params['sell-trigger'] == 'sell-bb_middleband3':
		            conditions.append(dataframe['close'] > dataframe['bb_middleband3'])

		    if not conditions:
		        pass
		    else:
		        dataframe.loc[
		            reduce(lambda x, y: x & y, conditions),
		            'sell'] = 1

		    return dataframe

		return populate_sell_trend
		
	@staticmethod
	def sell_indicator_space() -> List[Dimension]:
		"""
		Define your Hyperopt space for searching sell strategy parameters
		"""
		return [
		    Categorical(['sell-bb_middleband1',
		                 'sell-bb_middleband2',
		                 'sell-bb_middleband3'], name='sell-trigger')
		]
		
		

		
		
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
		    (dataframe['close'] > dataframe['bb_middleband']),
		    'sell'
		] = 1
		return dataframe
