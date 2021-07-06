"""suffix_trie.py: This module demonstrates an exemplative code of suffix trie using a node class and
                   a OrfFinder class which uses the suffix trie structure to store data.
    Neither python dictionaries or sets are used in this module.
    Complexities mentioned in this file is of Worst Time unless otherwise specified."""

class GenomeNode:
    """
    This class represents a node of Tries.
    """

    def __init__(self, level=None, size=5):
        # data[0] is a list which stores the indices in the original string of the added chars.
        # data[1] stores the char value.
        self.data = []
        self.links = [None] * size
        self.level = level


class OrfFinder:
    def __init__(self, genome):
        """
        This function will appropriately store the suffixes of the given genome into `OrfFinder` class instance
        by calling `insert()` function.
        :param:
            - `genome`: A single non-empty string consisting only of uppercase [A-D].
                      genome is passed as an argument to the __init__ method of OrfFinder.
        :time complexity:
            - O(N^2) time, where N == len(genome):
                Creating lists of suffixes/prefixes of genome string costs O(N^2) * 2,
                Calling insert() with for loops costs O(N) * 2,
                and each insert() execution costs O(N).
        """
        self.genome = genome
        # Create a Suffix Trie to find the prefix matching of `start`
        self.root1 = GenomeNode(level=0)
        current = self.root1
        level_count = current.level
        genome_lst = []
        for i in range(len(genome)):
            genome_lst.append(genome[i:])
        lst = []
        for i in range(len(genome)):
            lst.append(self.insert(current, genome_lst[i], level_count, i, genome))

        # Create a Suffix Trie to find the suffix matching of `end` using the reversed version of `genome`.
        self.root2 = GenomeNode(level=0)
        current = self.root2
        level_count = current.level
        reversed_genome = genome[::-1]
        reversed_genome_lst = []
        reversed_lst = []
        for i in range(len(reversed_genome)):
            reversed_genome_lst.append(reversed_genome[i:])
        for i in range(len(reversed_genome)):
            reversed_lst.append(self.insert(current, reversed_genome_lst[i], level_count, i, reversed_genome))

    def insert(self, current, g, level_count, i, original_genome):
        """
        This function recursively adds the given genome to this class.
        current.data[0] saves the indices in the original string of the added char

        :param:
            - `current`: The current root node during the recursion.
            - `g`: A string to be added at the given node.
            - `level_count`: A number counting the height of the root node.
            - `i`: Positional index of g in the caller list, and used to get the index within the original string
                of the char to be stored.
            - `original_genome`: The full string to be added by one insert call.
        :time complexity:
            - O(len(s)): The recursion depth is len(s) and adding appropriate information takes O(1) time.
        """
        level_count += 1

        # Base case: reached the terminal
        if level_count == len(g) + 1:
            # Go through the terminal $, where index = 0
            index = 0
            if current.links[index] is not None:
                current = current.links[index]
            else:
                current.links[index] = GenomeNode(level=level_count)
                current = current.links[index]
            # Add data to the payload
            # level_count-1+i represents the position of the char in the original string.
            current.data.append(level_count - 1 + i)

        # Recursive Part
        else:
            # convert ASCII to index
            # $ = 0, a = 1, b = 2 ...
            char = g[level_count - 1]
            index = ord(char) - 65 + 1

            # If the path exists
            if current.links[index] is not None:
                current = current.links[index]
            # If the path doesn't exist
            else:
                # Create a new Node
                current.links[index] = GenomeNode(level=level_count)
                current = current.links[index]
            self.insert(current, g, level_count, i, original_genome)
            current.data.append(level_count - 1 + i)

    def find(self, start, end):
        """
        :param:
            - `start`: A single non-empty string consisting of only uppercase [A-D].
            - `end`: A single non-empty string consisting of only uppercase [A-D].
        :return:
            - a list: A list of strings, which contains all the substrings of genome
                      which have start as prefix and end as a suffix.
                      The order of these strings does not matter.
                      start and end must not overlap in the substring.
        :time complexity:
            - (len(start)+len(end)+U) time, where finding prefix/suffix matching by calling find_aux()
            costs len(start)/len(end)
                and U == number of characters in the output list.
        """
        res = []
        current = self.root1
        genome = self.genome
        level_count = current.level
        try:
            matching_prefixes = self.find_aux(current, start, level_count)
        except Exception:
            return []

        current = self.root2
        level_count = current.level
        reversed_end = end[::-1]
        try:
            matching_suffixes = self.find_aux(current, reversed_end, level_count)
        except Exception:
            return []

        """Get the output"""
        # max(end_indices) needs to be greater than max(start_indices), otherwise there's no valid output.
        # Time Complexity: O(U) where U is 1
        min_prefix_index = matching_prefixes[0] - len(start) + 1
        max_suffix_index = len(genome) - matching_suffixes[0] - 1 + len(end)
        if max_suffix_index <= min_prefix_index:
            return []

        # Time Complexity: O(U) where U is the number of characters in the output list.
        for index1 in matching_prefixes:
            # Get the index of the beginning of prefix from index1 in matching_prefixes
            start_index = index1 - len(start) + 1
            for index2 in matching_suffixes:
                # Get the index indicating the end of the suffix from index2 in matching_suffixes
                end_index = len(genome) - index2 - 1 + len(end)
                # exclude overlapping or invalid index combinations
                # As the 2 lists are sorted, if there's any inappropriate value somewhere inside this loop,
                # it can immediately move to the next iteration of the outer loop.
                if end_index > start_index and len(start) + len(end) <= end_index - start_index:
                    res.append(genome[start_index:end_index])
                else:
                    break
        return res

    def find_aux(self, current, key, level_count):
        """
        :param
            - `current`: The current root node during the recursion.
            - `key`: A string to be searched for matching prefixes or suffixes.
            - `level_count`: A number counting the height of the root node.
        :return: current.data at the base case, else return its recursive call.
        :time complexity: O(len(key)) as the recursion depth is the len(key) + 1.
        """
        level_count += 1
        # Base case: reached the terminal
        if level_count == len(key) + 1:
            return current.data

        # Recursive Part
        else:
            # convert ASCII to index
            # $ = 0, a = 1, b = 2 ...
            char = key[level_count - 1]
            index = ord(char) - 65 + 1
            # If the path exists
            if current.links[index] is not None:
                current = current.links[index]
                return self.find_aux(current, key, level_count)

            # If the path doesn't exist
            else:
                raise Exception(str(key) + " doesn't exist")