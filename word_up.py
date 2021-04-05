#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import typing
from typing import Dict, Tuple, List

def build_matrix(rows: int, cols: int) -> List[List[str]]:
    """Build empty matrix."""
    matrix: List[List[str]] = []
    for i in range(rows):
        matrix.append([])
        for _j in range(cols):
            matrix[i].append("")
    return matrix


def search(
    matrix: List[List[str]],
    word: str,
    initial_position: Tuple[int, int],
    dictionary: Dict[str, List[int]],
    direction: str = "None",
) -> Tuple[int, int]:
    """
    Find the end position of the given word.

    By determining a direction, we know the word will not change direction so
    we check each letter of word with the next position in the matrix that
    corresponds with our direction. It continues this process until the length
    of the word we are checking is zero, that is the base case. At that point,
    we know the final position is the final initial position tuple we passed in
    the function so we return it.
    """
    possible_directions: List[str] = []
    tuples: List[typing.Tuple[int, int]] = []
    # Base case that returns the final position of the word
    if len(word) == 0:
        return initial_position

    if direction == "None":
        for key, lists in dictionary.items():
            tuple_pos = (
                initial_position[0] + lists[0],
                initial_position[1] + lists[1],
            )

            """
            Try statment handles Index error when
            tuple_pos + initial_position is out of the index of matrix.
            """
            try:
                if (
                    (tuple_pos[1] >= 0)
                    and (tuple_pos[0] >= 0)
                    and (matrix[tuple_pos[0]][tuple_pos[1]] == word[0])
                ):
                    possible_directions.append(key)
                    tuples.append(tuple_pos)
            except IndexError:
                continue

    if direction != "None":
        tuple_pos = (
            initial_position[0] + dictionary[direction][0],
            initial_position[1] + dictionary[direction][1],
        )
        """
        Essentially the same as the last try function but this one only
        tries in one direction.
        """
        try:
            # Checks if next letter in direction == first letter of word
            if (
                (tuple_pos[1] >= 0)
                and (tuple_pos[0] >= 0)
                and matrix[tuple_pos[0]][tuple_pos[1]] == word[0]
            ):
                return search(matrix, word[1:], tuple_pos, dictionary, direction)
            else:
                return (-1, -1)
        except IndexError:
            return (-1, -1)
    # Checks each possibility of the given starting position.
    for i in range(len(possible_directions)):
        final_position = search(
            matrix, word[1:], tuples[i], dictionary, possible_directions[i]
        )
        if (final_position is not None) and (final_position[0]) >= 0:
            return final_position
    # Don't like this but had to for type-checking
    return (-1, -1)


def matrix_search(
    matrix: List[List[str]], word: str
) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Search through given matrix and return starting and ending position."""
    # Tells the program directions based of a 2-D array
    direction_dictionary = {
        "North": [-1, 0],
        "Northeast": [-1, 1],
        "East": [0, 1],
        "Southeast": [1, 1],
        "South": [1, 0],
        "Southwest": [1, -1],
        "West": [0, -1],
        "Northwest": [-1, -1],
    }
    # Searches through entire matrix for first letter of the word
    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            if word[0] == matrix[row][column]:
                initial_position = (row, column)
                # Calls the search function to find the final position
                final_position = search(
                    matrix, word[1:], initial_position, direction_dictionary
                )
                """
                Check to see if final_position is valid and is the last letter
                of the word
                """
                if (final_position is not None) and (
                    matrix[final_position[0]][final_position[1]] == word[-1]
                    and (final_position[0] >= 0)
                ):
                    return initial_position, final_position
    # Don't like this but had to do so for type-checking
    return ((-1, -1), (-1, -1))


def main() -> None:
    """Get user input and find a pattern in any given matrix."""
    locations: List[typing.Tuple[typing.Tuple[int, int], typing.Tuple[int, int]]] = []
    words: List[str] = []
    user_iterations: int = int(input())
    # Get user input for every matrix they want to use
    for it in range(user_iterations):
        input()
        user_input_list: List[str] = input().split()
        user_rows: int = int(user_input_list[0])
        user_cols: int = int(user_input_list[1])

        matrix: List[List[str]] = build_matrix(user_rows, user_cols)

        # Fills the empty matrix with user-defined symbols
        for i in range(user_rows):
            user_letter_list: List[str] = input().split()
            for j in range(len(user_letter_list)):
                matrix[i][j] = user_letter_list[j]

        user_word: str = input()
        words.append(user_word)
        locations.append(matrix_search(matrix, user_word))

    # Prints results of each test and determines if word was found
    for i in range(len(locations)):
        print('Searching for "{}" in matrix {} yields:'.format(words[i], i))
        if (locations[i] is None) or (locations[i][1][0] < 0):
            print("The pattern was not found.")
            print()
        else:
            print(
                "Start pos: {} to End pos: {}".format(locations[i][0], locations[i][1])
            )
            print()


if __name__ == "__main__":
    main()
