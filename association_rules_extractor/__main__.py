import sys
import time

from association_rules_extractor import helpers
from association_rules_extractor import a_priori
from association_rules_extractor import select_confidence


def main():

    t = time.time()
    
    if len(sys.argv) < 4:
        print('Use: python -m association_rules_extractor <filename> <min_sup> <min_conf>')
        return

    filename = sys.argv[1]

    try:
        min_sup, min_conf = float(sys.argv[2]), float(sys.argv[3])
        if min_sup < 0 or min_sup > 1 or min_conf < 0 or min_conf > 1:
            raise Exception

    except Exception as e:
        print('<min_sup> and <min_conf> must be a floats between 0 and 1 !')
        print(e)
        return

    transactions = helpers.load_csv(filename)

    large_itemsets, supports = a_priori.a_priori(transactions, min_support=min_sup)
    helpers.print_large_itemsets(large_itemsets, supports)
    helpers.save_large_itemsets(large_itemsets, supports)
    
    selected_rules = select_confidence.select_high_conf_rules(large_itemsets, supports, min_conf)
    helpers.print_rules(selected_rules)
    helpers.save_rules(selected_rules)

    print('Done in ', time.time() - t)
    
if __name__ == '__main__':
    main()
