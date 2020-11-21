import {combineReducers} from "redux";
import setButtonTarget from "./navbar";

const reducer = combineReducers({
    'navbar': setButtonTarget
})

export default reducer;