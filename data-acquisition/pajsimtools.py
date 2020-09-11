try:
    import __builtin__
    __builtin__.total_sim_pc = 0
except:
    import builtins
    print('need to fix for python3 later')

def Run(title, wait_pcharge_C):
    print('Run: '+title+'***** pC={}'.format(wait_pcharge_C))
    __builtin__.total_sim_pc = __builtin__.total_sim_pc + wait_pcharge_C
    return 0

def Delay(time):
    print('Delay: {}'.format(time))
    return 0

def Set(pv, value):
    print('Set: {} = {}'.format(pv, value))
    return 0

def Simulate():
    print('*****Simulate mode')
    print('total PC= {}'.format(__builtin__.total_sim_pc))
    print('total time at 1.4 MW= {} hours'.format(__builtin__.total_sim_pc / 5.))
    return {'simulation':''}

def Submit(name):
    print('*****Submit mode: '+name)
    print('total PC= {}'.format(__builtin__.total_sim_pc))
    print('total time at 1.4 MW= {} hours'.format(__builtin__.total_sim_pc / 5.))
    return 0
