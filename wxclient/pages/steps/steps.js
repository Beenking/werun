//steps.js
const util = require('../../utils/util.js')

const app = getApp()

Page({
  data: {
    logs:[],
    steps: [],
    motto: '步数挑战'
  },

  onLoad: function () {
    console.log('Page steps Enter')
    this.setData({
      logs: (wx.getStorageSync('logs') || []).map(log => {
        return util.formatTime(new Date(log))
      })
    })
    console.log('Page index Leave')
  },

  //获取encryptedData（没有解密的步数）和iv（加密算法的初始向量）
  getStepData: function () {
    wx.getWeRunData({
      success: res => {
        console.log(res);
        var encryptedData = res.encryptedData
        var iv = res.iv
        wx.request({
          url: app.globalData.wxserver + 'getStepData',
          method: 'post',
          header: { 'Content-Type': "application/x-www-form-urlencoded" },
          data:
          {
            iv: iv,
            encryptedData: encryptedData
          },
          success: res => {
            if (res) {
              var runData = res.data
              runData.stepInfoList = runData.stepInfoList.reverse()
              for (var i in runData.stepInfoList) {
                runData.stepInfoList[i].date = util.formatTime(
                  new Date(runData.stepInfoList[i].timestamp * 1000))
                delete(runData.stepInfoList[i].timestamp)
              }
              this.setData({
                steps: runData.stepInfoList.slice(0, 10)
              })
              this.data.steps = runData.stepInfoList.slice(0,10)
              console.log(this.data.steps)
            }
          }
        })
      },
      fail: function (res) {
        wx.showModal({
          title: '提示',
          content: '开发者未开通微信运动，请关注“微信运动”公众号后重试',
          showCancel: false,
          confirmText: '知道了'
        })
      }
    })
  }
})
