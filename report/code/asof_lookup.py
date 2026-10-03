def vintage_view(frame, cutoff, first=False):
    cutoff = pd.Timestamp(cutoff).strftime('%Y-%m-%d')
    if first:
        eligible = frame.drop_duplicates('observation_month',keep='first')
        eligible = eligible.loc[eligible.realtime_start <= cutoff]
    else:
        eligible = frame.loc[(frame.realtime_start <= cutoff) & (frame.realtime_end >= cutoff)]
    if eligible.duplicated('observation_month').any():
        raise ValueError('Overlapping vintage intervals')
    return eligible.set_index('observation_month')[['value','realtime_start']].sort_index()
