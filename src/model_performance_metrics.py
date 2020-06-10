import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
import random
from sklearn.preprocessing import StandardScaler
from sklearn import ensemble
from sklearn.metrics import f1_score
import operator
import config.config as config
from sklearn.ensemble import GradientBoostingClassifier


def cross_validation():

    cbb = pd.read_csv(config.LOCAL_FE_DATA_FILEPATH)

    train_and_validation = cbb[cbb.Year != 2020]

    factor = pd.factorize(
        ['DIDNT_MAKE', 'R64', 'R32', 'Sweet Sixteen', 'Elite Eight', 'Final Four', 'Finals', 'CHAMPS'])
    dict = {list(factor[1])[i]: list(factor[0])[i] for i in range(len(factor[1]))}
    train_and_validation['postseason_factor'] = train_and_validation['Postseason'].map(dict)

    DIDNT_MAKE = train_and_validation[train_and_validation.Postseason == 'DIDNT_MAKE']
    R64 = train_and_validation[train_and_validation.Postseason == 'R64']
    R32 = train_and_validation[train_and_validation.Postseason == 'R32']
    S16 = train_and_validation[train_and_validation.Postseason == 'Sweet Sixteen']
    E8 = train_and_validation[train_and_validation.Postseason == 'Elite Eight']
    F4 = train_and_validation[train_and_validation.Postseason == 'Final Four']
    SECOND_PLACE = train_and_validation[train_and_validation.Postseason == 'Finals']
    CHAMPIONS = train_and_validation[train_and_validation.Postseason == 'CHAMPS']

    f1_list = []

    for seed in range(1,config.NUMBER_OF_CV_REPLICATES+1):
        print(seed)

        for df in [R32, S16, E8, F4, SECOND_PLACE, CHAMPIONS]:
            fold_list = [1, 2, 3, 4] * int(len(df) / 4)
            random.Random(seed).shuffle(fold_list)
            df['val_fold'] = fold_list

        fold_list = [1, 2, 3, 4] * int(len(DIDNT_MAKE) / 4)
        fold_list.append(1)
        fold_list.append(2)
        fold_list.append(3)
        random.Random(seed).shuffle(fold_list)
        DIDNT_MAKE['val_fold'] = fold_list

        fold_list = [1, 2, 3, 4] * int(len(R64) / 4)
        fold_list.append(1)
        fold_list.append(2)
        random.Random(seed).shuffle(fold_list)
        R64['val_fold'] = fold_list

        DIDNT_MAKE_bal = DIDNT_MAKE
        R64_bal = pd.concat([R64] * 9, ignore_index=True)
        R32_bal = pd.concat([R32] * 18, ignore_index=True)
        S16_bal = pd.concat([S16] * 36, ignore_index=True)
        E8_bal = pd.concat([E8] * 72, ignore_index=True)
        F4_bal = pd.concat([F4] * 144, ignore_index=True)
        SECOND_PLACE_bal = pd.concat([SECOND_PLACE] * 288, ignore_index=True)
        CHAMPIONS_bal = pd.concat([CHAMPIONS] * 288, ignore_index=True)

        all_bal = [DIDNT_MAKE_bal, R64_bal, R32_bal, S16_bal, E8_bal, F4_bal, SECOND_PLACE_bal, CHAMPIONS_bal]

        train_and_validation_bal = pd.concat(all_bal, ignore_index=True)

        for fold in [1, 2, 3, 4]:
            print(fold)
            train = train_and_validation_bal[train_and_validation_bal.val_fold != fold]
            validate = train_and_validation_bal[train_and_validation_bal.val_fold == fold]

            X_train = train[['ADJOE', 'ADJDE', 'EFG_O', 'EFG_D', 'TOR', 'TORD', 'ORB', 'DRB', 'FTR',
                             'FTRD', 'Two_PO', 'Two_PD', 'Three_PO', 'Three_PD', 'ADJ_T', 'avg_conf_power_rating',
                             'win_perc', 'wab_perc']]

            y_train = train['postseason_factor']

            X_val = validate[['ADJOE', 'ADJDE', 'EFG_O', 'EFG_D', 'TOR', 'TORD', 'ORB', 'DRB', 'FTR',
                              'FTRD', 'Two_PO', 'Two_PD', 'Three_PO', 'Three_PD', 'ADJ_T', 'avg_conf_power_rating',
                              'win_perc', 'wab_perc']]

            y_val = validate['postseason_factor']

            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)
            X_val = scaler.transform(X_val)

            classifier = GradientBoostingClassifier(learning_rate=config.LEARNING_RATE,n_estimators =config.N_ESTIMATORS, min_samples_leaf=config.MIN_SAMPLES_LEAF, max_depth=config.MAX_DEPTH, random_state = config.RANDOM_STATE)
            classifier.fit(X_train, y_train)

            y_pred = classifier.predict(X_val)

            f1 = f1_score(y_val, y_pred, average='macro')

            f1_list.append(f1)

    mean_f1 = np.mean(f1_list)

    f1_file = pd.DataFrame([mean_f1], columns=['mean_f1'])
    f1_file.to_csv(config.F1_SCORE_FILE_PATH)