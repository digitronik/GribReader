import csv
from datetime import datetime, timedelta

import pygrib
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


class Grib:
    """grib v1 and v2 file reading and some basic properties related to parameters

    Args:
        name (str): name of grib file

    .. code-block:: python

    grb_file = Grib(name="multi_1.glo.grib2")
    grb = grb_file.read()
    """
    def __init__(self, name):
        self.name = name

    @property
    def read(self):
        return pygrib.open(self.name)

    def latlons(self):
        return self.read[1].latlons()

    @property
    def data(self):
        return {el['name']: el for el in self.read}

    @property
    def parameter_names(self):
        return list(self.data.keys())

    def parameter(self, name):
        return self.read.select(name=name)[0]

    def select_parameter(self, name):
        return Grb(parameter=self.parameter(name=name))


class Grb:
    def __init__(self, parameter):
        self.parameter = parameter

    def plot(self, lat=None, lon=None, bar_orientation='horizontal'):
        """For plotting graphs

        Args:
            lat (ndarray): Latitudes
            lon (ndarray): Longitude
            bar_orientation (str): color bar orientation ('horizontal', 'vertical')
        Returns:
            object for the :py:class: cfme.storage.volume.Volume
        """
        if not (lat or lon):
            lat, lon = self.parameter.latlons()

        m = Basemap(projection='mill',
                    lat_ts=10,
                    llcrnrlon=lon.min(),
                    urcrnrlon=lon.max(),
                    llcrnrlat=lat.min(),
                    urcrnrlat=lat.max(),
                    resolution='c'
                    )

        x, y = m(lon, lat)
        cs = m.pcolormesh(x, y, self.parameter.values, shading='flat', cmap=plt.cm.jet)

        m.drawcoastlines()
        m.fillcontinents()
        m.drawmapboundary()

        m.drawparallels(np.arange(-90., 120., 10.), labels=[1, 0, 0, 0], color='grey')
        m.drawmeridians(np.arange(-180., 180., 10.), labels=[0, 0, 0, 1], latmax=100., color='grey')

        plt.colorbar(cs, orientation=bar_orientation)
        plt.title(self.parameter['name'])
        plt.show()

    @property
    def longitudes(self):
        return list(self.parameter.distinctLongitudes)

    @property
    def min_lon(self):
        return min(self.longitudes)

    @property
    def max_lon(self):
        return max(self.longitudes)

    @property
    def latitudes(self):
        return list(self.parameter.distinctLatitudes)

    @property
    def min_lat(self):
        return min(self.latitudes)

    @property
    def max_lat(self):
        return max(self.latitudes)

    @property
    def data(self):
        return self.parameter.values.data

    def data_latlon(self, lat, lon):
        return self.data[self.latitudes.index(lat)][self.longitudes.index(lon)]

    @property
    def datadate(self):
        return datetime.strptime(str(self.parameter.dataDate), '%Y%m%d')

    @property
    def forcast_time(self):
        return self.parameter.forecastTime

    @property
    def forcast_datetime(self):
        return self.datadate + timedelta(hours=self.forcast_time)

    def export_csv(self, file):
        with open("export.csv", "wb") as csvfile:
            import ipdb; ipdb.set_trace()
            dw = csv.writer(csvfile, delimiter=',')
            lon_csv = ["Latitude /Longitude"] + self.latitudes
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
        return True
