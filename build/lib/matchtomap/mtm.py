

##################################################### map matching process
def LCSSMapMatching(trace_file):
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
    pdf = match_result.matches_to_geodataframe()
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