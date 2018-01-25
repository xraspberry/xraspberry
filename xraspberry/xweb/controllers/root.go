package controllers

import "github.com/gin-gonic/gin"

func Root(c *gin.Context) {
	c.JSON(200, "Hello! It's Xraspberry")
}
