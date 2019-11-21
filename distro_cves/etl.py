import json
import os

class ETL(object):

  def __init__(self, path):
    self.path = path

  def extract(self, path):
    try:
      with open(path, 'rb') as f:
        json_content = f.read()
      cve_dict = json.loads(json_content.decode('utf-8'))
    except json.JSONDecodeError as e:
      raise e
    except TypeError as e:
      raise TypeError('json.loads failed in ETL.extract: ' + str(e))
    return cve_dict

  def transform(self, cve_dict):
    pass

  def load(self, newline_json):
    pass

class ETLDebian(ETL):

  def __init__(self, path):
    super().__init__(path)

  def transform(self, cve_dict):
    local_file = self.path + 'newline.json'

    newline_list = []
    for package in cve_dict.keys():
      cve_list = []
      for cve in cve_dict[package].keys():
        this_cve = cve_dict[package][cve]
        for release in this_cve['releases'].keys():
          this_release = this_cve['releases'][release]
          repositories = []
          for repo in this_release['repositories'].keys():
            repositories.append({
              'release_name': repo,
              'version': this_release['repositories'][repo]
            })
          cve_dict[package][cve]['releases'][release]['repositories'] = repositories
        cve_list.append({
          'cve_id': cve,
          'details': cve_dict[package][cve]
        })
      newline_list.append({
        'package': package,
        'cves': cve_list
      })

    try:
      # The file may already exist, but we want to start with an empty one
      if os.path.isfile(local_file):
        try:
          os.remove(local_file)
        except Exception as e:
          # todo: properly handle exception types here
          raise e

      # This seems clunky, but we want one json object per line for our BQ load
      for line in newline_list:
        with open(local_file, 'a') as f:
          f.write(json.dumps(line, indent=None, separators=(',', ':')) + '\n')

    except IOError as e:
      raise IOError('newline delimited json serialization failed in '
                    'ETLDebian.transform: ' + str(e))

    return local_file

