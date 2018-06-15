
import math
import random
import sys, os

import pandas as pd
import numpy as np

from parse import parse

def calc_games(game_df, score_df, cur_game_id, cur_status):

    if cur_game_id == game_df.shape[0]:


    return result_df



def run(score_filename, game_filename):

    df = pd.read_csv(score_filename)
    print df.shape

    nations = list(df['nation1'].unique()) + list(df['nation2'].unique())
    nations = list(set(nations))

    print nations

    game_df = pd.read_csv(game_filename)

    result = calc_games(game_df, df, 0, cur_status)

    print result




if __name__ == '__main__':
    score_filename = 'probability_score.csv'
    game_filename = 'probability_win.csv'
    run(score_filename, game_filename)

