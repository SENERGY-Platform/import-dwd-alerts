# import-dwd-alerts

Allows you to import weather alerts from DWD.

## Outputs
* warnCellId (string): Identifies the warning area. Data about these ids, such as shapes, can be found [here](https://maps.dwd.de/geoserver/web/wicket/bookmarkable/org.geoserver.web.demo.MapPreviewPage?10&filter=false) (search for Warngebiete)
* regionName (string): Human readable name of the warning area
* end (string): when the alert ends (rfc3339)
* start (string): when the alert starts (rfc3339)
* event (string): Human readable type of warning
* type (int): integer encoded event
* state (string): Political state of warning area 
* level (int): Warning intensity level. Find details [here](https://www.dwd.de/DE/wetter/warnungen_aktuell/kriterien/warnkriterien.html)
* description(string): Human readable description of the warning 
* headline(string): Human readable summary of description 
* instruction (string): Actions to be taken
* stateShort (string): Abbreviation of state
* altitudeStart (string): Altitude in meters above see level in which the warning is active
* altitudeEnd (string): Altitude in meters above see level in which the warning is not active 
* urgency (string): Either 'Warnung' (shortly before the event or when the event is active) or 'Vorabinformation' (in advance)

## Configs
You can filter warnings by location by providing region names and/or warn cell ids and/or state abbreviations.
If an alert matches at least one filter criteria, it will be imported.

 * FilterRegionNames (list): List of strings that match a regionName
 * FilterWarnCellIds (list): List of strings that match a warnCellId
 * FilterStateShorts (list): List of strings that match a stateShort

---

This tool uses publicly available data provided by Deutscher Wetterdienst.

The supplied information about warn levels and events are no substitution for the official warnings by DWD.
This tool may only be used for weather analysis and not to warn user about current weather events.
Please use the official warnings available [here](https://www.dwd.de/DE/wetter/warnungen_gemeinden/warnWetter_node.html).
