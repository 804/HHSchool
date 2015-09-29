# -*- coding: utf-8 -*-
"""
Created on 25.09.15

:author: 804

Script for submitting expressions containing brackets,
one variable, the operations of addition, subtraction,
multiplication, and constant degree in expanded form.

Example.
Input:
(x - 6x^2)(((3 + 6x)(x + 3) - 4x^9000)x - 3)

Output:
24x^9003 - 4x^9002 - 36x^5 - 120x^4 - 33x^3 + 27x^2 - 3x
"""
import math
import sys


def add_operand_in_stack(operand, reverse_polish_notation, operand_stack):
    """ Adding operand at stack and pushing it out to the output
    operands from the stack while there will be nothing left, or until
    on the top of the stack will be '(', or until the top of the stack
    will not lie operand with higher priority

    :param operand: added operand
    :type operand: <type 'str'>
    :param reverse_polish_notation: output in the form of reverse Polish notation
    :type reverse_polish_notation: <type 'list'>
    :param operand_stack: stack's current statement
    :type operand_stack: <type 'list'>
    """
    priority = ('+', '-', '*', '^')
    while operand_stack and (operand_stack[len(operand_stack) - 1] != '(') and (
                priority.index(operand_stack[len(operand_stack) - 1]) > priority.index(operand)):
        reverse_polish_notation.append(operand_stack.pop())
    operand_stack.append(operand)


def string_simple_monomial_to_dictionary(monomial):
    """ The function to convert the simple monomial's string
    record in a convenient for computing dictionary-form

    :param monomial: converted monomial
    :type monomial: <type 'str'>
    :return: monomial in dictionary-form
    :rtype: <type 'dict'>
    """
    if monomial[0] == 'x':
        return {1: 1}
    else:
        return {0: int(monomial)}


def dictionary_polinomial_to_string(polinomial):
    """ The function to convert the polinomial's dictionary-form
    in a string record

    :param polinomial: converted polinomial
    :type polinomial: <type 'dict'>
    :return: polinomial in string record
    :rtype: <type 'str'>
    """
    result = []
    for key in sorted(polinomial.keys(), reverse=True):
        if polinomial[key] > 0:
            if key == 1:
                result.append(' + ' + str(polinomial[key]) + 'x')
            elif key == 0:
                result.append(' + ' + str(polinomial[key]))
            else:
                result.append(' + ' + str(polinomial[key]) + 'x^' + str(key))
        else:
            if key == 1:
                result.append(' - ' + str(int(math.fabs(polinomial[key]))) + 'x')
            elif key == 0:
                result.append(' - ' + str(int(math.fabs(polinomial[key]))))
            else:
                result.append(' - ' + str(int(math.fabs(polinomial[key]))) + 'x^' + str(key))
    return ''.join(result)[3:]


def addition_polinomials(first, second):
    """ The function to addition of polinomials in dictionary-form

    :param first: added polinomial
    :type first: <type 'dict'>
    :param second: added polinomial
    :type second: <type 'dict'>
    :return: result of addition
    :rtype: <type 'dict'>
    """
    first_keys = first.keys()
    for key in second.keys():
        if key in first_keys:
            first[key] += second[key]
        else:
            first[key] = second[key]
    return first


def subtraction_polinomials(first, second):
    """ The function to subtraction of polinomials in dictionary-form

    :param first: shrinkable polinomial
    :type first: <type 'dict'>
    :param second: deducted polinomial
    :type second: <type 'dict'>
    :return: result of subtraction
    :rtype: <type 'dict'>
    """
    first_keys = first.keys()
    for key in second.keys():
        if key in first_keys:
            first[key] -= second[key]
        else:
            first[key] = -second[key]
    return first


def multiple_on_monomial(polinomial, coefficient, degree):
    """ The function to multiple polinomial on monomial in dictionary-form

    :param polinomial: multiplied polinomial
    :type polinomial: <type 'dict'>
    :param coefficient: multiplied monomial's coefficient
    :type coefficient: <type 'int'>
    :param degree: multiplied monomial's degree
    :type degree: <type 'int'>
    :return: result of multiple
    :rtype: <type 'dict'>
    """
    result = {}
    for key in polinomial.keys():
        result[key + degree] = coefficient * polinomial[key]
    return result


def multiple_polinomials(first, second):
    """ The function to multiple of polinomials in dictionary-form

    :param first: multiplied polinomial
    :type first: <type 'dict'>
    :param second: multiplied polinomial
    :type second: <type 'dict'>
    :return: result of multiple
    :rtype: <type 'dict'>
    """
    result = {}
    for key in second.keys():
        result = addition_polinomials(multiple_on_monomial(first, second[key], key), result)
    return result


