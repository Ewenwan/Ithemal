import os

class MPConfig :

    THREADS_KEY = "OMP_NUM_THREADS";
    AFFINITY_KEY = "KMP_AFFINITY";
    PYTORCH_THREAD_OFFSET = 2;

    def __init__(self, trainers, threads) :
        assert 0 < trainers
        assert 4 <= threads

        self.trainers = trainers
        self.threads = threads
        self.saved_env = None

    def __enter__(self) :
        
        threads = None
        if MPConfig.THREADS_KEY in os.environ :
            threads = os.environ[MPConfig.THREADS_KEY]

        affinity = None
        if MPConfig.AFFINITY_KEY in os.environ :
            affinity = os.environ[MPConfig.AFFINITY_KEY]

        self.saved_env = (threads, affinity)

    def set_env(self, trainer_id) :
        assert trainer_id < self.trainers
    
        os.environ[MPConfig.THREADS_KEY] = str(self.threads - MPConfig.PYTORCH_THREAD_OFFSET);
        os.environ[MPConfig.AFFINITY_KEY] = "verbose,granularity=fine,compact,1,%d" % (trainer_id * self.threads, ) 
    
    def __exit__(self,exc_type, exc_value, traceback)  :
        
        assert self.saved_env is not None

        (threads, affinity) = self.saved_env
        if threads is not None :
            os.environ[MPConfig.THREADS_KEY] = threads

        if affinity is not None :
            os.environ[MPConfig.AFFINITY_KEY] = affinity

        self.saved_env = None

   
