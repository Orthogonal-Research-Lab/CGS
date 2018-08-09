import parcels
import warnings
import numpy as np
from datetime import timedelta

class kernel_file(parcels.ParticleFile):
    """Inherit from parcels.ParticleFile.
    Add additional dimension: 'word_dim', and additional varaibles: 'word', 'meaning', 'particle_color'
    in netCDF file to save the words, meanings and colors of kernels respectively.
    """
    
    def __init__(self, name, particleset, outputdt=np.infty, write_ondelete=False):
        super(kernel_file,self).__init__(name, particleset, outputdt=outputdt, write_ondelete=write_ondelete)
        self.dataset.createDimension('word_dim',None)
        self.word = self.dataset.createVariable('word',str,['word_dim','traj','obs'],fill_value=np.nan)
        self.meaning = self.dataset.createVariable('meaning',str,['word_dim','traj','obs'],fill_value=np.nan)
        self.particle_color = self.dataset.createVariable('particle_color','f4',['traj','obs'],fill_value=np.nan)
        
    def write(self, pset, time, sync=True, deleted_only=False):
        """Write function of class kernel_file.
        Overload write function from parcels.particlefile module.
        Save words,meanings,particel colors in netCDF.
        """
        if isinstance(time, timedelta):
            time = time.total_seconds()
        if self.lasttime_written != time and \
           (self.write_ondelete is False or deleted_only is True):
            if pset.size > 0:

                first_write = [p for p in pset if p.fileid < 0 or len(self.idx) == 0]  # len(self.idx)==0 in case pset is written to new ParticleFile
                for p in first_write:
                    p.fileid = self.lasttraj
                    self.lasttraj += 1

                self.idx = np.append(self.idx, np.zeros(len(first_write)))

                for p in pset:
                    i = p.fileid
                    self.id[i, self.idx[i]] = p.id
                    self.time[i, self.idx[i]] = time
                    self.lat[i, self.idx[i]] = p.lat
                    self.lon[i, self.idx[i]] = p.lon
                    self.z[i, self.idx[i]] = p.depth
                    # save words,meanings,particel colors in netCDF
                    self.word[:, i, self.idx[i]] = np.array([p.word_state.word],dtype=object)
                    self.meaning[:, i, self.idx[i]] = np.array([p.word_state.meaning],dtype=object)
                    self.particle_color[i , self.idx[i]] = p.word_state.color
                    for var in self.user_vars:
                        getattr(self, var)[i, self.idx[i]] = getattr(p, var)
                for p in first_write:
                    for var in self.user_vars_once:
                        getattr(self, var)[p.fileid] = getattr(p, var)
            else:
                logger.warning("ParticleSet is empty on writing as array")

            if not deleted_only:
                self.idx += 1
                self.lasttime_written = time

        if sync:
            self.sync() 