def constant_degree(polinomial, degree):
    """ The function for involution of polinomial in constant degree

    :param polinomial: multiplied polinomial
    :type polinomial: <type 'dict'>
    :param degree: constant degree
    :return: result of multiple
    :rtype: <type 'dict'>
    """
    result = {0: 1}
    for i in xrange(degree):
        result = multiple_polinomials(result, polinomial)
    return result


def expression_is_correct(expression):
    """ The function checks the validity of the input expression

    :param expression: multiplied polinomial
    :type expression: <type 'str'>
    :return: expression is correct or not
    :rtype: <type 'bool'>
    """
    brackets = 0
    for char_index in xrange(len(expression)):
        if (expression[char_index] in ('+', '-', '*', '^', '(')) and (
                    (char_index + 1 == len(expression)) or (
                            expression[char_index + 1] in ('+', '-', '*', '^', ')'))):
            return False
        if (expression[char_index] == '^') and (expression[char_index + 1] == 'x'):
            return False
        brackets += 1 if expression[char_index] == '(' else -1 if expression[char_index] == ')' else 0
        if brackets < 0:
            return False
    return True


def make_reverse_polish_notation(expression):
    """ The function to make reverse polish notation
    form from input expression

    :param expression: input expression
    :type expression: <type 'str'>
    :return: reverse polish notation form
    :rtype: <type 'list'>
    """
    position = 0
    numbers = [chr(item) for item in xrange(48, 58)]
    reverse_polish_notation = []
    operand_stack = []
    while position < len(expression):
        if (position != 0) and (expression[position - 1] == ')'):
            if expression[position] in (numbers + ['x', '(']):
                add_operand_in_stack('*', reverse_polish_notation, operand_stack)
        if (position != 0) and (expression[position] in ('x', '(')):
            if expression[position - 1] in (numbers + ['x']):
                add_operand_in_stack('*', reverse_polish_notation, operand_stack)

        if expression[position] == '(':
            operand_stack.append('(')
            position += 1
        elif expression[position] == ')':
            while operand_stack[len(operand_stack) - 1] != '(':
                reverse_polish_notation.append(operand_stack.pop())
            operand_stack.pop()
            position += 1
        elif expression[position] in ('+', '-', '*', '^'):
            add_operand_in_stack(expression[position], reverse_polish_notation, operand_stack)
            position += 1
        else:
            limits = [expression[position + 1:].index(char) for char in ('+', '-', ')', '(', '*', '^', 'x') if
                      char in expression[position + 1:]]
            if limits:
                reverse_polish_notation.append(expression[position:position + min(limits) + 1])
                position += min(limits) + 1
            else:
                reverse_polish_notation.append(expression[position:])
                position = len(expression)
    while operand_stack:
        reverse_polish_notation.append(operand_stack.pop())
    return reverse_polish_notation


def calculate(reverse_polish_notation):
    """ Calculate expression in the form of reverse polish notation

    :param reverse_polish_notation: reverse polish notation form of expression
    :type reverse_polish_notation: <type 'list'>

    :raise: Exception
    """
    position = 0
    while position < len(reverse_polish_notation):
        if reverse_polish_notation[position] == '+':
            reverse_polish_notation[position - 2:position + 1] = [
                addition_polinomials(reverse_polish_notation[position - 2], reverse_polish_notation[position - 1])]
            position -= 1
            continue
        elif reverse_polish_notation[position] == '-':
            reverse_polish_notation[position - 2:position + 1] = [
                subtraction_polinomials(reverse_polish_notation[position - 2], reverse_polish_notation[position - 1])]
            position -= 1
            continue
        elif reverse_polish_notation[position] == '*':
            reverse_polish_notation[position - 2:position + 1] = [
                multiple_polinomials(reverse_polish_notation[position - 2], reverse_polish_notation[position - 1])]
            position -= 1
            continue
        elif reverse_polish_notation[position] == '^':
            try:
                if reverse_polish_notation[position - 1].keys() != [0]:
                    raise Exception('Input error', 'Incorrect degree for involution')
            except Exception as exception:
                print "%s: %s" % (exception[0], exception[1])
                sys.exit(0)
            reverse_polish_notation[position - 2:position + 1] = [
                constant_degree(reverse_polish_notation[position - 2], reverse_polish_notation[position - 1][0])]
            position -= 1
            continue
        position += 1


def main():
    expression = raw_input("\nInput expression:\n").replace(' ', '').lower()
    try:
        if not expression_is_correct(expression):
            raise Exception('Input error', 'Input expression is not correct')
    except Exception as exception:
        print '%s: %s' % (exception[0], exception[1])
        sys.exit(0)
    reverse_polish_notation = make_reverse_polish_notation(expression)
    reverse_polish_notation = [string_simple_monomial_to_dictionary(string) if string not in ('+', '-', '*', '^') else string for
                               string in reverse_polish_notation]
    calculate(reverse_polish_notation)
    print '\nResult:\n%s' % dictionary_polinomial_to_string(reverse_polish_notation[0])


if __name__ == '__main__':
    main()
