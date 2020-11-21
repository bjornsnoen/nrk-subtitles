import {INavState, INavAction, BUTTON_TYPE} from "../actions/navbar";

const setButonTarget = (state: INavState = {back: null, forward: null, up: null}, action: INavAction) => {
    switch (action.buttonName) {
        case BUTTON_TYPE.BACK:
            state.back = action.payload;
            break;
        case BUTTON_TYPE.FORWARD:
            state.forward = action.payload
            break;
        case BUTTON_TYPE.UP:
            state.up = action.payload
            break;
    }

    return state;
}

export default setButonTarget;