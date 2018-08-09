import matplotlib
import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib import rc
from netCDF4 import Dataset

def _sigmoid(x,amp):
    """Sigmoid function used internally for determining colors of particles.
    """
    return 1/(1+np.exp(amp*x))

def plot_kernel_trajectories(filename, interval=200):
    """ Present the animation of kernel moving trajectories.
    """

    clrs = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', \
            'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
    
    pfile = Dataset(filename, 'r')
    lon = np.ma.filled(pfile.variables['lon'], np.nan)
    lat = np.ma.filled(pfile.variables['lat'], np.nan)
    time = np.ma.filled(pfile.variables['time'], np.nan)
    word = np.ma.filled(pfile.variables['word'])[0,:,:]
    meaning = np.ma.filled(pfile.variables['meaning'])[0,:,:]
    color = np.ma.filled(pfile.variables['particle_color'], np.nan)
    
    time_len = lat.shape[1]
    word_shape = word.shape
    word = np.reshape(np.array([wrd.encode('ascii') for wrd in np.reshape(word,[-1])]),word_shape)
    meaning = np.reshape(np.array([mng.encode('ascii') for mng in np.reshape(meaning,[-1])]),word_shape)
    pairs = [(word[i,j]+':'+meaning[i,j]) for i in range(word_shape[0]) for j in range(word_shape[1])]
    legends = list(set(pairs))
    wrd_mng = np.reshape(np.array(pairs),word_shape)

    ## If amount of word_meaning pairs is not greater than that of default colors, use default colors.
    ## Otherwise assign the colors with sigmoid function.
    use_default_color = True if len(legends)<=len(clrs) else False
        
    fig = plt.figure()
    ax = plt.axes(xlim=(np.nanmin(lon), np.nanmax(lon)), ylim=(np.nanmin(lat), np.nanmax(lat)))
    plottimes = np.unique(time)
    plottimes = plottimes[~np.isnan(plottimes)]
    b = time == plottimes[0]
    scat = ax.scatter(lon[b], lat[b], s=60, c=color[b])
    ttl = ax.set_title('Particle at time ' + str(plottimes[0]))
    frames = np.arange(1, len(plottimes))

    def animate(t):
        ax.cla()
        ax.set_xlim(np.nanmin(lon), np.nanmax(lon))
        ax.set_ylim(np.nanmin(lat), np.nanmax(lat))

        for j in range(len(legends)):
            try:
                idx = wrd_mng[:,t]==legends[j]
                lat_ = np.reshape(np.array(lat[idx],dtype=np.float32),[-1,time_len])
                lon_ = np.reshape(np.array(lon[idx],dtype=np.float32),[-1,time_len])
                time_ = np.reshape(np.array(time[idx],dtype=np.float32),[-1,time_len])
                b = time_ == plottimes[t]
                if not use_default_color:
                    color_ = np.reshape(np.array(color[idx],dtype=np.float32),[-1,time_len])
                    clr = color_[b][0]
                    clrp = [_sigmoid(3*np.abs(clr-0.25)-0.5,-5),_sigmoid(3*np.abs(clr-0.5)-0.75,-5),\
                            _sigmoid(3*np.abs(clr-0.75)-1.0,-5)]
                    clrp = matplotlib.colors.to_hex(clrp)
                else:
                    clrp = clrs[j]
                ax.scatter(lon_[b], lat_[b], c=clrp, s=60, label=legends[j])
                ax.legend(loc=1)
            except:
                continue            
        ttl.set_text('Particle at time ' + str(plottimes[t]))
        return scat,

    rc('animation', html='jshtml')
    anim = animation.FuncAnimation(fig, animate, frames=frames,
                                   interval=interval, blit=False)


    plt.close()
    return anim
