#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   logsReader.py
@Time    :   2023/04/22 18:02:59
@Desc    :   Handlers for file reading and logs processing
'''

import os

import numpy as np
import pandas as pd


class FileHandler:
    """
    File reader for individual logs.
    For batch processing, see the FileAggregator class below.
    """
    def __init__(self, filename:str) -> None:
        """
        Constructor for file handler

        Parameters
        ----------
        filename : str
            filename to read
        """
        self._filename = filename
        self._log = pd.read_csv(filename, sep=';', decimal=',', names = ['x', 'y'])
    
    @property
    def content(self) -> pd.DataFrame:
        """
        Returns the data contained in the file handler
        """
        return self._log
    
    def expand(self, missing_length:int) -> None:
        """
        Expands the log in place with nan

        Parameters
        ----------
        missing_length : int
            missing length
        """
        self._log = pd.concat([self.content, pd.DataFrame(np.asarray([[np.nan, np.nan]]*missing_length), columns=['x', 'y'])], axis=0)  # noqa: E501
    
    @property
    def filename(self) -> str:
        """
        Returns the filename in the file handler
        """
        return self._filename


    def __repr__(self) -> str:

        return(self.filename)

class FileAggregator:
    """
    File aggregator for logs.
    For individual logs, see the FileHandler class above.
    """
    def __init__(self, dir:str) -> None:
        """
        Constructor for FileAggregator object

        Parameters
        ----------
        dir : str
            path where all the logs are
        """
        self._logs = {}
        self._drops_indexes = {}
        for ind, f in enumerate(sorted(os.listdir(dir))):
            if ind == 0:
                ind = 'beacon'
            self._logs[ind] = FileHandler(os.path.join(dir, f))
        # Sort and filter short acquisitions
        master_len = -1
        for k in list(self._logs.keys()):
            if k == 'beacon':
                master_len = len(self._logs[k].content)
            else:
                if len(self._logs[k].content) != master_len:
                    missing_values = master_len - len(self._logs[k].content)
                    self._drops_indexes[k] = len(self._logs[k].content)
                    self._logs[k].expand(missing_values)
                    
    @property
    def disconnections(self) -> dict:
        """
        Get which robots lost connection and when they did

        Returns
        -------
        dict
            dict with robot ids as keys and drop step as values
        """
        return self._drops_indexes

    @property
    def get_number_of_followers(self) -> int:
        """
        Returns the number of follower robots

        Returns
        -------
        int
            number of follower robots
        """
        return len(list(self._logs.keys()))-1

    def get_center(self) -> pd.DataFrame:
        """
        Get the center of the swarm

        Returns
        -------
        pd.DataFrame
            Center (x,y) of the swarm at every step
        """
        keys = list(self._logs.keys())[1:]
        xs, ys = {}, {}
        for k in keys:
            xs[k] = self._logs[k].content['x'].to_numpy()
            ys[k] = self._logs[k].content['y'].to_numpy()
        xs = pd.DataFrame.from_dict(xs, orient='columns')
        ys = pd.DataFrame.from_dict(ys, orient='columns')
        # replace NaN
        xs.apply(lambda row: row.fillna(row.mean()), axis=1)
        ys.apply(lambda row: row.fillna(row.mean()), axis=1)

        return pd.concat([xs.mean(1), ys.mean(1)], keys=['x', 'y'], axis=1)

    def get_beacon(self) -> pd.DataFrame:
        """
        Get the beacon position

        Returns
        -------
        pd.DataFrame
            Position (x,y) of the beacon at every step
        """
        return self._logs['beacon'].content
    
    def get_distance(self) -> pd.DataFrame:
        """
        Get the distance between the center of the swarm and the real beacon position

        Returns
        -------
        pd.DataFrame
            distance (pandas dataframe with a single column) between swarm center and beacon at every step
        """  # noqa: E501
        poly_center = self.get_center()

        beacon = self.get_beacon()
        return (poly_center-beacon).pow(2).sum(axis = 1).pow(0.5)
    
    @property
    def logs(self) -> dict:
        """
        ICE, to directly access the logs

        Returns
        -------
        dict
            dict with FileHandler instances as values
        """
        return self._logs