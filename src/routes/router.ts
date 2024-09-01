import {nextTick, Ref} from "vue"
import {createRouter, createWebHistory, RouteLocationNormalized} from "vue-router"
import {LoadingBarApi} from "naive-ui"

export const loadingBarApiRef: Ref<LoadingBarApi | null> = { value: null } as Ref<LoadingBarApi | null>

export default function createSiteRouter(routes: any) {
  const router = createRouter({
    history: createWebHistory(),
    routes
  })

  router.beforeEach(function (to, from, next) {
    if (!from || to.path !== from.path) {
      if (loadingBarApiRef.value) {
        loadingBarApiRef.value.start()
      }
    }
    next()
  })

  router.afterEach(function (to: RouteLocationNormalized, from: RouteLocationNormalized) {
    if (!from || to.path !== from.path) {
      if (loadingBarApiRef.value) {
        loadingBarApiRef.value.finish()
      }
      if (to.hash && to.hash !== from.hash) {
        nextTick(() => {
          const el = document.querySelector(to.hash)
          if (el) el.scrollIntoView()
        })
      }
    }
  })

  return router
}