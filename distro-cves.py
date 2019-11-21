from distro_cves.download import DownloadDebian
from distro_cves.etl import ETLDebian

class DistroCVEs(object):

  def __init__(self):
    self.debian_cve_url = 'https://security-tracker.debian.org/tracker/data/json'
    self.debian_local_path = './debian/'

  def debian(self):
    d = DownloadDebian(self.debian_local_path,
                       self.debian_cve_url)
    etl = ETLDebian(self.debian_local_path)

    debian_cve_file = d.download()
    cve_dict = etl.extract(debian_cve_file)
    newline_json_file = etl.transform(cve_dict)

def main():
  distro_cves = DistroCVEs()
  distro_cves.debian()

if __name__ == '__main__':
  main()