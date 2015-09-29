# -*- coding: utf-8 -*-
"""
Created on 27.09.15

:author: 804

The script for the determination of the first occurrence of input
sequences into an infinite sequence formed by gluing consecutive
positive integers: S = 123456789101112131415...

Example.
Input:
6789

Output:
6
"""
import sys


def sequence_position(number):
    """ Function for calculating position of number
    in an infinite sequence formed by gluing consecutive
    positive integers

    :param number: input number
    :type number: <type 'int'>
    :return: position of number in infinite sequence
    :rtype: <type 'int'>
    """
    digit = 1
    sign_in_number = 1
    position = 0
    while number // (digit * 10) > 0:
        position += sign_in_number * (digit * 10 - digit)
        digit *= 10
        sign_in_number += 1
    position += sign_in_number * (number - digit) + 1
    return position


def bearing_element(subsequence, offset, length):
    """ Function for finding subsequence's bearing element with
    input offset and length
    (first element whose beginning lies in a given subsequence

    :param subsequence: input subsequence
    :type subsequence: <type 'str'>
    :param offset: input offset
    :type offset: <type 'int'>
    :param length: input length of element
    :type length: <type 'int'>
    :return: bearing element or None if element not found
    :rtype: <type 'int'>, <type 'NoneType'>
    """
    if length + offset > len(subsequence):
        if subsequence[offset] == '0':
            return None
        element = [None] * length
        end = str(int(subsequence[:offset]) + 1).zfill(offset)
        for i in xrange(len(subsequence) - offset):
            element[i] = subsequence[i + offset]
        for i in xrange(len(end)):
            if element[len(element) - 1 - i] is None:
                element[len(element) - 1 - i] = end[len(end) - 1 - i]
            else:
                if end[len(end) - 1 - i] != element[len(element) - 1 - i]:
                    return None
        element = ['0' if element[i] is None else element[i] for i in xrange(len(element))]
        return int(''.join(element))
    else:
        if subsequence[offset] == '0':
            return None
        element = int(subsequence[offset:offset + length])
        if (offset != 0) and (subsequence[:offset] != str(element - 1)[len(str(element - 1)) - offset:]):
            return None
        position = offset + length
        increment = 1
        while position + len(str(element + increment)) < len(subsequence):
            if int(subsequence[position:position + len(str(element + increment))]) != element + increment:
                return None
            position += len(str(element + increment))
            increment += 1
        if (position == len(subsequence)) or (
                    subsequence[position:] == str(element + increment)[:len(subsequence) - position]):
            return element
        else:
            return None


def get_min_position(subsequence):
    """ Function for calculating position of subsequence
    into an infinite sequence formed by gluing consecutive
    positive integers

    :param subsequence: input subsequence
    :type subsequence: <type 'str'>
    :return: minimal position of given subsequence
    :rtype: <type 'int'>
    """
    try:
        if int(subsequence) == 0:
            print sequence_position(10 ** len(subsequence)) + 1
            sys.exit(0)
    except ValueError:
        print 'Incorrect input sequence. It most be a string of digits.'
        sys.exit(0)
    min_position = -1
    for length in xrange(1, len(subsequence) + 1):
        for offset in xrange(length):
            element = bearing_element(subsequence, offset, length)
            if element is not None:
                if (min_position == -1) or (
                                sequence_position(element) + offset < min_position):
                    min_position = sequence_position(element) - offset
    return min_position


def main():
    subsequence = raw_input('\nInput sequence:\n')
    print '\nResult:\n%s' % get_min_position(subsequence)


if __name__ == '__main__':
    main()
