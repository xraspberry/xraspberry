package middleware

import "github.com/gin-gonic/gin"

func applyCors(c *gin.Context) {
	c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
	c.Writer.Header().Set("Access-Control-Max-Age", "86400")
	c.Writer.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE, UPDATE")
	c.Writer.Header().Set("Access-Control-Allow-Headers", "Origin, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization")
	c.Writer.Header().Set("Access-Control-Expose-Headers", "Content-Length")
	c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
}

func CORS(router *gin.Engine) func(c *gin.Context) {
	router.OPTIONS("/*cors", func(c *gin.Context) {
		applyCors(c)
	})
	return func (c *gin.Context) {
		applyCors(c)
	}
}