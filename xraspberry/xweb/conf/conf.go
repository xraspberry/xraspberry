package conf

import (
	"gopkg.in/yaml.v2"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
)

type ServiceConfigStruct struct {
	Port  int    `yaml:port`
	DBUrl string `yaml:db_url`
}

var ServiceConfig = &ServiceConfigStruct{}

func init() {
	dir, _ := os.Getwd()
	configFile := filepath.Join(dir, "conf/config.yml")

	confFile, err := filepath.Abs(configFile)
	if err != nil {
		log.Printf("No correct config file: %s - %s", configFile, err.Error())
		os.Exit(1)
	}

	configs, err := ioutil.ReadFile(confFile)
	if err != nil {
		log.Printf("Failed to read config fliel <%s> : %s", confFile, err.Error())
		os.Exit(1)
	}

	err = yaml.Unmarshal(configs, ServiceConfig)
	if err != nil {
		log.Printf("Failed to parse config fliel <%s> : %s", confFile, err.Error())
		os.Exit(1)
	}
}
