import Vue from 'vue'
import Router from 'vue-router'
import MyVuetable from '@/components/MyVuetable'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/users',
      name: 'MyVuetable',
      component: MyVuetable
    }
  ]
})
