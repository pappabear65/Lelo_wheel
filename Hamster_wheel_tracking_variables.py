"""
Hamster exercise wheel
Variables for the Hamster_wheel_tracking application.
I have tried to make the names readable for their functions in the application.
"""

fileSizeAtMax = 0
reed1TriggerTime = 0
reed1TriggerTimeLast = 0
reed1TriggerTimeDifference = 0
reed1TriggerTimeForDirection = 0
reed1triggerTimeEndOfSession = 0

reed2TriggerTime = 0
reed2TriggerTimeLast = 0
reed2TriggerTimeForDirection = 0

sessionRotationDirection = "tbd"
reedIdForFileWrite = "start up"
systemStatusForFileWrite = "pwr on"
sessionCounter = 0
sessionCounterFormatted = 0
reed1SessionRotationCounter = 0
reed2SessionRotationCounter = 0
distanceRunInSession = 0
distanceRunInSessionPrevious = 0
distanceRunInSessionFormatted = 0
distanceRunInDay = 0
distanceRunInDayFormatted = 0
distanceRunInDayDisplay = 0
distanceRunInDayDisplayFormatted = 0
wheelCircumfrenceMeters = 0.86
secondsInAMilisecond = 0.001
digitRounding = 3
speedMetersPerSecond = 0
maxSpeedToday = 0
fileName = open("hamster_wheel_data.csv", "a")
inactivitySessionEndTime = 2000 #2500
sessionEndFlag = 1
dayEndFlag = 1
timeSynchRefreshSeconds = 15 # ( 10800 = 3 hrs)
flagDayForAverageSpeed = 0

ignoreMeSpeedDirection = False
ignoreMeDirectionDirection = False

localDateLast = 0-0-0
localDisplayTimeLast = 0
sessionCounterFormattedLast = 0
distanceRunInSessionFormattedLast = 0
sessionRotationDirectionLast = "tbd"
distanceRunInDayDisplayFormattedLast = 0
speedMetersPerSecondLast = 0
maxSpeedTodayLast = 0
testMe1Last = "tbd"
testMe2Last = "tbd"