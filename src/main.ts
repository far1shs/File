import {createApp} from "vue";
import App from "./App.vue";
import PrimeVue from "primevue/config";
import Aura from "@primevue/themes/aura";
import ToastService from "primevue/toastservice";
import ConfirmationService from "primevue/confirmationservice";
import "primeicons/primeicons.css"
import {definePreset} from "@primevue/themes";
import naive from "naive-ui";
import {routes} from "./routes/routes.ts";
import createSiteRouter from "./routes/router.ts";
import axios from "axios";
import AnimateOnScroll from "primevue/animateonscroll";
import {getApiListItem} from "./script/tool.ts";
import {apiList} from "./model";

const app = createApp(App);
const router = createSiteRouter(routes);


if (localStorage.getItem("initial")) {
    apiList.value = getApiListItem(String(localStorage.getItem("api")), JSON.parse(String(localStorage.getItem("api_list"))));
}
if (localStorage.getItem("initial")) {
    axios.defaults.baseURL = apiList.value?.path;
}
if (localStorage.getItem("initial")) {
    axios.defaults.headers["X-API-KEY"] = String(apiList.value?.key);
}
axios.defaults.timeout = 10000;

const Noir = definePreset(Aura, {
    semantic: {
        primary: {
            50: "{zinc.50}",
            100: "{zinc.100}",
            200: "{zinc.200}",
            300: "{zinc.300}",
            400: "{zinc.400}",
            500: "{zinc.500}",
            600: "{zinc.600}",
            700: "{zinc.700}",
            800: "{zinc.800}",
            900: "{zinc.900}",
            950: "{zinc.950}"
        },
        colorScheme: {
            light: {
                primary: {
                    color: "{zinc.950}",
                    inverseColor: "#ffffff",
                    hoverColor: "{zinc.900}",
                    activeColor: "{zinc.800}"
                },
                highlight: {
                    background: "{zinc.950}",
                    focusBackground: "{zinc.700}",
                    color: "#ffffff",
                    focusColor: "#ffffff"
                }
            },
            dark: {
                primary: {
                    color: "{zinc.50}",
                    inverseColor: "{zinc.950}",
                    hoverColor: "{zinc.100}",
                    activeColor: "{zinc.200}"
                },
                highlight: {
                    background: "rgba(250, 250, 250, .16)",
                    focusBackground: "rgba(250, 250, 250, .24)",
                    color: "rgba(255,255,255,.87)",
                    focusColor: "rgba(255,255,255,.87)"
                }
            }
        }
    }
});
app.use(PrimeVue, {
    theme: {
        preset: Noir,
        options: {
            darkModeSelector: ".dark-model"
        }
    }
});
app.use(router);
app.use(ToastService);
app.use(ConfirmationService);
app.use(naive);
app.directive("animateonscroll", AnimateOnScroll);
app.mount("#app");
