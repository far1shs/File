import {nextTick, ref, watch} from "vue";

export const screenWidth =
    ref(window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth);
export const screenHeight =
    ref(window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight);

window.onresize = () => {
    nextTick(() => {
        screenWidth.value = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    });
    nextTick(() => {
        screenHeight.value = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
    });
};

watch(() => screenWidth, (value) => {
    screenWidth.value = Number(value);
});

watch(() => screenHeight, (value) => {
    screenHeight.value = Number(value);
});