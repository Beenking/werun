//app.js
App({
  onLaunch: function () {
    console.log('App OnLauch enter')

    // 展示本地存储能力
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 获取用户信息
    wx.getSetting({
      success: res => {
        if (res.authSetting['scope.userInfo']) {

          // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
          wx.getUserInfo({
            success: res => {
              // 可以将 res 发送给后台解码出 unionId
              console.log(res)
              this.globalData.userInfo = res.rawData
              // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
              // 所以此处加入 callback 以防止这种情况
              if (this.userInfoReadyCallback) {
                this.userInfoReadyCallback(res)
              }
            }
          })

          // 登录
          wx.login({
            success: res => {
              if (res.code) {
                // 发送 res.code 到后台换取 openId, sessionKey, unionId
                wx.request({
                  url: this.globalData.wxserver + 'wxusr',
                  method: 'post',
                  header: { 'Content-Type': "application/x-www-form-urlencoded" },
                  data:{
                    code: res.code,
                    userInfo: this.globalData.userInfo
                  },
                  success: res => {
                    console.log('user login server sucessed!')
                  }
                })
              } else {
                console.log('wx.login failed!' + res.errMsg)
              }
            }
          })
        }
      }
    })

    console.log('App OnLauch leave')
  },

  globalData: {
    userInfo: null,
    wxserver:'http://66.112.220.247:5000/'
    //http://127.0.0.1:5000/
    //http://66.112.220.247:5000/
  }
})