

def find_dwell_time_FWHM(time, event, event_type):
    
    """ Finds the dwell time of an event using the full width at half maximum (FWHM) method
    
    Args:
        time (numpy.ndarray): The time array corresponding to one event.
        event (numpy.ndarray): The current array for the event.
        event_type (str): Type of event to analyze. Accepts "trough-peak" or "peak-only".

    Returns:
        float: The dwell time of the event, calculated as the difference in time between the start and end points defined by the FWHM method.

    """

    start, end = 0, 0 # Initialize
    
    if event_type == "trough-peak" and event[0] >= np.min(event)/2 and event[-1] <= np.max(event)/2:
        # condition prevents error in the case where the start and end of the event are not below the half max value
        half_max_peak = np.max(event)/2
        intercept_peak = np.where(np.diff(np.sign(event - half_max_peak)))[0] # find where the peak signal crosses the half max value
        half_max_trough = np.min(event)/2
        intercept_trough = np.where(np.diff(np.sign(event - half_max_trough)))[0] # find where the trough signal crosses the half max value

        start = intercept_trough[intercept_trough < np.argmin(event)]
        start = start[-1] if start.size != 0 else 0 # 
        end = intercept_peak[intercept_peak > np.argmax(event)]
        end = end[0] if end.size != 0 else len(event) - 1
        
    elif event_type == "peak-only" and event[0] <= np.max(event)/2 and event[-1] <= np.max(event)/2:
        half_max_peak = np.max(event)/2
        intercepts = np.where(np.diff(np.sign(event - half_max_peak)))[0] # find where the signal crosses the half max value
        
        start = intercepts[intercepts < np.argmax(event)]
        start = start[-1] if start.size != 0 else 0
        end = intercepts[intercepts > np.argmax(event)]
        end = end[0] if end.size != 0 else len(event) - 1
    
    else:
        start = 0
        end = len(event) - 1
        
    dwell_time = time[end] - time[start]
        
    return dwell_time