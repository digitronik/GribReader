import csv
from datetime import datetime, timedelta

import pygrib
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


class Grib(object):
    """Grib v1 and v2 file reading and some basic properties related to parameters

    :param path: Path of Grib file.
    :type path: str

    .. code-block:: python

    grb_file = Grib(name="test_file.grib2")
    grb = grb_file.read()
    """

    def __init__(self, path):
        self.path = path

    @property
    def read(self):
        """Read the grib file.

        :returns: pygrib object
        :rtype: pygrib.open
        """
        return pygrib.open(self.path)

    def latlons(self):
        """Latitude and Longitude of data.

        :returns: Tuple of array of latitude and longitude.
        :rtype: tuple
        """
        return self.read[1].latlons()

    @property
    def data(self):
        """Read grib file data.

        :returns: Complete grib file data.
        :rtype: dict
        """
        return {el["name"]: el for el in self.read}

    @property
    def parameters(self):
        """Get list of all available parameters with grib file.

        :returns: List of parameters.
        :rtype: list
        """
        return list(self.data.keys())

    def _parameter(self, name):
        return self.read.select(name=name)[0]

    def select(self, name):
        """Select parameter for more operations.

        :param name: Name of parameter (grib message).
        :type name: str
        :returns: Instance of Grb
        :rtype: instance
        """
        return Grb(parameter=self._parameter(name=name))


class Grb(object):
    """Provide specific parameter operations

    :param parameter: Parameter (grib message) object.
    :type parameter: instance

    .. code-block:: python

    grb_file = Grib(name="test_file.grib2")
    grb = grb_file.select("Significant height of combined wind waves and swell")
    grb.plot()
    """

    def __init__(self, parameter):
        self.parameter = parameter

    def plot(self, lat=None, lon=None, bar_orientation="horizontal"):
        """Plot graph for parameter (grib message)

        :param lat: Latitude else it will take as per grib file.
        :type lat: float
        :param lon: Longitude else it will take as per grib file.
        :type lon: float
        :param bar_orientation: Color bar orientation default is horizontal (horizontal/vertical).
        :type lon: float
        """
        if not (lat or lon):
            lat, lon = self.parameter.latlons()

        m = Basemap(
            projection="mill",
            lat_ts=10,
            llcrnrlon=lon.min(),
            urcrnrlon=lon.max(),
            llcrnrlat=lat.min(),
            urcrnrlat=lat.max(),
            resolution="c",
        )

        x, y = m(lon, lat)
        cs = m.pcolormesh(x, y, self.parameter.values, shading="flat", cmap=plt.cm.jet)

        m.drawcoastlines()
        m.drawmapboundary()
        m.fillcontinents()
        m.drawparallels(np.arange(-90.0, 120.0, 10.0), labels=[1, 0, 0, 0], color="grey")
        m.drawmeridians(
            np.arange(-180.0, 180.0, 10.0), labels=[0, 0, 0, 1], latmax=100.0, color="grey"
        )

        plt.colorbar(cs, orientation=bar_orientation)
        plt.title(self.parameter["name"])
        plt.show()

    @property
    def longitudes(self):
        """Get list of longitudes of parameter.

        :returns: longitudes
        :rtype: list
        """
        return list(self.parameter.distinctLongitudes)

    @property
    def min_lon(self):
        """Get start value of longitudes range.

        :returns: Minimum longitude
        :rtype: float
        """
        return min(self.longitudes)

    @property
    def max_lon(self):
        """Get end value of longitudes range.

        :returns: Maximum longitude
        :rtype: float
        """
        return max(self.longitudes)

    @property
    def latitudes(self):
        """Get list of latitudes of parameter.

        :returns: latitudes
        :rtype: list
        """

        return list(self.parameter.distinctLatitudes)

    @property
    def min_lat(self):
        """Get start value of latitudes range.

        :returns: Minimum latitude
        :rtype: float
        """
        return min(self.latitudes)

    @property
    def max_lat(self):
        """Get end value of latitudes range.

        :returns: Maximum latitude
        :rtype: float
        """
        return max(self.latitudes)

    @property
    def data(self):
        """Get data of parameter.

        :returns: Data of parameter.
        :rtype: array
        """

        return self.parameter.values.data

    def data_latlon(self, lat, lon):
        """Get data for Specific latitudes and longitudes.

        :param lat: Latitude
        :type lat: float
        :param lon: Longitude
        :type lon: float
        :returns: Data of latitude and longitudes.
        :rtype: float
        """
        return self.data[self.latitudes.index(lat)][self.longitudes.index(lon)]

    @property
    def datadate(self):
        """Get data and time of data collection.

        :returns: datetime of data collection.
        :rtype: datetime.datetime
        """

        return datetime.strptime(str(self.parameter.dataDate), "%Y%m%d")

    @property
    def forcast_time(self):
        """Get forcast time.

        :returns: time of forcast.
        :rtype: datetime.datetime
        """
        return self.parameter.forecastTime

    @property
    def forcast_datetime(self):
        """Get data and time of forcast.

        :returns: datetime of data forcast.
        :rtype: datetime.datetime
        """
        return self.datadate + timedelta(hours=self.forcast_time)

    def export_csv(self, path):
        """Export parameter data in csv file.
        :param path: Path to save csv file.
        :type path: str
        """
        with open("path", "wb") as csvfile:
            dw = csv.writer(csvfile, delimiter=",")
            lon_csv = ["Latitude /Longitude"] + self.longitudes
            dw.writerow(lon_csv)

            for lat in self.latitudes:
                row = [lat]
                for lon in self.longitudes:
                    value = self.data_latlon(lat, lon)

                    if isinstance(value, np.float64):
                        row.append(str(value))
                    else:
                        row.append("--")
                dw.writerow(row)
