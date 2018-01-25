package main

import (
	"github.com/gin-gonic/gin"
	"xweb/controllers"
	"xweb/middleware"
)

func RegisterRouterHandler(ginIns *gin.Engine) {
	ginIns.Use(middleware.CORS(ginIns))
	ginIns.GET("/", controllers.Root)
}
