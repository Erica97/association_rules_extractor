

def select_high_conf_rules(large_itemsets, supports, min_conf):

    print('========== RUNNING CONF SELECTION ===========\n')

    selected_rules = []
    for l in large_itemsets:
        # splits = find_subsets(l)
        if len(l) > 1:
            splits = [(l.difference([elmt]), set([elmt])) for elmt in l] # find splits of size (size(l) - 1)*1
            for (lhs, rhs) in splits:
                support = supports[l]
                confidence = support/supports[lhs]
                if confidence >= min_conf:
                    selected_rules.append((lhs, rhs, confidence, support))
    
    print('========== CONF SELECTION DONE =========== \n\n')

    return selected_rules