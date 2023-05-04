
'''
use this function to setup a Paperspace Instance
'''
def _setup_data(data_dir, competition_name):
    '''
    # How to download competition data to temp folder(data) 
    # unzip it there, then symlink it like its a subdir
    # NOTE: make sure kaggle.json is in /root/.kaggle/
    data_dir: put all data here, it is removed whenever instance terminated
    competition_name: competition data to download
    '''
    import os
    from os.path import exists
    import subprocess
    print('setup data...')
   
    loc="/root/"+data_dir+'/'

    #if /root/data exists then this script has been run already so bail
    if os.path.exists(loc):
        print('Script already ran...bailing')
        return
  
    #remove original symlink from this directory
    if exists('./data'):os.remove('./data')

    #create temp holder
    subprocess.Popen(['mkdir',loc]).wait()

    #symlink it
    subprocess.Popen('ln -s '+loc+' ./' +data_dir,shell=True).wait()
    
    #download competition data to temp data folder, this assummes .kaggle.json key is in the /.kaggle directory
    subprocess.Popen('cd ./' +data_dir+ ';kaggle competitions download -c '+competition_name,shell=True).wait()

    #unzip it, -q is silent
    subprocess.Popen('cd ./' +data_dir+ ';unzip -q '+ competition_name + '.zip',shell=True).wait()
    
    #remove zip file
    subprocess.Popen('cd ./datap;rm amp-parkinsons-disease-progression-prediction.zip',shell=True).wait()
    
    return True

# #run the function this wraps just once
# def _run_once(f):
#     #use @run_once decorator
#     def wrapper(*args, **kwargs):
#         if not wrapper.has_run:
#             wrapper.has_run = True
#             return f(*args, **kwargs)
#     wrapper.has_run = False
#     return wrapper

def _setup_env(data_dir): 
    '''
    data_dir: symlink, points to where data will go, if exists 
              then this function has run already this session
    '''
    import os
    from os.path import exists
    import subprocess
    
    #if there we already ran, bail
    if os.path.exists(os.readlink(data_dir)):
        print("_setup_env already run, bailing...")
        return
   
    print('setup environment...')
    
    #get the libraries needed
    _setup_packages()
        
    #setup dotfiles   
    subprocess.Popen("wget https://raw.githubusercontent.com/kperkins411/dotfiles/master/setup.sh",shell=True).wait()

    #make executable, then run
    print('Running setup.sh...')
    subprocess.Popen('chmod 700 setup.sh; ./setup.sh',shell=True).wait()
    
    #remove setup file
    if exists('./setup.sh'):os.remove('./setup.sh')

    #just in case its wide open
    print('Changing key permissions...')
    os.system('chmod 600 /root/.kaggle/kaggle.json')
 
def _setup_packages():
    '''
    install needed libraries for this project
    '''
    #what about Kaggle API?  'pip install kaggle'
    print('Setup python packages...')
    import os
    try: from path import Path
    except ModuleNotFoundError:
        os.system('pip install path --quiet')
        from path import Path
    try: import timm
    except ModuleNotFoundError:
        os.system('pip install timm --quiet')
        import timm
    try: import optuna
    except ModuleNotFoundError:
        os.system('pip install optuna --quiet')
        import optuna  
        
def setup_all(data_dir, competition_name):
    '''
    setup for Kaggle competition competition_name
    data_dir: put all data here, it is removed whenever instance terminated
    competition_name: competition data to download
    '''
    _setup_env(data_dir)
    _setup_data(data_dir, competition_name)  