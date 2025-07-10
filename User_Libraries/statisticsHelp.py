# statisticshelp.py
# Library for statistical calculations and data tokenization.
# Written by David Dueiri
# 7/9/2025
# This file contains helper functions for statistical calculations.
import math


from transformers import AutoTokenizer



class StatisticsHelper:
    def __init__(self):
        """Initialize the StatisticsHelper class."""
        pass


    #staticmethods are used for efficiency and to avoid the need for instantiation.
    @staticmethod
    def tokenize(data, alphaOrNum=3):
        """
        Tokenize a string using a pre-trained tokenizer.
        A user may input data of any type and have it tokenized to save time and energy.
        """
        tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        if isinstance(data, str):
            components = data.split()  # clean up the string by splitting on whitespace
        else:
            components = list(data)
        dirtyTokens = [tokenizer.tokenize(component) for component in components]
        tokens = []
        # Flatten the list and filter out empty tokens, include single tokens and clean up larger tokens
        for token in dirtyTokens:
            if isinstance(token, list):
                if len(token) == 1:
                    tokens.append(token[0])
                else:
                    tokenParsed = [t.strip() for t in token]
                    finalToken = ""
                    # Clean up the token by removing non-alphanumeric characters, concatenate letters and digits
                    for t in tokenParsed:
                        for letter in t:
                            if letter.isalpha() or letter.isdigit() or letter in ['-']:
                                finalToken += str(letter)
                    tokens.append(str(finalToken))

        # if self.alphaOrNum:
        if alphaOrNum == 1:
            # Convert tokens to alphabetical tokens
            tokens = [token for token in tokens if token.isalpha()]
        elif alphaOrNum == 2:
            # Convert tokens to numerical tokens
            tokens = [float(token) for token in tokens if token.lstrip('-').isdigit()]
        return tokens

    @staticmethod
    def mean(data):
        """Calculate the mean of a list of numbers."""
        if not data:
            return 0
        return sum(data) / len(data)

    @staticmethod
    def stemLeafToList(stem_leaf_str):
        """
        Convert a stem-and-leaf plot string to a list of numbers.
        Example input:
          5 | 8
          6 | 2 5 7 8
          7 | 1 4 5 8
          8 | 1 4 8
          9 | 1 5 9
        """
        data = []
        for line in stem_leaf_str.strip().splitlines():
            if "|" not in line:
                continue
            stem_part, leaf_part = line.split("|", 1)
            stem = stem_part.strip()
            leaves = leaf_part.strip().split()
            for leaf in leaves:
                if stem and leaf.isdigit():
                    data.append(int(stem + leaf))
        return data

    @staticmethod
    def median(data):
        """Calculate the median of a list of numbers."""
        if not data:
            return 0
        sorted_data = sorted(data)
        n = len(sorted_data)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_data[mid - 1] + sorted_data[mid]) / 2
        else:
            return sorted_data[mid]

    @staticmethod
    def populationStandardDeviation(data):
        """Calculate the standard deviation of a list of numbers with population."""
        if not data:
            return 0
        meanValue = StatisticsHelper.mean(data)
        populationVariance = sum((i - meanValue) ** 2 for i in data) / len(data)
        return math.sqrt(populationVariance)

    @staticmethod
    def sampleStandardDeviation(data):
        """Calculate the standard deviation of a list of numbers with sample."""
        if not data:
            return 0
        meanValue = StatisticsHelper.mean(data)
        sampleVariance = sum((i - meanValue) ** 2 for i in data) / (len(data) - 1)
        return math.sqrt(sampleVariance)

    @staticmethod
    def range(data):
        """Calculate the range of a list of numbers."""
        if not data:
            return 0
        return max(data) - min(data)

    @staticmethod
    def mode(data):
        """Calculate the mode of a list of numbers."""
        if not data:
            return None
        frequency = {}
        for number in data:
            frequency[number] = frequency.get(number, 0) + 1
        max_freq = max(frequency.values())
        modes = [num for num, freq in frequency.items() if freq == max_freq]
        return modes if len(modes) > 1 else modes[0]

    @staticmethod
    def datasetToList(dataset, delimiter=","):
        """Convert a dataset string to a list of numbers."""
        if not isinstance(dataset, str):
            if isinstance(dataset, list):
                return dataset
            raise ValueError("Dataset must be a string.")
        return [int(i) for i in dataset.split(delimiter)]

    @staticmethod 
    def findQuartiles(dataset):
        """Calculate the first, second, third, and fourth quartiles of a dataset."""
        if not dataset:
            return None, None
        sorted_data = sorted(dataset)
        n = len(sorted_data)
        q2 = StatisticsHelper.median(sorted_data)
        if n % 2 == 0:
            lower_half = sorted_data[: n // 2]
            upper_half = sorted_data[n // 2 :]
        else:
            lower_half = sorted_data[: n // 2]
            upper_half = sorted_data[n // 2 + 1 :]
        q1 = StatisticsHelper.median(lower_half)
        q3 = StatisticsHelper.median(upper_half)
        q4 = sorted_data[-1]

        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = [x for x in sorted_data if x < lower_bound or x > upper_bound]
        return q1, q2, q3, q4, iqr, lower_bound, upper_bound, outliers
    

    @staticmethod #manipulate to work with float data
    def frequencyDistribution(data, lowest_class_limit, class_width):
        """Print a formatted frequency distribution table (supports int and float data)."""
        if not data:
            print("No data provided.")
            return

        min_value = float(lowest_class_limit)
        max_value = max(data)
        # Calculate number of classes needed
        num_classes = int(math.ceil((max_value - min_value) / class_width))

        # Build class intervals
        intervals = []
        for i in range(num_classes):
            lower = min_value + (i * class_width)
            upper = lower + class_width
            intervals.append((lower, upper))
        # If the last interval does not cover the max value, extend it
        if intervals[-1][1] < max_value:
            intervals[-1] = (intervals[-1][0], max_value)

        # Count frequencies
        freq = [0] * num_classes
        for value in data:
            for idx, (lower, upper) in enumerate(intervals):
                # For the last interval, include the upper bound
                if idx == num_classes - 1:
                    if lower <= value <= upper:
                        freq[idx] += 1
                        break
                else:
                    if lower <= value < upper:
                        freq[idx] += 1
                        break

        # Print table
        print(f"{'Class Interval':<25}{'Frequency':<10}")
        print("-" * 35)
        for (lower, upper), f in zip(intervals, freq):
            interval_str = f"{lower:.2f} - {upper:.2f}"
            print(f"{interval_str:<25}{f:<10}")


