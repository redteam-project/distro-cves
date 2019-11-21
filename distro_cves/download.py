import os

import urllib.request
from urllib.error import ContentTooShortError

class Download(object):
  """Parent object for CVE downloaders

  Args:
    path: download path

  Returns:
    None

  Raises:
    None
  """

  def __init__(self, path, url):
    self.path = path
    self.url = url

  def download(self):
    """Downloads the distro CVE data

    Args:

    Returns:
      downloaded_file: relative path of the file that was downloaded

    Raises:
      ContentTooShortError: if the download fails or is incomplete
    """

    filename = os.path.basename(self.url)
    try:
      urllib.request.urlretrieve(self.url, self.path + filename)
    except ContentTooShortError as e:
      raise e
    downloaded_file = self.path + filename

    return downloaded_file

class DownloadDebian(Download):

  def __init__(self, path, url):
    super().__init__(path, url)

