import pprint
from garminconnect import Garmin, GarminConnectConnectionError, GarminConnectAuthenticationError, GarminConnectTooManyRequestsError
from typing import Optional, Dict
import os
import datetime
import json
import rsa
import functools
from time import sleep
from logger import log_settings

app_log = log_settings()


def error_wrap(original_func):
    @functools.wraps(original_func)
    def inner(*args, **kwargs):
        try:
            x = original_func(*args, **kwargs)
            app_log.debug(f"Call of: {original_func.__name__} was succesfull")
            return x
        except (
                GarminConnectConnectionError, GarminConnectTooManyRequestsError,
                GarminConnectAuthenticationError) as err:
            app_log.error(f"Connection error: {err}")
        except Exception as ex:
            app_log.error(f"General error: {ex}")
    return inner


class MyGarmin:

    client = None
    retry_number = 5
    default_sleep = 5
    _user = None
    _pwd = None
    is_connect = False
    token_dir = "token"

    def __init__(self) -> None:
        self.login_path = os.path.join(os.getcwd(), self.token_dir, "garmin_login.json")
        self.rsa_key_pass = os.path.join(os.getcwd(), self.token_dir, "rsa_key")
        self.passw_path = os.path.join(os.getcwd(), self.token_dir, "pass.txt")
        self.get_user_login()
        self.get_pwd()
        self.create_garmin_inst()
        self._day_stats = dict()

    @error_wrap
    def create_garmin_inst(self):
        self.client = Garmin(self.user, self.pwd)

    @property
    def user(self):
        return self._user

    @property
    def pwd(self):
        return self._pwd

    def get_pwd(self):
        with open(self.passw_path, "rb") as pw:
            pwd = pw.read()
        with open(self.rsa_key_pass, "r") as priv:
            fil = priv.read()
            private_key = rsa.PrivateKey.load_pkcs1(fil.encode(), "PEM")
        self._pwd = rsa.decrypt(pwd, private_key).decode()
        app_log.debug("Password received")

    def get_user_login(self):
        with open(self.login_path, "r", encoding="utf-8") as file1:
            f1 = json.load(file1)
            self._user = f1.get("user")
            app_log.debug("Username received")

    def connect(self):
        for _ in range(self.retry_number):
            try:
                self.client.login()
                app_log.info("Login succesfull")
                self.is_connect = True
                break
            except (GarminConnectConnectionError, GarminConnectTooManyRequestsError, GarminConnectAuthenticationError) as err:
                app_log.info(f"Reconnection: {err}")
                sleep(self.default_sleep)
                self.create_garmin_inst()
            except Exception as ex:
                app_log.info(f"Reconnection: {ex}")
                sleep(self.default_sleep)
        else:
            app_log.error("Can not connect")
            quit(503)

    @error_wrap
    def get_full_name(self):
        return self.client.get_full_name()

    @error_wrap
    def get_unit_system(self):
        return self.client.get_unit_system()

    @error_wrap
    def get_hr_data(self, day: str):
            return self.client.get_heart_rates(day)

    @error_wrap
    def get_steps_data(self, day: str):
        return self.client.get_steps_data(day)

    @error_wrap
    def get_activities(self, start=0, limit=1):
        return self.client.get_activities(start, limit)

    @error_wrap
    def get_stats(self, day: str):
        self._day_stats = self.client.get_stats(day)
        return self._day_stats

    @property
    def day_stats(self) -> Dict:
        return self._day_stats

    @property
    def get_date(self) -> datetime.date:
        text_date = self.day_stats.get("calendarDate")
        return datetime.datetime.strptime(text_date, "%Y-%m-%d").date()

    @property
    def get_active_calories(self) -> float:
        return self.day_stats.get("activeKilocalories")

    @property
    def get_active_seconds(self) -> int:
        return self.day_stats.get("activeSeconds")

    @property
    def get_high_active_seconds(self) -> int:
        return self.day_stats.get("highlyActiveSeconds")

    @property
    def get_max_hr(self) -> int:
        return self.day_stats.get("maxHeartRate")

    @property
    def get_max_avg_hr(self) -> int:
        return self.day_stats.get("maxAvgHeartRate")

    @property
    def get_min_hr(self) -> int:
        return self.day_stats.get("minHeartRate")

    @property
    def get_rest_hr(self) -> int:
        return self.day_stats.get("restingHeartRate")

    @property
    def get_min_avg_hr(self) -> int:
        return self.day_stats.get("minAvgHeartRate")

    @property
    def get_sleep_seconds(self) -> int:
        return self.day_stats.get("sleepingSeconds")


if __name__ == "__main__":
    tdate = "2021-09-26"
    app_log.info("Garmin connection starts")
    cl = MyGarmin()
    cl.connect()
    pprint.pprint(cl.get_stats(tdate))
    del cl
    app_log.info("Garmin connection ends")
