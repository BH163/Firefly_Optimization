def firefly_algorithm(objective_function, num_of_generations, domain, dimensions = 10, population_size = 10, alpha = 1, beta = 1, gamma = .01, move_restriction = False):
    # initialize population
    ## additional dimension (dimension + 1) stores objective function value
    population = np.random.uniform(low = domain[0], high = domain[1], size = (population_size, dimensions + 1))


    # calculate inital firefly brightness
    for firefly in population:
        objective_function_value = objective_function(firefly[:-1])
        # store objective function value
        firefly[-1] = objective_function_value




    t = 0
    best_firefly_value = 100000000

    while t < num_of_generations:
        for i in range(population_size):
            for j in range(population_size):

                # compare objective function values (BRIGHTNESS)
                ## note that lower brightness (lower objective function value) is actually associated with better result as we are minimizing
                if population[j][-1] < population[i][-1]:

                    # find distance between fireflies
                    summ = 0
                    for dim in range(dimensions-1) :
                        summ += (population[i][dim] - population[j][dim])**2
                    distance = np.sqrt(summ)


                    # store firefly values before movement (in case of move restriction approach used)
                    firefly_i = population[i]


                    # calculate next position
                    epsilon = np.random.normal(1)
                    for dim in range(dimensions - 1):
                        population[i][dim] = population[i][dim] + (beta * np.exp(-gamma * distance) * (population[j][dim] - population[i][dim])) + (alpha * epsilon)
                    # calcuate new objective function value
                    population[i][-1] = objective_function(population[i][:-1])

                    # move restriction (do not move firefly unless result is better)
                    if move_restriction == True:
                        if population[i][-1] > firefly_i[-1]:
                            population[i] = firefly_i
                  

            
        # test if we have a lower best_firefly_value now
        for firefly in population:
            if firefly[-1] < best_firefly_value:
                best_firefly_value = firefly[-1]


        
        t += 1


    return(best_firefly_value)


    

        
    

    
    


if __name__ == "__main__":
    import numpy as np

    ######################################################################################################
    ## DEFINE FUNCTIONS ##



    # reference Bird Mating Optimizer paper for mathematic representation of functions
    composed_modal_function_set = []

    ##UNIMODALS FUNCTIONS -->
    unimodal_function_set = []


    # f1
    domain_f1 =  [-100,100]
    min_f1 = 0
    f1 = lambda x : sum([i**2 for i in x ])
    unimodal_function_set.append([domain_f1, min_f1, f1,'f1'])


    # f2
    domain_f2 = [-10,10]
    min_f2 = 0
    f2 = lambda x : sum([np.abs(i) for i in x ]) + np.prod([np.abs(i) for i in x ])
    unimodal_function_set.append([domain_f2, min_f2, f2, 'f2'])



    # f3
    domain_f3 = [-100,100]
    min_f3 = 0
    def f3(x):
        i = 0
        summ = 0
        while i <= len(x):
            summ += sum(x[:i])**2
            i += 1
        return summ
    unimodal_function_set.append([domain_f3, min_f3, f3, 'f3'])

    

    # f5
    domain_f5 = [-30,30]
    min_f5 = 0
    def f5(x):
        i = 0
        summ = 0
        while i < len(x)-1:
            summ += 100 * (x[i+1]-x[i]**2)**2 + (x[i]-1)**2
            i+=1 
        return summ
    
    unimodal_function_set.append([domain_f5, min_f5, f5, 'f5'])

    
    # f6
    domain_f6 = [-100,100]
    min_f6 = 0
    f6 = lambda x : sum([np.floor(i +0.5)**2 for i in x])
    unimodal_function_set.append([domain_f6, min_f6, f6, 'f6'])


    #f7
    domain_f7 = [-1.28,1.28]
    min_f7 = 0
    def f7(x):
        summ = 0
        for i, num in enumerate(x):
            summ += (i+1) * num**4 + np.random.uniform(0,1)
        return summ
    unimodal_function_set.append([domain_f7, min_f7, f7, 'f7'])


    composed_modal_function_set.append(unimodal_function_set)


    

    ## MULTIMODAL FUNCTIONS -->
    multimodal_function_set = []

    # f8
    domain_f8 =[-500,500]
    min_f8 = -12569.5
    f8 = lambda x : sum([-1 * i * np.sin(np.sqrt(np.abs(i))) for i in x])
    multimodal_function_set.append([domain_f8, min_f8, f8, 'f8'])


    #f9
    domain_f9 = [-5.12,5.12]
    min_f9 = 0
    f9 = lambda x : sum([i**2 - 10*np.cos(2*np.pi*i) + 10 for i in x])
    multimodal_function_set.append([domain_f9, min_f9, f9, 'f9'])

    composed_modal_function_set.append(multimodal_function_set)

    ######################################################################################################

    ## TESTING ##

    def testing(move_restriction = False, alpha = 0.25, beta = 0.85, gamma = 1):
        type_multimodal = 0
        for type in composed_modal_function_set:
            print('Type Begin')
            # 10000 generations unimodal
            if type_multimodal == 0:
                num_of_generations = 10000
            # 2000 generations multimodal
            else:
                num_of_generations: 2000

            for function in type:
                i = 0
                j = 0
                results = []
                # run test 50 times for each function to get statisitcs
                while i < 50:
                    # assume dimension of 5 (dimensionality not noted in bird mating optimization paper)
                    results.append(firefly_algorithm(function[2], num_of_generations, function[0], dimensions = 5, population_size = 200, alpha = 0.25, beta = 0.85, gamma = 1, move_restriction = False))
                    # run progress 
                    i+=1
                    if i%10 == 0:
                        j+=1
                        print(function[-1], str(j), '/ 5')

                # results
                print(function[3], '-->    Mean: ', str(np.mean(results)), '     STD:', str(np.std(results)),   '     Expected min: ', str(function[1]))

            type_multimodal = 1

            type_multimodal = 0



    print("Begin testing --> \n")

    # Initial
    print("\n\n Inital test: move_restriction = False, alpha = 0.25, beta = 0.85, gamma = 1 \n\n")
    testing(move_restriction = False, alpha = 0.25, beta = 0.85, gamma = 1)

    # Move Restriction
    print("\n\n Second test [Move Restriction True]: move_restriction = True, alpha = 0.25, beta = 0.85, gamma = 1 \n\n")
    testing(move_restriction = True, alpha = 0.25, beta = 0.85, gamma = 1)

    # Alpha Tuning
    print("\n\n Third test [Alpha Increased]: move_restriction = True, alpha = 0.50, beta = 0.85, gamma = 1\n\n ")
    testing(move_restriction = True, alpha = 0.50, beta = 0.85, gamma = 1)
    print("\n\nFourth test [Alpha Decreased]: move_restriction = True, alpha = 0.10, beta = 0.85, gamma = 1 \n\n")
    testing(move_restriction = False, alpha = 0.10, beta = 0.85, gamma = 1)









