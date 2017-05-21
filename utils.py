# Utils (config, etc)
#
# Copyright: Ricardo Salveti <rsalveti@rsalveti.net>
#
# SPDX-License-Identifier: MIT

class Config:
    def __init__(self, defaults = {}, config_file = "/config.json"):
        self.config = defaults
        self.config_file = config_file

        import ujson as json
        try:
            with open(config_file) as f:
                config = json.loads(f.read())
        except (OSError, ValueError):
            print("Could not load %s, saving defaults" % config_file)
            self.store_config()
        else:
            self.config.update(config)
            print("Loaded config from", config_file)

    def store_config(self):
        import ujson as json
        try:
            with open(self.config_file, "w") as f:
                f.write(json.dumps(self.config))
        except OSError:
            print("Could not save", self.config_file)

    def get(self, name, default = None):
        try:
            return self.config[name]
        except KeyError:
            return default

    def set(self, name, value):
        self.config[name] = value
        self.store_config()

