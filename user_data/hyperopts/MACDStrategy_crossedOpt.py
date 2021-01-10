import talib.abstract as ta
from pandas import DataFrame
from typing import Dict, Any, Callable, List
from functools import reduce

from skopt.space import Categorical, Dimension, Integer, Real

import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.optimize.hyperopt_interface import IHyperOpt

class_name = 'MACDStrategy_crossedOpt'


class MACDStrategy_crossedOpt(IHyperOpt):


		
	
	
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
    		    Real(0.0001, 0.005, name='roi_p1'),]
        
    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the buy signal for the given dataframe
        :param dataframe: DataFrame
        :return: DataFrame with buy column
        """
        dataframe.loc[
            (
                qtpylib.crossed_above(dataframe['macd'], dataframe['macdsignal']) &
                (dataframe['cci'] <= -50.0)
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the sell signal for the given dataframe
        :param dataframe: DataFrame
        :return: DataFrame with buy column
        """
        dataframe.loc[
            (
                qtpylib.crossed_below(dataframe['macd'], dataframe['macdsignal']) &
                (dataframe['cci'] >= 100.0)
            ),
            'sell'] = 1

        return dataframe
