package models

import (
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/sqlite"
	"log"
	"os"
	"time"
	"xweb/conf"
)

var DB *gorm.DB = initDB()

func initDB() *gorm.DB {
	db, err := gorm.Open("sqlite3", conf.ServiceConfig.DBUrl)
	if err != nil {
		log.Printf("db connect failed! %s", err.Error())
		os.Exit(1)
	}
	db.LogMode(true)
	return db
}

type BaseModel struct {
	ID        int        `gorm:"primary_key" json:"id"`
	CreatedAt time.Time  `json:"created_at"`
	UpdatedAt time.Time  `json:"updated_at"`
	DeletedAt *time.Time `json:"-"`
}
