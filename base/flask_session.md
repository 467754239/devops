## flask session

```
flask中的session默认是完全保留在客户端浏览器中的，
也就是说我往flask的session中写入数据，最终这些数据将会以json字符串的形式，
经过base64编码写入到用户浏览器的cookie里，也就是说无须依赖第三方数据库保存 session数据，
也无需依赖文件来保存，这一点倒是挺有意思

SecureCookieSession
```