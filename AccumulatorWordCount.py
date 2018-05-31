# Sample spark script to use customized accumulators
# Author: Mateusz Dolinski

from pyspark import SparkConf, SparkContext
from pyspark.accumulators import AccumulatorParam


class WordAccumulator(AccumulatorParam):
    """
    Accumulator for saving words.

    Accumulator that stores words appearing in text.
    in form of dictionary {word: #_of_occurences_in_text}
    """

    def zero(self, value):
        """
        Method for setting counter to zero.
        :param: value: currently unused
        :return: empty dictionary
        """
        return {}
        
    def addInPlace(self, v1, v2):
        """
        Function for accumulator incrementation.
        It merges two dictionaries.
        :param v1:
        :param v2:
        :return: incremented accumulator
        """
        if len(v1.keys()) == 0:
            return v2
        for key in v2.keys():
            if key in v1.keys():
                v1[key] += v2[key]
            else:
                v1[key] = v2[key]
        return v1


conf = SparkConf() \
       .setAppName('Wordcount') \
       .setMaster('local[*]')
       
sc = SparkContext(conf = conf)

wordcount = sc.accumulator({}, WordAccumulator())

sample_file = sc.textFile('/path/to/sample/textfile/on/hdfs') \
              .flatMap(lambda line: line.split(' ')) \
              .filter(lambda word: word != '') \
              .map(lambda word: {word: 1}) \
              .foreach(lambda pair: wordcount.add(pair))

print(wordcount.value)
