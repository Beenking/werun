//rank.js

const app = getApp()

Page({
  data: {
    ranks:[],
    motto: '步数挑战'
  },

  onLoad: function () {
    wx.request({
      url: app.globalData.wxserver + 'ranks',
      method: 'post',
      header: { 'Content-Type': "application/x-www-form-urlencoded" },
      data:{user:'wb'},
      success: res => {
        if (res.data) {
          this.setData({
            ranks: res.data
          })
          console.log(res.data)
        }
        else{
          console.log('empty res.data')
        }
      }
    })
  }
})