export const routes = [
    {
        path: "/",
        component: () => import("../views/index.vue"),
    }, {
        path: "/settings",
        component: () => import("../views/settings.vue"),
    }, {
        path: "/welcome",
        component: () => import("../views/welcome.vue"),
    }
]
