export interface INavState {
    back: string | null;
    forward: string | null;
    up: string | null;
}

export enum BUTTON_TYPE {
    BACK,
    FORWARD,
    UP
}

export interface INavAction {
    buttonName: BUTTON_TYPE;
    payload: string;
}

export default INavAction;