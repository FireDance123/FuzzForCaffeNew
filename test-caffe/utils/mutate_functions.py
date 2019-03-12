def mutate_for_li(li, target_mutation_function):
    for i in range(len(li)):
        for j in range(len(li[0])):
            for k in range(len(li[0][0])):
                li[i][j][k] = target_mutation_function(li[i][j][k])
    return li

def mutate_erase(data):
    pass

def mutate_insert(data):
    pass


