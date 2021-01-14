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
	def sell_strategy_generator(params: Dict[str, Any]) -> Callable:
		"""
		Define the sell strategy parameters to be used by hyperopt
		"""
		def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
			# print(params)
			conditions = []
			# GUARDS AND TRENDS
			if 'sell-rsi-enabled' in params and params['sell-rsi-enabled']:
				conditions.append(dataframe['sell-rsi'] > params['sell-rsi-value'])

			# TRIGGERS
			if 'sell-trigger' in params:
				if params['sell-trigger'] == 'sell-bb_lower2':
				    conditions.append(dataframe['close'] > dataframe['bb_lowerband2'])
				if params['sell-trigger'] == 'sell-bb_middle2':
				    conditions.append(dataframe['close'] > dataframe['bb_middleband2'])
				if params['sell-trigger'] == 'sell-bb_upper2':
				    conditions.append(dataframe['close'] > dataframe['bb_upperband2'])

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
		return [
		    Integer(60, 100, name='sell-rsi-value'),
		    Categorical([True, False], name='sell-rsi-enabled'),
		    Categorical(['sell-bb_lower2',
				 'sell-bb_middle2',
				 'sell-bb_upper2'], name='sell-trigger')
		]

	
	@staticmethod
	def generate_roi_table(params: Dict) -> Dict[int, float]:

		roi_table = {}
		roi_table[0] = params['roi_p1'] + params['roi_p2'] + params['roi_p3'] + params['roi_p4'] + params['roi_p5'] + params['roi_p6'] + params['roi_p7'] + params['roi_p8'] + params['roi_p9'] + params['roi_p10']
		roi_table[params['roi_t10']] = params['roi_p1'] + params['roi_p2'] + params['roi_p3'] + params['roi_p4'] + params['roi_p5'] + params['roi_p6'] + params['roi_p7'] + params['roi_p8'] + params['roi_p9']
		roi_table[params['roi_t10'] + params['roi_t9']] = params['roi_p1'] + params['roi_p2'] + params['roi_p3'] + params['roi_p4'] + params['roi_p5'] + params['roi_p6'] + params['roi_p7'] + params['roi_p8']
		roi_table[params['roi_t10'] + params['roi_t9'] + params['roi_t8']] = params['roi_p1'] + params['roi_p2'] + params['roi_p3'] + params['roi_p4'] + params['roi_p5'] + params['roi_p6'] + params['roi_p7']
		roi_table[params['roi_t10'] + params['roi_t9'] + params['roi_t8'] + params['roi_t7']] = params['roi_p1'] + params['roi_p2'] + params['roi_p3'] + params['roi_p4'] + params['roi_p5'] + params['roi_p6']
		roi_table[params['roi_t10'] + params['roi_t9'] + params['roi_t8'] + params['roi_t7'] + params['roi_t6']] = params['roi_p1'] + params['roi_p2'] + params['roi_p3'] + params['roi_p4'] + params['roi_p5']
		roi_table[params['roi_t10'] + params['roi_t9'] + params['roi_t8'] + params['roi_t7'] + params['roi_t6'] + params['roi_t5']] = params['roi_p1'] + params['roi_p2'] + params['roi_p3'] + params['roi_p4']
		roi_table[params['roi_t10'] + params['roi_t9'] + params['roi_t8'] + params['roi_t7'] + params['roi_t6'] + params['roi_t5'] + params['roi_t4']] = params['roi_p1'] + params['roi_p2'] + params['roi_p3']
		roi_table[params['roi_t10'] + params['roi_t9'] + params['roi_t8'] + params['roi_t7'] + params['roi_t6'] + params['roi_t5'] + params['roi_t4'] + params['roi_t3']] = params['roi_p1'] + params['roi_p2']
		roi_table[params['roi_t10'] + params['roi_t9'] + params['roi_t8'] + params['roi_t7'] + params['roi_t6'] + params['roi_t5'] + params['roi_t4'] + params['roi_t3'] + params['roi_t2']] = params['roi_p1']
		roi_table[params['roi_t10'] + params['roi_t9'] + params['roi_t8'] + params['roi_t7'] + params['roi_t6'] + params['roi_t5'] + params['roi_t4'] + params['roi_t3'] + params['roi_t2'] + params['roi_t1']] = 0

		return roi_table

	@staticmethod
	def roi_space() -> List[Dimension]:

		return [
		    Integer(1, 300, name='roi_t10'),
		    Integer(1, 300, name='roi_t9'),
		    Integer(1, 300, name='roi_t8'),
		    Integer(1, 300, name='roi_t7'),
		    Integer(1, 300, name='roi_t6'),
		    Integer(1, 300, name='roi_t5'),
		    Integer(1, 300, name='roi_t4'),
		    Integer(1, 300, name='roi_t3'),
		    Integer(1, 300, name='roi_t2'),
		    Integer(1, 300, name='roi_t1'),

		    Real(0.001, 0.005, name='roi_p10'),
		    Real(0.001, 0.005, name='roi_p9'),
		    Real(0.001, 0.005, name='roi_p8'),
		    Real(0.001, 0.005, name='roi_p7'),
		    Real(0.001, 0.005, name='roi_p6'),
		    Real(0.001, 0.005, name='roi_p5'),
		    Real(0.001, 0.005, name='roi_p4'),
		    Real(0.001, 0.005, name='roi_p3'),
		    Real(0.0001, 0.005, name='roi_p2'),
		    Real(0.0001, 0.005, name='roi_p1'),
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
		    (dataframe['sell-rsi'] > 60) &
            		(dataframe['close'] > dataframe['bb_middleband2']),
		    'sell'
		] = 1
		return dataframe
