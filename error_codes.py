class Error:
  GET_PARAGRAPH_FAILED = "Could not fetch data from metaphorpsum.com, please try again later"
  INVALID_SEARCH_OPERATOR = "Query parameter 'op' values can be on of 'in' or 'and'"
  INVALID_SEARCH_QUERY = "Query parameter 'q' should be comma separated string. e.g q=word1,word2,word3"
