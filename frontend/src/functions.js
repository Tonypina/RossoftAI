
import { renderSlot } from "vue";
import {axiosInst} from "./axios-api.js";

export default class Functions {

    get_file_extension(filename) {
        return (/[.]/.exec(filename)) ? /[^.]+$/.exec(filename)[0] : undefined;
    }

    round(num) {
        var m = Number((Math.abs(num) * 100).toPrecision(15));
        return Math.round(m) / 100 * Math.sign(num);
    }

}