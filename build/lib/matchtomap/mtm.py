import os

##################################################### map matching process for a dataset
def LCSSMapMatching(src,des):

    files=os.listdir(src)

    # progress bar
    cnt=0   # counter for progress bar
    tn=len(files)  # total number for progress bar

    except_list=[]
    for fname in files:
        srcfn=src+"/"+fname
        sp1=str(fname).split('.')
        sp2=sp1[0].split('_')
        desfn=des+"/RNT_"+sp2[1]+".csv"
        
        try:
            mr=LCSSMapMatcher(srcfn)
            SaveResult(mr,desfn)
        except:
            except_list.append(fname)

        # progress bar
        p=int(cnt*100/tn)
        print("\r", end="")
        print("progress...",end=" ")
        print('\033[92m'+str(p)+"%"+'\033[0m', end="")
        cnt=cnt+1
    # progress bar
    print("\r", end="")
    print("progress...",end=" ")
    print('\033[92m'+"100%"+'\033[0m', end="")
    print('\033[93m'+"     completed"+'\033[0m')
    print()
    print()
    print("Excepted Trajectories:", except_list)


##################################################### map matching process for one trajectory
def LCSSMapMatcher(trace_file):
    trace=LoadData(trace_file)
    nx_map=LoadRN(trace)
    match_result=MapMatching(trace, nx_map)
    return match_result


##################################################### plot map matching result in dataframe
def PlotResult(match_result):
    match_result.path_to_geodataframe().plot()  


##################################################### save map matching result in a file
def SaveResult(match_result, result_file):
    # convert result to dataframe
    pdf = match_result.path_to_geodataframe()
    pdf.to_csv(result_file)


#####################################################  load data 
def LoadData(trace_file):
    from mappymatch import package_root
    import pandas as pd
    df = pd.read_csv(trace_file)
    from mappymatch.constructs.trace import Trace
    trace = Trace.from_csv(trace_file, lat_column="latitude", lon_column="longitude", xy=True)
    return trace


#################################################### download road network
def LoadRN(trace):
    # build geofance from trace
    from mappymatch.constructs.geofence import Geofence
    geofence = Geofence.from_trace(trace, padding=2e3)
    # load road network
    from mappymatch.maps.nx.nx_map import NxMap, NetworkType
    nx_map = NxMap.from_geofence(geofence, network_type=NetworkType.DRIVE)    
    return nx_map


#################################################### map matching 
def MapMatching(trace, nx_map):
    from mappymatch.matchers.lcss.lcss import LCSSMatcher
    matcher = LCSSMatcher(nx_map)
    match_result = matcher.match_trace(trace)
    return match_result