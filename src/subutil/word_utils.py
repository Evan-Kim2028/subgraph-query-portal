def levenshtein_distance(s1: list[str], s2: list[str]) -> int:
    """
    Compute the Levenshtein distance between two lists of strings. The Levenshtein distance
    is used to measure the similarity between words.

    Args:
        s1: The first list of strings.
        s2: The second list of strings.

    Returns:
        The Levenshtein distance between s1 and s2.
    """
    # Create a matrix to store the distances
    m = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]

    # Initialize the first row and column
    for i in range(len(s1) + 1):
        m[i][0] = i
    for j in range(len(s2) + 1):
        m[0][j] = j

    # Fill in the rest of the matrix
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            if s1[i - 1] == s2[j - 1]:
                cost = 0
            else:
                cost = 1
            m[i][j] = min(m[i - 1][j] + 1, m[i][j - 1] + 1, m[i - 1][j - 1] + cost)

    # Return the distance
    return m[-1][-1]

def make_levenshtein_dict(query_entity_list: list[str], schema_entity_list: list[str]) -> dict:
    """
    Returns a dictionary that maps each word in query_entity_list to its closest matching word in schema_entity_list
    using the Levenshtein distance.

    Args:
        query_entity_list (list[str]): The list of words to find matches for.
        schema_entity_list (list[str]): The list of words to find matches in.

    Returns:
        dict: A dictionary that maps each word in query_entity_list to its closest matching word in schema_entity_list.
    """
    # create an empty dictionary to store the matches
    matches = {}

    # create a set of unique words from schema_entity_list
    schema_entity_list_set = set(schema_entity_list)

    # loop through the words in query_entity_list
    for word1 in query_entity_list:
        # find the closest match in schema_entity_list using the Levenshtein distance
        best_distance = float('inf')
        best_match = None
        for word2 in schema_entity_list_set:
            distance = levenshtein_distance(word1.lower(), word2.lower())
            if distance < best_distance:
                best_distance = distance
                best_match = word2

        # remove the best match from the set to avoid using it again
        schema_entity_list_set.discard(best_match)

        # add the match to the dictionary
        matches[word1] = best_match

    # return the dictionary
    return matches

