from functools import reduce
import pprint

def generate_candidates(itemset, L_k):
    candidates_k = []
    for l in L_k:
        for i in itemset.difference(l):
            if l.union(set([i])) not in candidates_k: # avoid duplicates
                candidates_k.append(l.union(set([i])))
    return candidates_k

def generate_candidates_enhanced(itemset, L_k):
    # idée: prendre tous les sets de taille k réalisables avec L_k
    # puis pruner ceux qui ont un subset de taille k-1 qui n'est pas dans L_k
    
    if L_k == [set()]: # case k = 1
        return [set([elmt]) for elmt in itemset]
    
    candidates_k = []
    for t in L_k:
        for q in L_k:
            for elmt in q:
                if not set(q).issubset(t): # avoid duplicates inside this new set of size k
                    new_set = set(q).union(t)
                    if not new_set in candidates_k: # avoid adding a new set already generated
                        candidates_k.append(new_set)

    for c in candidates_k:
        subsets = [c.difference([elmt]) for elmt in c] # get all subsets of size k-1
        if any(s not in L_k for s in subsets):
            candidates_k.remove(c)

    return candidates_k

def compute_supports(transactions, candidates):
    print('Scanning transactions to compute supports...'
          + '(%s transactions to scan, %s candidates)' % (len(transactions), len(candidates)))
    candidates_supports = {frozenset(c): 0 for c in candidates}
    for idx, transaction in enumerate(transactions):
        if int(100*idx/len(transactions)) % 10 == 0 and int(100*(idx-1)/len(transactions)) % 10 != 0:
            print(str(int(100*idx/len(transactions))) + ' % done')
        for c in candidates:
            if c.issubset(transaction):
                candidates_supports[frozenset(c)] += 1
    print('Scanning done, supports computed')
    return {c: candidates_supports[c]/len(transactions) for c in candidates_supports}

def a_priori(transactions, min_support, generate_candidates=generate_candidates_enhanced):

    print('========== RUNNING A PRIORI ===========\n')

    itemset = reduce(lambda x, y: x.union(y), transactions)
    large_itemsets = set()
    L_k = [set()]
    supports = dict() # structure: {frozenset(1,2,3): support, ...}
    k = 0

    while L_k != []:
        k += 1
        
        # generate candidates:
        candidates_k = generate_candidates(itemset, L_k)
        
        # scan once to compute supports of candidates:
        candidates_supports = compute_supports(transactions, candidates_k)
                
        # filter candidates based on support:
        L_k = [frozenset(c) for c in candidates_k if candidates_supports[frozenset(c)] >= min_support]
        large_itemsets = large_itemsets.union(L_k)
        supports.update(candidates_supports) # TODO: update only the candidates filtered ? to gain memory
        
        # print('Large itemsets of size ', k, ' : \n', pprint.pformat(L_k))
        print('Selected %s large itemsets of size %s' % (len(L_k), k))
    
    print('\n=========== A PRIORI DONE =============\n\n')
    
    return large_itemsets, supports