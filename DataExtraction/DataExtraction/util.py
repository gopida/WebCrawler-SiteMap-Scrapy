from datetime import datetime


def getDateTime(timestring):

    text = timestring.split("/")
    time_text = text[0].strip() + text[1].strip()
    daytime = datetime.strptime(time_text, '%B %d, %Y%H:%M %p')
    return daytime
