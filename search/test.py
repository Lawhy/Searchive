from search_mongo_pos import mode_select

search_query = "constant spacetime mean curvature surfaces"
mode = 'general'  # mode = 'abstract' / 'title' / 'author'/ 'param'
search_phrase = "\"constant spacetime mean curvature surfaces\""
print(mode_select(search_query, 'general').__len__())  # result:search time 0.12  # 138445
print(mode_select(search_phrase, 'general'))  # result:search time 0.11