"""
Basic ML demo example
"""
import numpy
import sys
import os
import datetime
import urllib2
import re

class CollectData(object):
    def __init__(self):
        self._url = ("https://archive.ics.uci.edu/ml/machine-learning-"
                     "databases/undocumented/connectionist-bench/"
                     "sonar/sonar.all-data")
        self._collecteddata_list = []
        self._data = None

    @property
    def urldata(self):
        return self._data

    def _collectdata_1_fetch(self):
        with open("data", "r") as d:
            self._data = d.readlines()

    @property
    def datalist(self):
        return self._collecteddata_list

    def _collectdata_2_xlist(self):
        for line in self.urldata:
            #split on comma
            row = line.strip().split(",")
            self._collecteddata_list.append(row)


def collect():
    def sortcb(cb_name):
        return int(cb_name.split("_")[2])

    collectdata = CollectData()
    for cb in sorted([_cb for _cb in dir(collectdata)
                      if _cb.startswith("_collectdata_")], key=sortcb):
        getattr(collectdata, cb)()
    return collectdata.datalist


class SummaryStatistics(object):
    def __init__(self):
        self._col_to_sumup = 3
        self._col_last = 60
        self._ntiles = [4, 10]
        self._col_data = []
        self._collected_data = collect()
        for collec_data in self._collected_data:
            self._col_data.append(float(collec_data[self._col_to_sumup]))

    @property
    def colarray(self):
        return numpy.array(self._col_data)

    @property
    def colmean(self):
        return numpy.mean(self.colarray)

    @property
    def colsd(self):
        return numpy.std(self.colarray)

    @property
    def display_bdry(self):
        for _i in self._ntiles:
            percentBdry = []
            for i in range(_i+1):
                percentBdry.append(numpy.percentile(self.colarray, i*(100)/_i))
            print "%d Percentile" % _i
            print percentBdry

    def get_counts_per_category(self):
        last_col_data = [row[self._col_last] for row in self._collected_data]
        unique_last_col_data = set(last_col_data)
        print unique_last_col_data
        cat_count_dict = dict(zip(list(unique_last_col_data),
                                  range(len(unique_last_col_data))))
        cat_count = [0] * len(unique_last_col_data)
        for elt in last_col_data:
            cat_count[cat_count_dict[elt]] += 1
        print cat_count

    def __repr__(self):
        return "\n".join(["SummaryStatistics",
                          "-" * len("SummaryStatistics"),
                          "Mean  = %s" % str(self.colmean),
                          "STD.D = %s" % str(self.colsd)])


ss = SummaryStatistics()
print ss
ss.display_bdry
ss.get_counts_per_category()
