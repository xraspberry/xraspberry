package controllers

import (
	"github.com/gin-gonic/gin"
	"xweb/models"
)

type User struct {
	Username string `json:username`
}

func Root(c *gin.Context) {
	err := models.DB.CreateTable(&User{}).Error
	if err != nil {
		c.JSON(400, err.Error())
	}
	err = models.DB.DropTable(&User{}).Error
	if err != nil {
		c.JSON(400, err.Error())
	}

	c.JSON(200, "Hello! It's Xraspberry")
}
