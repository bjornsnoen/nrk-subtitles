export interface INavState {
  back: string | null;
  forward: string | null;
  up: string | null;
}

export enum ButtonType {
  BACK,
  FORWARD,
  UP,
}

export interface INavAction {
  buttonName: ButtonType;
  payload: string;
}

export default INavAction;
