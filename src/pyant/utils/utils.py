import sys, os, string, getopt, time, shutil, glob

DAG = ['ma','di','wo','do','vr','za','zo']
MAAND = ['jan', 'feb', 'maa', 'apr', 'mei', 'jun', 'jul', 'aug', 'sep', 'okt', 'nov', 'dec']


def today(uur_min=False):
    lt = time.localtime()
    yr = str(lt.tm_year)[2:]
    day = str(lt.tm_mday)
    mnd = MAAND[lt.tm_mon-1]
    if uur_min:
        hm  = '%2d%2d'%(lt.tm_hour, lt.tm_min)
        return day+mnd+yr+'_'+hm
    else:
        return day+mnd+yr


def datename(fname, uur_min=False):
    fn, ext = os.path.splitext(fname)
    if uur_min:
        return fn+'_'+today(uur_min=True)+ext
    else:
        return fn+'_'+today()+ext


def progress(count, stap1=100, stap2=1000):
    if count % 100 == 0:
        print('.', end-'')
    if count % 1000 == 0:
        print(f"-> {format(count)}")


def its_time(condition):
    """
    test conditie. Conditie is boolean expressie op basis van een aantal
    variabelen:
    altijd
    nooit
    dag             dag van week (integer, maandag == 1, etc)
    week            weeknummer (integer)
    maand           naam van maand ('jan', etc)
    jaar            jaar (integer)
    dow             dag_van_week ('ma', etc)
    dom             dag van maand (integer)
    doj             dag van jaar (integer)

    bijv:
    "dag_van_week in ['ma', 'wo', 'vr']"
    "dag_van_maand ==15"
    "nooit"
    """
    if condition:
        lt = time.localtime()

        context = {}
        context['altijd'] = True
        context['nooit'] = False
        context['dag'] = lt.tm_wday+1
        context['week'] = int(time.strftime('%W', time.localtime(time.time())))
        context['maand'] = MAAND[lt.tm_mon-1]
        context['jaar'] = lt.tm_year
        context['dag_van_week'] = DAG[lt.tm_wday]
        context['dag_van_maand'] = lt.tm_mday
        context['dag_van_jaar'] = lt.tm_yday

        return eval(condition, context, context)
    else:
        return True
