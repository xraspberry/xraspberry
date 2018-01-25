package main

import (
	"fmt"
	"github.com/facebookgo/grace/gracehttp"
	"github.com/gin-gonic/gin"
	"log"
	"net/http"
	"time"
	"xweb/conf"
)

func main() {
	ginIns := gin.New()

	ginIns.Use(gin.Recovery())
	ginIns.Use(gin.Logger())
	RegisterRouterHandler(ginIns)

	if err := gracehttp.Serve(
		&http.Server{
			Addr:              fmt.Sprintf(":%d", conf.ServiceConfig.Port),
			Handler:           ginIns,
			ReadTimeout:       5 * time.Minute,
			ReadHeaderTimeout: 5 * time.Minute,
		},
	); err != nil {
		log.Printf("fatal error: %s", err.Error())
	}
}
