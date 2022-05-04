
import { renderSlot } from "vue";
import {axiosInst} from "./axios-api.js";

export default class Functions {

    get_file_extension(filename) {
        return (/[.]/.exec(filename)) ? /[^.]+$/.exec(filename)[0] : undefined;
    }

}