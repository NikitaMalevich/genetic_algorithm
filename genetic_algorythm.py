import random

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def population(N_person):
    '''Create population'''
    df_population= pd.DataFrame([])
    for i in range(0, N_person):
        I0 = random.random() * random.choice([1e-1,1,1e-2,1e-3,1e-4,1e-5,1e-6,1e-7,1e-8])
        R1 = random.random() * random.choice([1e-3,1e-2,1e-1,1,1e1,1e2,1e3])
        R2 = random.random() * random.choice([1e-3,1e-2,1e-1,1,1e1,1e2,1e3])

        df_population.loc[i, 'I0'] = I0
        df_population.loc[i, 'R1'] = R1
        df_population.loc[i, 'R2'] = R2
    return df_population

def direct_task(df,string):
    I0 = df['I0'].iloc[string]
    R1 = df['R1'].iloc[string]
    R2 = df['R2'].iloc[string]

    df_direct_task = pd.DataFrame([])
    for i in range(0,5):
        Ud = i*1e-2
        Id = I0*(np.exp(40*Ud)-1)
        I = Id + Ud/R1
        U = Ud + I*R2
        df_direct_task.loc[i, 'U'] = round(U,3)
        df_direct_task.loc[i, 'I'] = round(I,3)
    df_direct_task.index = [0,1,2,3,4]
    return df_direct_task

def choose_2_person(df_population):
    P1,P2 = 0,0

    while P1 == P2:
        P1 = int(random.choice(np.linspace(0,len(df_population)-1,len(df_population))))
        P2 = int(random.choice(np.linspace(0,len(df_population)-1,len(df_population))))

    return P1,P2


def diviation(df_initial,df,string):
    I0 = df['I0'].iloc[string]
    R1 = df['R1'].iloc[string]
    R2 = df['R2'].iloc[string]

    df_task = pd.DataFrame([])

    #TASK
    for i in range(0,5):
        Ud = i*1e-2

        Id = I0 * (np.exp(40 * Ud) - 1)
        I = Id + Ud / R1
        U = Ud + I * R2

        df_task.loc[i, 'U'] = round(U, 3)
        df_task.loc[i, 'I'] = round(I, 3)

    Error = 0
    for i in range(len(df_task)):
        Error = Error + (df_initial.loc[i, 'U'] - df_task.loc[i, 'U'])**2 + \
                (df_initial.loc[i, 'I'] - df_task.loc[i, 'I'])**2

    df.loc[string, 'error'] = Error
    return df_task



def crossover(df_population,df_new_generation,P1,P2,string):
    # print(f'P2={P2}, len_df={len(df_population)}  \n {df_population}')
    P1 = df_population.loc[P1].to_frame(name='P1')
    P2 = df_population.loc[P2].to_frame(name='P2')

    # random choose childs characteristics
    I0 = random.choice([P1.iloc[0][0], P2.iloc[0][0]])
    R1 = random.choice([P1.iloc[1][0], P2.iloc[1][0]])
    R2 = random.choice([P1.iloc[2][0], P2.iloc[2][0]])

    df_new_generation.loc[string,'I0'] = I0
    df_new_generation.loc[string, 'R1'] = R1
    df_new_generation.loc[string, 'R2'] = R2

def VA_char(df_initial,df_task):
    I_in, I_res = df_initial['I'], df_task['I']
    U_in, U_res = df_initial['U'], df_task['U']
    plt.plot(I_in,U_in,color = 'blue',label='initial')
    plt.plot(I_res, U_res,color = 'orange',label='result')
    plt.grid()
    plt.xlabel('I,A')
    plt.ylabel('U,V')
    plt.legend()
    plt.show()

def main():
    df_initial = pd.DataFrame({'U': [0, 0.136, 0.324, 0.591, 0.9735],
                               'I': [0, 0.6, 1.449, 2.67, 4.445]})
    Er = 100
    ITER,repeat = 0,0
    E = [0]
    df_new_generation = pd.DataFrame([])
    P = population(100)

    while Er > 0.05:
        if ITER >= 100:
            print(f'число итераций достигло = {ITER}')

            find = P.loc[P['error'] == Er]
            print(find)
            return None

        ITER += 1
        print(f' \n ITERATION {ITER}  repeat = {repeat}')

        for i in range(0, len(P)):
            two_parents = choose_2_person(P)
            P1 = two_parents[0]
            P2 = two_parents[1]
            crossover(df_population=P, df_new_generation=df_new_generation, P1=P1, P2=P2, string=i)

        for i in range(0, len(P)):
            diviation(df=P, string=i,df_initial=df_initial)

        for i in range(0, len(df_new_generation)):
            diviation(df=df_new_generation, string=i,df_initial=df_initial)

        df_next = pd.concat([P, df_new_generation], ignore_index=True)
        print(df_next)

        if ITER % 4 == 0:
            R = df_next[df_next['error'] < Er * 5]
        else:
            R = df_next[df_next['error'] < Er * 10]

        P = R[R['I0'] > 0]
        P = P.reset_index()
        Er = P['error'].min()

        if E[-1] == Er:
            repeat +=1
            if repeat == 20:
                print(f'repeat ={repeat}, try resolve it again')
                main()
                ITER,repeat = 0,0
                # break
        else:
            repeat = 0
            E = []
        E.append(Er)

        if len(P) <= 2:
            print('i cant do this, try again____length massive = ', len(P))
            return ()

        if 'index' in P:
            P = P.drop(['index'], axis=1)

        P = P.drop_duplicates(subset=['I0','R1','R2'],ignore_index = True)

        print(f' \n {P}')
        print(f'min_er={Er}')

    find = P.loc[P['error'] == Er]

    print(f'\n Iterarions={ITER}')
    print(find)

    df_res = direct_task(find,string=0)
    VA_char(df_initial,df_res)

if __name__ == "__main__":
	main()