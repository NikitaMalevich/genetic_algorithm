import numpy as np
import pandas as pd
import random


#1*e+2*a+3*b+4*c = 30


# eq = 1*e+2*a+3*b+4*c - 30

def population(N_person):
    '''Create population'''
    df_population= pd.DataFrame([])
    for i in range(0, N_person):
        a = round(0 + random.random() * 30, 3)
        b = round(0 + random.random() * 30, 3)
        c = round(0 + random.random() * 30, 3)
        e = round(0 + random.random() * 30, 3)

        df_population.loc[i, 'a'] = a
        df_population.loc[i, 'b'] = b
        df_population.loc[i, 'c'] = c
        df_population.loc[i, 'e'] = e
    return df_population

def choose_2_person(df_population):
    P1,P2 = 0,0

    while P1 == P2:
        P1 = int(random.choice(np.linspace(0,len(df_population)-1,len(df_population))))
        P2 = int(random.choice(np.linspace(0,len(df_population)-1,len(df_population))))

    return P1,P2


def direct_task(df_population, N_parents):
    a = df_population['a'].iloc[N_parents]
    b = df_population['b'].iloc[N_parents]
    c = df_population['c'].iloc[N_parents]
    e = df_population['e'].iloc[N_parents]

    function_value = 1*e+2*a+3*b+4*c

    print(f'function_value={function_value}')
    return function_value


def diviation(df,string):
    a = df['a'].iloc[string]
    b = df['b'].iloc[string]
    c = df['c'].iloc[string]
    e = df['e'].iloc[string]

    function_value = 1 * e + 2 * a + 3 * b + 4 * c
    ref_value = 30
    error = abs(function_value-ref_value)/(ref_value/100)

    df.loc[string, 'error'] = error


def crossover(df_population,df_new_generation,P1,P2,string):

    P1 = df_population.loc[P1].to_frame(name='P1')
    P2 = df_population.loc[P2].to_frame(name='P2')

    # random choose childs characteristics
    a = random.choice([P1.iloc[0][0], P2.iloc[0][0]])
    b = random.choice([P1.iloc[1][0], P2.iloc[1][0]])
    c = random.choice([P1.iloc[2][0], P2.iloc[2][0]])
    e = random.choice([P1.iloc[3][0], P2.iloc[3][0]])

    df_new_generation.loc[string,'a'] = a
    df_new_generation.loc[string, 'b'] = b
    df_new_generation.loc[string, 'c'] = c
    df_new_generation.loc[string, 'e'] = e


def main():
    Er = 100
    k,ITER = 0,0
    df_new_generation = pd.DataFrame([])
    P = population(100)

    while Er > 0.05:
        if ITER >= 20:
            print(f'число итераций достигло = {ITER}')
            find = P.loc[P['error'] == Er]
            print(find)
            return None
        k +=1
        ITER += 1
        print(f' \n ITERATION {ITER}')

        for i in range(0,2*len(P)):
            two_parents = choose_2_person(P)
            P1 = two_parents[0]
            P2 = two_parents[1]
            crossover(df_population = P, df_new_generation = df_new_generation, P1=P1, P2=P2,string=i)

        for i in range(0,len(P)):
            diviation(df=P, string=i)
        for i in range(0,len(df_new_generation)):
            diviation(df=df_new_generation,string=i)

        print(P)
        print(df_new_generation)
        df_next = pd.concat([P,df_new_generation],ignore_index=True)

        P = df_next[df_next['error'] < 50]
        P = P.reset_index()
        Er = P['error'].min()

        if len(P) <= 1:
            print('i cant do this, try again   length massive = ',len(P))
            return ()
        if k == 2:
            P = P.drop(['index','level_0'],axis =1)
            k = 0
        print(P)
        print(f'min_er={Er}')

    find = P.loc[P['error'] == Er]

    print(find)
    print(f'Iterarions={ITER}')



main()