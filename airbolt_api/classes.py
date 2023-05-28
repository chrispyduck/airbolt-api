from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, EmailStr, Field, conint


class UserInfo(BaseModel):
    id: str = Field(alias="_id")
    username: str
    time_created: datetime = Field(alias="timeCreated")
    name: str
    email: EmailStr
    roles: List[str]
    failed_login_attempts: int = Field(alias="failedLoginAttempts")
    two_factor_enabled: bool = Field(alias="twoFactorEnabled")
    profile_picture: str = Field(alias="profilePicture")
    blocked_until: Optional[str] = Field(alias="blockedUntil")
    country: str
    currency: str
    timezone: str
    deleted: bool
    cell_scan_limit: int = Field(alias="cellScanLimit")

class SessionInfo(BaseModel):
    id: str = Field(alias="_id")
    user_id: str = Field(alias="userId")
    key: str
    time: datetime
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    v: int = Field(alias="__v")

class LoginResult(UserInfo):
    session: SessionInfo
    auth_header: str = Field(alias="authHeader")

class TemperatureConfiguration(BaseModel):
    enable: bool
    send_location: bool = Field(alias="sendLocation")
    realert_duration: int = Field(alias="reAlertDuration")
    condition: Literal['lessOrEqual']
    level: int = conint(ge=1)
    unit: Literal['f', 'c']

class AccelerometerConfiguration(BaseModel):
    enable: bool
    ultra_power_mode: bool = Field(alias="ultraPowerMode")
    send_location: bool = Field(alias="sendLocation")
    sensitivity: int = conint(ge=1, le=10)
    duration: int = conint(ge=1)

class WaterAlarmConfiguration(BaseModel):
    enable: bool
    send_location: bool = Field(alias="sendLocation")
    realert_duration: int = Field(alias="reAlertDuration")

class FoundDevice(BaseModel):
    id: str = Field(alias="_id")
    temperature: TemperatureConfiguration
    accelerometer: AccelerometerConfiguration
    water_alarm: WaterAlarmConfiguration = Field(alias='waterAlarm')
    device_type: Literal['shield_gps'] = Field(alias='deviceType')
    latitude: float # unused?
    longitude: float # unused?
    alert_level: int = Field(alias="alertLevel")
    last_history_time: datetime = Field(alias="lastHistoryTime")
    mark_as_lost: int = Field(alias="markAsLost")
    tone: int
    deleted: bool
    color: Optional[str]
    tsa_accessible: bool = Field(alias="tsaAccessible")
    modem_voltage: int
    modem_temperature: int
    modem_state: int
    operating_mode: Literal['batteryLife', 'responsiveness'] = Field(alias='operatingMode')
    schedule_report: List[Literal['gps', 'temp', 'cell']] = Field(alias='scheduleReport')
    schedule_report_interval: int = Field(alias='scheduleReportInterval')
    location_report_mode: str = Field(alias='locationReportMode') # should be enum? found 'once'
    led_flash: bool = Field(alias='ledFlash')
    push_notification: bool = Field(alias='pushNotification')
    email_alerts: bool = Field(alias='emailAlerts')
    location_update_notification: bool = Field(alias='locationUpdateNotification')
    sos_alert_notification: bool = Field(alias='sosAlertNotification')
    alarm: bool
    notification_emails: List[EmailStr] = Field(alias='notificationEmails')
    emergency_mode: bool = Field(alias='emergencyMode')
    proximity: str # found: 'medium'
    device_uuid: str = Field(alias='deviceUUID')
    device_picture: str = Field(alias='devicePicture')
    name: str
    time_created: datetime = Field(alias='timeCreated')
    last_seen_time: datetime = Field(alias='lastSeenTime')
    last_report_type: Literal['Motion', 'SOS', 'Schedule', 'Location'] = Field(alias="lastReportType") # water?

    # unused fields:
    """
    {
        "isTrialAvailed": true,
        "rai_value": false,
        "listenToLock": false,
        "subscriptionRemindOn": null,
        "userId": "646805c7b91db16459331694",
        "passcode": "00000000000000000000000000000000",
        "markedByUsername": "",
        "markedByEmail": "",
        "masterKey": "",
        "outOfRangeTimeout": null,
        "imei": "350916062274561",
        "iccid": "8931681011102392389F",
        "esim": {
            "_id": "64681196b91db16459331733",
            "iccid": "8931681011102392389F",
            "eid": "89044045817727484800000048120740",
            "status": "Active",
            "createdAt": "2023-05-20T00:17:26.410Z",
            "updatedAt": "2023-05-21T11:37:21.340Z",
            "__v": 0
        },
        "subscriptionRemindCount": null,
        "createdAt": "2023-05-20T00:17:26.414Z",
        "updatedAt": "2023-05-26T00:20:54.337Z",
        "edrx_ptw": -1,
        "edrx_value": -1,
        "psm_active_time": 16,
        "psm_tau": 14400,
        "cellRequestsCount": 6,
        "cellRequestsResetOn": "2023-06-21T23:59:59.595Z",
        "continuousReportReset": null,
        "privilege": 3,
        "sharedUserCount": 1,
        "share_count": 1,
        "subscription": {
            "status": "Trial ends Jun 20 2023 "
        },
        "cellScanLimit": 150
    },
    """


class HistoryEntry(BaseModel):
    id: str = Field(alias='_id')
    device_uuid: str = Field(alias='deviceUUID')
    modem_voltage: Optional[int]
    modem_temperature: Optional[int]
    type: Literal['gps', 'mcell', 'scell'] # cell is a guess
    time_created: datetime = Field(alias='timeCreated')
    latitude: float
    longitude: float
    accuracy: float
    location_changed: bool = Field(alias='locationChanged')
    duration: int
    alert_type: Literal['Motion', 'SOS', 'Schedule', 'Location'] = Field(alias='alertType')
    address: str
    last_seen_on: datetime = Field(alias='lastSeenOn')

    """
    "latitude": 38.8321749,
    "longitude": -77.2072074,
    "accuracy": 807.957,
    "unlockType": 0,
    "isLocked": false,
    "locationChanged": true,
    "modem_voltage": 3926,
    "modem_temperature": 25,
    "alertType": "Motion",
    "duration": 0,
    "_id": "646cf0bc4346239e7508a868",
    "deviceUUID": "fca00cf27698",
    "type": "mcell",
    "timeCreated": "2023-05-23T16:58:11.000Z",
    "address": "Little River Turnpike, Koreatown, Accotink Heights, Annandale, Fairfax County, Virginia, 22031, United States",
    "lastSeenOn": "2023-05-23T16:58:11.000Z"
    """


class Pagination(BaseModel):
    total: int
    """Total number of records"""

    total_pages: int = Field(alias='totalPages')
    """Total number of pages"""

    next: int
    """Next page number"""
    has_next: bool = Field(alias='hasNext')
    """Whether there's a next page"""

    prev: int
    """Previous page number"""
    has_prev: bool = Field(alias='hasPrev')
    """Whether there's a previous page"""
    
    per_page: int = Field(alias='perPage')
    """Page size"""

    current: int
    """Current page number"""

    """
    "total": 163,
    "totalPages": 17,
    "next": 2,
    "hasNext": true,
    "prev": 0,
    "hasPrev": false,
    "perPage": 10,
    "current": 1
    """


class DeviceHistoryPage(BaseModel):
    success: bool
    data: List[HistoryEntry]
    pagination: Pagination
